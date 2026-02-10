"""
MERIDIAN Brain - Auto-Linking System
D1.4: Automatic link generation between chunks for graph traversal

Provides AutoLinker for automatic link generation and LinkGraph for fast traversal.
"""

import json
import logging
from collections import deque
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Set, Any, Tuple

try:
    from .memory_store import Chunk, ChunkStore, ChunkLinks
except ImportError:
    # For running directly
    from memory_store import Chunk, ChunkStore, ChunkLinks

logger = logging.getLogger(__name__)


@dataclass
class LinkStrength:
    """Link strength with reasoning."""
    score: float
    reason: Optional[str] = None


class LinkGraph:
    """
    Maintain bidirectional link index for fast traversal.
    
    Stores links as adjacency lists with link type information:
    - from -> to (link_type)
    - to -> from (f"{link_type}_reverse")
    """
    
    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self._forward: Dict[str, Dict[str, List[str]]] = {}  # chunk -> {link_type -> [targets]}
        self._reverse: Dict[str, Dict[str, List[str]]] = {}  # chunk -> {link_type -> [sources]}
        self._load()
    
    def _load(self):
        """Load link graph from disk."""
        if self.index_path.exists():
            try:
                data = json.loads(self.index_path.read_text(encoding="utf-8"))
                self._forward = data.get("forward", {})
                self._reverse = data.get("reverse", {})
                logger.info(f"Loaded link graph from {self.index_path}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load link graph: {e}")
                self._forward = {}
                self._reverse = {}
    
    def _save(self):
        """Persist link graph to disk."""
        data = {
            "forward": self._forward,
            "reverse": self._reverse,
            "updated": datetime.utcnow().isoformat() + "Z"
        }
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    
    def add_link(self, from_id: str, to_id: str, link_type: str):
        """
        Add bidirectional link.
        
        Args:
            from_id: Source chunk ID
            to_id: Target chunk ID
            link_type: Type of link (context_of, follows, related_to, etc.)
        """
        # Initialize structures if needed
        if from_id not in self._forward:
            self._forward[from_id] = {}
        if to_id not in self._reverse:
            self._reverse[to_id] = {}
        
        # Add forward link: from -> to (link_type)
        if link_type not in self._forward[from_id]:
            self._forward[from_id][link_type] = []
        if to_id not in self._forward[from_id][link_type]:
            self._forward[from_id][link_type].append(to_id)
        
        # Add reverse link: to -> from (link_type_reverse)
        reverse_type = f"{link_type}_reverse"
        if reverse_type not in self._reverse[to_id]:
            self._reverse[to_id][reverse_type] = []
        if from_id not in self._reverse[to_id][reverse_type]:
            self._reverse[to_id][reverse_type].append(from_id)
        
        # Also update reverse lookup for from_id
        if to_id not in self._reverse:
            self._reverse[to_id] = {}
        if reverse_type not in self._reverse[to_id]:
            self._reverse[to_id][reverse_type] = []
        if from_id not in self._reverse[to_id][reverse_type]:
            self._reverse[to_id][reverse_type].append(from_id)
        
        # Also update forward lookup for to_id
        if to_id not in self._forward:
            self._forward[to_id] = {}
        
        self._save()
        logger.debug(f"Added link: {from_id} -> {to_id} ({link_type})")
    
    def get_outgoing(self, chunk_id: str, link_type: str = None) -> List[str]:
        """
        Get chunks linked FROM chunk_id.
        
        Args:
            chunk_id: Starting chunk
            link_type: Filter by link type (None for all)
        
        Returns:
            List of target chunk IDs
        """
        if chunk_id not in self._forward:
            return []
        
        if link_type:
            return self._forward[chunk_id].get(link_type, [])
        
        # Return all outgoing links
        result = []
        for targets in self._forward[chunk_id].values():
            result.extend(targets)
        return list(set(result))  # Remove duplicates
    
    def get_incoming(self, chunk_id: str, link_type: str = None) -> List[str]:
        """
        Get chunks linked TO chunk_id.
        
        Args:
            chunk_id: Target chunk
            link_type: Filter by link type (None for all)
        
        Returns:
            List of source chunk IDs
        """
        if chunk_id not in self._reverse:
            return []
        
        if link_type:
            return self._reverse[chunk_id].get(f"{link_type}_reverse", [])
        
        # Return all incoming links
        result = []
        for sources in self._reverse[chunk_id].values():
            result.extend(sources)
        return list(set(result))  # Remove duplicates
    
    def get_links(self, chunk_id: str, link_type: str = None) -> Dict[str, List[str]]:
        """
        Get all links for a chunk.
        
        Returns:
            Dict of link_type -> list of chunk IDs
        """
        if chunk_id not in self._forward:
            return {}
        
        if link_type:
            return {link_type: self._forward[chunk_id].get(link_type, [])}
        
        return dict(self._forward[chunk_id])
    
    def traverse(self, start_id: str, max_depth: int = 3,
                 link_types: List[str] = None) -> List[str]:
        """
        BFS traversal from start chunk.
        
        Args:
            start_id: Starting chunk ID
            max_depth: Maximum traversal depth
            link_types: Filter by link types (None for all)
        
        Returns:
            List of reachable chunk IDs (excluding start)
        """
        visited = {start_id}
        queue = deque([(start_id, 0)])
        result = []
        
        while queue:
            current_id, depth = queue.popleft()
            
            if depth >= max_depth:
                continue
            
            # Get outgoing links
            outgoing = self.get_outgoing(current_id, None)
            
            for target_id in outgoing:
                # Check link type filter
                if link_types:
                    if current_id in self._forward:
                        valid = False
                        for lt, targets in self._forward[current_id].items():
                            if target_id in targets and lt in link_types:
                                valid = True
                                break
                        if not valid:
                            continue
                
                if target_id not in visited:
                    visited.add(target_id)
                    result.append(target_id)
                    queue.append((target_id, depth + 1))
        
        return result
    
    def get_path(self, from_id: str, to_id: str,
                 link_types: List[str] = None) -> Optional[List[str]]:
        """
        Find path between two chunks using BFS.
        
        Returns:
            List of chunk IDs forming a path, or None if no path exists
        """
        if from_id == to_id:
            return [from_id]
        
        visited = {from_id}
        queue = deque([(from_id, [from_id])])
        
        while queue:
            current_id, path = queue.popleft()
            
            outgoing = self.get_outgoing(current_id, None)
            
            for target_id in outgoing:
                if link_types:
                    if current_id in self._forward:
                        valid = False
                        for lt, targets in self._forward[current_id].items():
                            if target_id in targets and lt in link_types:
                                valid = True
                                break
                        if not valid:
                            continue
                
                if target_id == to_id:
                    return path + [target_id]
                
                if target_id not in visited:
                    visited.add(target_id)
                    queue.append((target_id, path + [target_id]))
        
        return None


