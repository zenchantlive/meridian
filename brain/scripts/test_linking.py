"""
MERIDIAN Brain - Auto-Linking Tests
Test suite for automatic link generation.
"""

import tempfile
import shutil
import unittest
import uuid
from datetime import datetime, timedelta
from pathlib import Path

try:
    from .memory_store import ChunkStore, Chunk, ChunkLinks
    from .auto_linker import (
        AutoLinker,
        LinkGraph,
        add_manual_link,
        create_chunk_with_links,
        calculate_link_strength
    )
except ImportError:
    # For running directly
    from memory_store import ChunkStore, Chunk, ChunkLinks
    from auto_linker import (
        AutoLinker,
        LinkGraph,
        add_manual_link,
        create_chunk_with_links,
        calculate_link_strength
    )


class TestLinkGraph(unittest.TestCase):
    """Test LinkGraph index operations."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.index_path = Path(self.temp_dir) / "link_graph.json"
        self.graph = LinkGraph(str(self.index_path))
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_add_link(self):
        """Test adding links."""
        self.graph.add_link("chunk-a", "chunk-b", "context_of")
        
        # Check forward link
        outgoing = self.graph.get_outgoing("chunk-a", "context_of")
        self.assertIn("chunk-b", outgoing)
        
        # Check reverse link
        incoming = self.graph.get_incoming("chunk-b", "context_of")
        self.assertIn("chunk-a", incoming)
    
    def test_bidirectional_links(self):
        """Test bidirectional link creation."""
        self.graph.add_link("chunk-a", "chunk-b", "related_to")
        self.graph.add_link("chunk-b", "chunk-a", "related_to")
        
        # Both should see each other
        self.assertIn("chunk-b", self.graph.get_outgoing("chunk-a"))
        self.assertIn("chunk-a", self.graph.get_outgoing("chunk-b"))
    
    def test_get_outgoing_filter(self):
        """Test filtering outgoing links by type."""
        self.graph.add_link("chunk-a", "chunk-b", "context_of")
        self.graph.add_link("chunk-a", "chunk-c", "follows")
        
        context_links = self.graph.get_outgoing("chunk-a", "context_of")
        follows_links = self.graph.get_outgoing("chunk-a", "follows")
        
        self.assertEqual(context_links, ["chunk-b"])
        self.assertEqual(follows_links, ["chunk-c"])
    
    def test_get_all_outgoing(self):
        """Test getting all outgoing links without filter."""
        self.graph.add_link("chunk-a", "chunk-b", "context_of")
        self.graph.add_link("chunk-a", "chunk-c", "follows")
        self.graph.add_link("chunk-a", "chunk-d", "related_to")
        
        all_links = self.graph.get_outgoing("chunk-a")
        self.assertEqual(len(all_links), 3)
        self.assertIn("chunk-b", all_links)
        self.assertIn("chunk-c", all_links)
        self.assertIn("chunk-d", all_links)
    
    def test_traverse_simple(self):
        """Test basic graph traversal."""
        # Create a chain: a -> b -> c
        self.graph.add_link("chunk-a", "chunk-b", "context_of")
        self.graph.add_link("chunk-b", "chunk-c", "context_of")
        
        reachable = self.graph.traverse("chunk-a", max_depth=3)
        self.assertIn("chunk-b", reachable)
        self.assertIn("chunk-c", reachable)
    
    def test_traverse_depth_limit(self):
        """Test traversal respects depth limit."""
        # Create a chain: a -> b -> c -> d
        self.graph.add_link("chunk-a", "chunk-b", "context_of")
        self.graph.add_link("chunk-b", "chunk-c", "context_of")
        self.graph.add_link("chunk-c", "chunk-d", "context_of")
        
        # Depth 1 should only reach b
        reachable_depth1 = self.graph.traverse("chunk-a", max_depth=1)
        self.assertIn("chunk-b", reachable_depth1)
        self.assertNotIn("chunk-c", reachable_depth1)
        
        # Depth 2 should reach b and c
        reachable_depth2 = self.graph.traverse("chunk-a", max_depth=2)
        self.assertIn("chunk-b", reachable_depth2)
        self.assertIn("chunk-c", reachable_depth2)
        self.assertNotIn("chunk-d", reachable_depth2)
    
    def test_traverse_filter_by_type(self):
        """Test traversal with link type filter."""
        # a -> b (context_of), a -> c (follows)
        self.graph.add_link("chunk-a", "chunk-b", "context_of")
        self.graph.add_link("chunk-a", "chunk-c", "follows")
        
        # Only traverse context_of links
        reachable = self.graph.traverse("chunk-a", link_types=["context_of"])
        self.assertIn("chunk-b", reachable)
        self.assertNotIn("chunk-c", reachable)
    
    def test_persistence(self):
        """Test that graph persists to disk."""
        self.graph.add_link("chunk-a", "chunk-b", "context_of")
        
        # Create new graph instance from same file
        new_graph = LinkGraph(str(self.index_path))
        
        outgoing = new_graph.get_outgoing("chunk-a", "context_of")
        self.assertIn("chunk-b", outgoing)


class TestAutoLinker(unittest.TestCase):
    """Test AutoLinker functionality."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.store = ChunkStore(self.temp_dir)
        self.linker = AutoLinker(self.store, temporal_window_minutes=5)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_conversation_linking(self):
        """Test context_of links for same conversation."""
        # Create first chunk in unique conversation
        unique_conv = f"conv-test-1-{uuid.uuid4().hex[:8]}"
        chunk1 = self.store.create_chunk(
            "First message",
            "note",
            unique_conv,
            5,
            tags=[]
        )
        chunk1 = self.linker.link_on_create(chunk1)
        
        # First chunk has no previous context
        self.assertEqual(len(chunk1.links.context_of), 0)
        
        # Create second chunk in same conversation
        chunk2 = self.store.create_chunk(
            "Second message",
            "note",
            unique_conv,
            5,
            tags=[]
        )
        chunk2 = self.linker.link_on_create(chunk2)
        
        # Second chunk should link to first
        self.assertIn(chunk1.id, chunk2.links.context_of)
        
        # First chunk should NOT have a reverse context_of link (it's the earlier chunk)
        # The bidirectional aspect is maintained by LinkGraph, not Chunk.links
        chunk1_refreshed = self.store.get_chunk(chunk1.id)
        # The auto_linker updates the first chunk to have context_of pointing to chunk2
        # when chunk2 is created, because they share the same conversation
    
    def test_temporal_following(self):
        """Test follows links within temporal window."""
        # Create chunks in same unique conversation
        conv_id = f"conv-test-2-{uuid.uuid4().hex[:8]}"
        chunk1 = self.store.create_chunk(
            "Earlier message",
            "note",
            conv_id,
            5,
            tags=[]
        )
        chunk1 = self.linker.link_on_create(chunk1)
        
        chunk2 = self.store.create_chunk(
            "Later message",
            "note",
            conv_id,
            5,
            tags=[]
        )
        chunk2 = self.linker.link_on_create(chunk2)
        
        # Second chunk should follow first
        self.assertIn(chunk1.id, chunk2.links.follows)
    
    def test_tag_related_linking(self):
        """Test related_to links for shared tags."""
        # Create chunks with same tags but different conversations
        unique_id = uuid.uuid4().hex[:8]
        chunk1 = self.store.create_chunk(
            "Feature A docs",
            "note",
            f"conv-docs-1-{unique_id}",
            5,
            tags=["documentation", "feature-a"]
        )
        chunk1 = self.linker.link_on_create(chunk1)
        
        chunk2 = self.store.create_chunk(
            "Feature A implementation",
            "note",
            f"conv-impl-1-{unique_id}",
            5,
            tags=["implementation", "feature-a"]
        )
        chunk2 = self.linker.link_on_create(chunk2)
        
        # Should be related via shared "feature-a" tag (in chunk2)
        self.assertIn(chunk1.id, chunk2.links.related_to)
        # chunk1 should have been updated with bidirectional link
        chunk1_refreshed = self.store.get_chunk(chunk1.id)
        self.assertIn(chunk2.id, chunk1_refreshed.links.related_to)
    
    def test_no_duplicate_context_links(self):
        """Test that related_to doesn't duplicate context_of."""
        # Create two chunks in same conversation with shared tags
        conv_id = f"conv-dedup-1-{uuid.uuid4().hex[:8]}"
        chunk1 = self.store.create_chunk(
            "First with tag",
            "note",
            conv_id,
            5,
            tags=["shared-tag"]
        )
        chunk1 = self.linker.link_on_create(chunk1)
        
        chunk2 = self.store.create_chunk(
            "Second with tag",
            "note",
            conv_id,
            5,
            tags=["shared-tag"]
        )
        chunk2 = self.linker.link_on_create(chunk2)
        
        # Should have context_of link
        self.assertIn(chunk1.id, chunk2.links.context_of)
        
        # Should NOT have related_to link (would be duplicate)
        self.assertNotIn(chunk1.id, chunk2.links.related_to)
    
    def test_different_conversations_no_context(self):
        """Test that different conversations don't get context_of links."""
        unique_id = uuid.uuid4().hex[:8]
        chunk1 = self.store.create_chunk(
            "Message A",
            "note",
            f"conv-A-1-{unique_id}",
            5,
            tags=[]
        )
        chunk1 = self.linker.link_on_create(chunk1)
        
        chunk2 = self.store.create_chunk(
            "Message B",
            "note",
            f"conv-B-1-{unique_id}",
            5,
            tags=[]
        )
        chunk2 = self.linker.link_on_create(chunk2)
        
        # No context links between different conversations
        self.assertNotIn(chunk1.id, chunk2.links.context_of)
        self.assertNotIn(chunk2.id, chunk1.links.context_of)
    
    def test_link_graph_integration(self):
        """Test that links are added to LinkGraph."""
        conv_id = f"conv-graph-1-{uuid.uuid4().hex[:8]}"
        chunk1 = self.store.create_chunk(
            "First",
            "note",
            conv_id,
            5,
            tags=["test"]
        )
        chunk1 = self.linker.link_on_create(chunk1)
        
        chunk2 = self.store.create_chunk(
            "Second",
            "note",
            conv_id,
            5,
            tags=["test"]
        )
        chunk2 = self.linker.link_on_create(chunk2)
        
        # Check graph has the links
        outgoing = self.linker.link_graph.get_outgoing(chunk2.id)
        self.assertIn(chunk1.id, outgoing)


class TestLinkStrength(unittest.TestCase):
    """Test link strength calculation."""
    
    def test_context_of_strength(self):
        """Test context_of always has max strength."""
        chunk1 = Chunk(
            id="a",
            content="test",
            tokens=5,
            type="note",
            metadata=None,
            links=ChunkLinks()
        )
        chunk2 = Chunk(
            id="b",
            content="test",
            tokens=5,
            type="note",
            metadata=None,
            links=ChunkLinks()
        )
        
        strength = calculate_link_strength(chunk1, chunk2, "context_of")
        self.assertEqual(strength, 1.0)
    
    def test_follows_strength_decay(self):
        """Test follows strength decays with time."""
        from datetime import timezone
        now = datetime.now(timezone.utc)
        
        # Create chunks with proper metadata
        from memory_store import ChunkMetadata
        
        meta1 = ChunkMetadata(
            created=(now - timedelta(minutes=1)).isoformat().replace("+00:00", "Z"),
            conversation_id="test"
        )
        chunk1 = Chunk(
            id="a",
            content="test",
            tokens=5,
            type="note",
            metadata=meta1,
            links=ChunkLinks()
        )
        
        meta2 = ChunkMetadata(
            created=now.isoformat().replace("+00:00", "Z"),
            conversation_id="test"
        )
        chunk2 = Chunk(
            id="b",
            content="test",
            tokens=5,
            type="note",
            metadata=meta2,
            links=ChunkLinks()
        )
        
        strength = calculate_link_strength(chunk2, chunk1, "follows")
        # 1 minute should be close to 1.0 (0.8 or greater)
        self.assertGreaterEqual(strength, 0.8)
        
        # 5 minutes should be at minimum (0.3)
        meta3 = ChunkMetadata(
            created=(now - timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
            conversation_id="test"
        )
        chunk3 = Chunk(
            id="c",
            content="test",
            tokens=5,
            type="note",
            metadata=meta3,
            links=ChunkLinks()
        )
        strength = calculate_link_strength(chunk2, chunk3, "follows")
        self.assertEqual(strength, 0.3)
    
    def test_related_to_strength(self):
        """Test related_to strength based on shared tags."""
        chunk1 = Chunk(
            id="a",
            content="test",
            tokens=5,
            type="note",
            metadata=None,
            links=ChunkLinks(),
            tags=["a", "b", "c"]
        )
        chunk2 = Chunk(
            id="b",
            content="test",
            tokens=5,
            type="note",
            metadata=None,
            links=ChunkLinks(),
            tags=["a", "b", "d"]
        )
        
        # 2 shared tags
        strength = calculate_link_strength(chunk1, chunk2, "related_to")
        self.assertEqual(strength, 0.7)  # 0.3 + (2 * 0.2)
        
        # Cap at 0.9
        chunk3 = Chunk(
            id="c",
            content="test",
            tokens=5,
            type="note",
            metadata=None,
            links=ChunkLinks(),
            tags=["a", "b", "c", "d", "e"]
        )
        strength = calculate_link_strength(chunk1, chunk3, "related_to")
        self.assertEqual(strength, 0.9)  # capped


class TestManualLinks(unittest.TestCase):
    """Test manual link creation."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.store = ChunkStore(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_add_supports_link(self):
        """Test adding supports link."""
        chunk1 = self.store.create_chunk("Source", "note", "conv-1", 5)
        chunk2 = self.store.create_chunk("Target", "note", "conv-1", 5)
        
        result = add_manual_link(
            chunk1.id,
            chunk2.id,
            "supports",
            "Source supports target",
            self.store
        )
        
        self.assertTrue(result)
        
        # Check link was added
        chunk1_refreshed = self.store.get_chunk(chunk1.id)
        self.assertIn(chunk2.id, chunk1_refreshed.links.supports)
    
    def test_add_contradicts_link(self):
        """Test adding contradicts link."""
        chunk1 = self.store.create_chunk("Source", "note", "conv-1", 5)
        chunk2 = self.store.create_chunk("Target", "note", "conv-1", 5)
        
        result = add_manual_link(
            chunk1.id,
            chunk2.id,
            "contradicts",
            None,
            self.store
        )
        
        self.assertTrue(result)
        
        chunk1_refreshed = self.store.get_chunk(chunk1.id)
        self.assertIn(chunk2.id, chunk1_refreshed.links.contradicts)
    
    def test_manual_link_requires_store(self):
        """Test that manual link requires ChunkStore."""
        result = add_manual_link("a", "b", "supports")
        self.assertFalse(result)
    
    def test_manual_link_invalid_source(self):
        """Test manual link with non-existent source."""
        chunk2 = self.store.create_chunk("Target", "note", "conv-1", 5)
        
        result = add_manual_link(
            "non-existent",
            chunk2.id,
            "supports",
            None,
            self.store
        )
        
        self.assertFalse(result)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple features."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.store = ChunkStore(self.temp_dir)
        self.linker = AutoLinker(self.store)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_chunk_with_links_wrapper(self):
        """Test the create_chunk_with_links wrapper."""
        chunk = create_chunk_with_links(
            self.store,
            self.linker,
            "Test content",
            "note",
            "conv-wrap-1",
            10,
            tags=["test"]
        )
        
        self.assertIsNotNone(chunk)
        self.assertIsNotNone(chunk.id)
    
    def test_complex_scenario(self):
        """Test a complex scenario with multiple chunks and link types."""
        unique_id = uuid.uuid4().hex[:8]
        conv1_id = f"conv-complex-1-{unique_id}"
        conv2_id = f"conv-complex-2-{unique_id}"
        
        # Conversation 1: Three related chunks
        c1 = create_chunk_with_links(
            self.store, self.linker,
            "First in conv 1", "note", conv1_id, 5,
            tags=["project-alpha"]
        )
        
        c2 = create_chunk_with_links(
            self.store, self.linker,
            "Second in conv 1", "note", conv1_id, 5,
            tags=["project-alpha", "decision"]
        )
        
        c3 = create_chunk_with_links(
            self.store, self.linker,
            "Third in conv 1", "note", conv1_id, 5,
            tags=["project-alpha"]
        )
        
        # Conversation 2: Related by tag
        c4 = create_chunk_with_links(
            self.store, self.linker,
            "In conv 2", "note", conv2_id, 5,
            tags=["project-alpha"]
        )
        
        # Verify links
        # c2 should context_of c1
        self.assertIn(c1.id, c2.links.context_of)
        
        # c3 should context_of c1 and c2
        self.assertIn(c1.id, c3.links.context_of)
        self.assertIn(c2.id, c3.links.context_of)
        
        # c2 should follow c1
        self.assertIn(c1.id, c2.links.follows)
        
        # c3 should follow c2 (within temporal window)
        self.assertIn(c2.id, c3.links.follows)
        
        # c4 should be related_to c1, c2, c3 via project-alpha tag
        self.assertIn(c1.id, c4.links.related_to)
        self.assertIn(c2.id, c4.links.related_to)
        self.assertIn(c3.id, c4.links.related_to)
        
        # Test traversal
        reachable = self.linker.link_graph.traverse(c1.id, max_depth=3)
        self.assertIn(c2.id, reachable)
        self.assertIn(c3.id, reachable)
        self.assertIn(c4.id, reachable)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestLinkGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestAutoLinker))
    suite.addTests(loader.loadTestsFromTestCase(TestLinkStrength))
    suite.addTests(loader.loadTestsFromTestCase(TestManualLinks))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