class AutoLinker:
    """
    Automatic link generation between chunks.
    
    Link Types:
    - context_of: Same conversation_id (bidirectional)
    - follows: Created within temporal window before this one (unidirectional)
    - related_to: Shares any tag (bidirectional)
    """
    
    def __init__(self, chunk_store: ChunkStore,
                 temporal_window_minutes: int = 5):
        self.chunk_store = chunk_store
        self.temporal_window = timedelta(minutes=temporal_window_minutes)
        self.link_graph = LinkGraph(
            str(chunk_store.index_path / "link_graph_index.json")
        )
    
    def link_on_create(self, new_chunk: Chunk) -> Chunk:
        """
        Generate automatic links when chunk is created.
        
        Args:
            new_chunk: The newly created chunk
        
        Returns:
            The chunk with updated links
        """
        chunk_id = new_chunk.id
        conversation_id = new_chunk.metadata.conversation_id
        created_str = new_chunk.metadata.created
        tags = new_chunk.tags
        
        # Parse creation timestamp
        try:
            created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            logger.warning(f"Invalid created timestamp for chunk {chunk_id}")
            created = datetime.utcnow()
        
        # 1. Find conversation context links
        context_chunks = self._find_conversation_chunks(conversation_id, chunk_id)
        for target_id in context_chunks:
            if target_id not in new_chunk.links.context_of:
                new_chunk.links.context_of.append(target_id)
                self.link_graph.add_link(chunk_id, target_id, "context_of")
                # Bidirectional
                self._add_reverse_link(target_id, chunk_id, "context_of")
        
        # 2. Find temporal predecessors
        predecessor_chunks = self._find_temporal_predecessors(
            created, conversation_id, chunk_id
        )
        for target_id in predecessor_chunks:
            if target_id not in new_chunk.links.follows:
                new_chunk.links.follows.append(target_id)
                self.link_graph.add_link(chunk_id, target_id, "follows")
        
        # 3. Find tag-related chunks
        related_chunks = self._find_tag_related(tags, chunk_id)
        for target_id in related_chunks:
            # Avoid duplicate links - if already context_of, skip weak related_to
            if target_id not in new_chunk.links.context_of:
                if target_id not in new_chunk.links.related_to:
                    new_chunk.links.related_to.append(target_id)
                    self.link_graph.add_link(chunk_id, target_id, "related_to")
                    # Bidirectional - add to target chunk as well
                    self._add_related_to_link(target_id, chunk_id)
        
        # Save updated chunk
        self._save_chunk(new_chunk)
        
        logger.info(f"Auto-linked chunk {chunk_id}: "
                   f"context={len(context_chunks)}, "
                   f"follows={len(predecessor_chunks)}, "
                   f"related={len(related_chunks)}")
        
        return new_chunk
    
    def _add_reverse_link(self, chunk_id: str, target_id: str, link_type: str):
        """
        Add bidirectional link to existing chunk.
        
        For bidirectional links (context_of, related_to), when new_chunk (target_id)
        links to existing_chunk (chunk_id), we also add a link from existing_chunk
        back to new_chunk to maintain bidirectionality.
        """
        chunk = self.chunk_store.get_chunk(chunk_id)
        if chunk:
            if link_type == "context_of":
                if target_id not in chunk.links.context_of:
                    chunk.links.context_of.append(target_id)
                    self._save_chunk(chunk)
                    # Also add to link graph for traversal
                    self.link_graph.add_link(chunk_id, target_id, link_type)
            elif link_type == "related_to":
                if target_id not in chunk.links.related_to:
                    chunk.links.related_to.append(target_id)
                    self._save_chunk(chunk)
                    # Also add to link graph for traversal
                    self.link_graph.add_link(chunk_id, target_id, link_type)
    
    def _add_related_to_link(self, target_id: str, new_chunk_id: str):
        """Add related_to link from target chunk to new chunk."""
        chunk = self.chunk_store.get_chunk(target_id)
        if chunk:
            if new_chunk_id not in chunk.links.related_to:
                chunk.links.related_to.append(new_chunk_id)
                self._save_chunk(chunk)
                # Also add to link graph for traversal
                self.link_graph.add_link(target_id, new_chunk_id, "related_to")
    
    def _save_chunk(self, chunk: Chunk):
        """Save chunk to storage without updating access tracking."""
        chunk_path = self.chunk_store._get_chunk_path(chunk.id)
        chunk_path.write_text(chunk.to_json(), encoding="utf-8")
    
    def _find_conversation_chunks(self, conversation_id: str,
                                   exclude: str) -> List[str]:
        """
        Find other chunks from same conversation.
        
        Args:
            conversation_id: Conversation to search
            exclude: Chunk ID to exclude (the new chunk)
        
        Returns:
            List of chunk IDs from same conversation (excluding the new chunk)
        """
        chunks = self.chunk_store.list_chunks(
            conversation_id=conversation_id
        )
        return [c for c in chunks if c != exclude]
    
    def _find_temporal_predecessors(self, created: datetime,
                                     conversation_id: str,
                                     exclude: str) -> List[str]:
        """
        Find chunks within temporal window before this one.
        
        Args:
            created: Creation time of new chunk
            conversation_id: Conversation to search
            exclude: Chunk ID to exclude (the new chunk)
        
        Returns:
            List of chunk IDs created within window before this chunk
        """
        window_start = created - self.temporal_window
        
        # Get chunks from same conversation within time window
        chunks = self.chunk_store.list_chunks(
            conversation_id=conversation_id,
            created_after=window_start,
            created_before=created
        )
        
        return [c for c in chunks if c != exclude]
    
    def _find_tag_related(self, tags: List[str], exclude: str) -> List[str]:
        """
        Find chunks sharing any tag.
        
        Args:
            tags: Tags to search for
            exclude: Chunk ID to exclude (the new chunk)
        
        Returns:
            List of chunk IDs sharing tags
        """
        if not tags:
            return []
        
        related = set()
        for tag in tags:
            chunks = self.chunk_store.tag_index.get_list(tag)
            related.update(chunks)
        
        # Exclude the new chunk itself
        related.discard(exclude)
        
        return list(related)


def calculate_link_strength(source: Chunk, target: Chunk,
                            link_type: str) -> float:
    """
    Calculate link strength based on link type and chunk attributes.
    
    Args:
        source: Source chunk
        target: Target chunk
        link_type: Type of link
    
    Returns:
        Strength score (0.0-1.0)
    """
    if link_type == "context_of":
        return 1.0
    
    elif link_type == "follows":
        # Time-decayed strength
        try:
            source_time = datetime.fromisoformat(
                source.metadata.created.replace("Z", "+00:00")
            )
            target_time = datetime.fromisoformat(
                target.metadata.created.replace("Z", "+00:00")
            )
            time_diff = (source_time - target_time).total_seconds()
            minutes = abs(time_diff) / 60
            return max(0.3, 1.0 - (minutes / 5))
        except (ValueError, AttributeError):
            return 0.5
    
    elif link_type == "related_to":
        # Based on shared tags
        shared = len(set(source.tags) & set(target.tags))
        return min(0.9, 0.3 + (shared * 0.2))
    
    elif link_type == "supports":
        return 0.8
    
    elif link_type == "contradicts":
        return 0.8
    
    return 0.5


def add_manual_link(from_id: str, to_id: str,
                    link_type: str, reason: str = None,
                    chunk_store: ChunkStore = None) -> bool:
    """
    Add manual link with optional reasoning.
    
    Supports manual link types:
    - supports: Source supports target
    - contradicts: Source contradicts/opposes target
    
    Args:
        from_id: Source chunk ID
        to_id: Target chunk ID
        link_type: Link type (supports, contradicts)
        reason: Optional reasoning for the link
        chunk_store: ChunkStore instance (required)
    
    Returns:
        True if link added successfully
    """
    if chunk_store is None:
        logger.error("ChunkStore required for manual linking")
        return False
    
    if link_type not in ("supports", "contradicts"):
        logger.warning(f"Unknown manual link type: {link_type}")
        return False
    
    # Get source chunk
    source = chunk_store.get_chunk(from_id)
    if not source:
        logger.error(f"Source chunk not found: {from_id}")
        return False
    
    # Add link
    if link_type == "supports":
        if to_id not in source.links.supports:
            source.links.supports.append(to_id)
    elif link_type == "contradicts":
        if to_id not in source.links.contradicts:
            source.links.contradicts.append(to_id)
    
    # Save source chunk
    chunk_path = chunk_store._get_chunk_path(from_id)
    chunk_path.write_text(source.to_json(), encoding="utf-8")
    
    # Update link graph
    linker = AutoLinker(chunk_store)
    linker.link_graph.add_link(from_id, to_id, link_type)
    
    logger.info(f"Added manual link: {from_id} -> {to_id} ({link_type})")
    if reason:
        logger.info(f"  Reason: {reason}")
    
    return True


# Integration function for ChunkStore
def create_chunk_with_links(store: ChunkStore, linker: AutoLinker,
                            content: str, chunk_type: str,
                            conversation_id: str, tokens: int,
                            tags: List[str] = None,
                            confidence: float = 0.7) -> Chunk:
    """
    Create chunk and auto-link it.
    
    Wrapper function that combines chunk creation with auto-linking.
    
    Args:
        store: ChunkStore instance
        linker: AutoLinker instance
        content: Chunk content
        chunk_type: Type of chunk
        conversation_id: Source conversation
        tokens: Token count
        tags: Optional tags
        confidence: Confidence score
    
    Returns:
        Created and linked chunk
    """
    chunk = store.create_chunk(
        content=content,
        chunk_type=chunk_type,
        conversation_id=conversation_id,
        tokens=tokens,
        tags=tags,
        confidence=confidence
    )
    
    return linker.link_on_create(chunk)


if __name__ == "__main__":
    # Test auto-linking
    try:
        from .memory_store import ChunkStore, init_storage
    except ImportError:
        from memory_store import ChunkStore, init_storage
    
    import tempfile
    import shutil
    
    # Use a temp directory for testing
    temp_dir = tempfile.mkdtemp()
    store = init_storage(temp_dir)
    linker = AutoLinker(store)
    
    # Create test chunks
    print("Creating test chunks...")
    chunk1 = store.create_chunk(
        "Content 1 - first in conversation",
        "note",
        "conv-123",
        10,
        tags=["test", "demo"]
    )
    chunk1 = linker.link_on_create(chunk1)
    print(f"Chunk 1 created: {chunk1.id}")
    print(f"  Links: {chunk1.links}")
    
    chunk2 = store.create_chunk(
        "Content 2 - second in conversation",
        "note",
        "conv-123",
        10,
        tags=["test", "feature"]
    )
    chunk2 = linker.link_on_create(chunk2)
    print(f"\nChunk 2 created: {chunk2.id}")
    print(f"  Links: {chunk2.links}")
    
    chunk3 = store.create_chunk(
        "Content 3 - different conversation",
        "note",
        "conv-456",
        10,
        tags=["demo", "other"]
    )
    chunk3 = linker.link_on_create(chunk3)
    print(f"\nChunk 3 created: {chunk3.id}")
    print(f"  Links: {chunk3.links}")
    
    # Test graph traversal
    print("\n--- Graph Traversal ---")
    print(f"From {chunk2.id}, outgoing: {linker.link_graph.get_outgoing(chunk2.id)}")
    print(f"From {chunk1.id}, incoming: {linker.link_graph.get_incoming(chunk1.id)}")
    
    reachable = linker.link_graph.traverse(chunk2.id, max_depth=2)
    print(f"Reachable from {chunk2.id}: {reachable}")
    
    # Test manual linking
    print("\n--- Manual Link ---")
    add_manual_link(
        chunk1.id,
        chunk2.id,
        "supports",
        "Chunk 1 provides context for chunk 2",
        store
    )
    
    chunk1_refreshed = store.get_chunk(chunk1.id)
    print(f"Chunk 1 after manual link: {chunk1_refreshed.links}")
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"\nCleaned up test directory: {temp_dir}")
