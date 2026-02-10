"""
MERIDIAN Brain - Cache System Tests
D5.1: Memory and disk caching tests
"""

import unittest
import tempfile
import shutil
import time
from pathlib import Path

# Handle both relative and direct imports
try:
    from brain.scripts.cache_system import MemoryCache, DiskCache, CacheManager
except ImportError:
    from cache_system import MemoryCache, DiskCache, CacheManager


class TestMemoryCache(unittest.TestCase):
    """Test in-memory cache."""
    
    def setUp(self):
        self.cache = MemoryCache(default_ttl=60)
    
    def test_basic_get_set(self):
        """Should store and retrieve values."""
        self.cache.set("key1", "value1")
        result = self.cache.get("key1")
        self.assertEqual(result, "value1")
    
    def test_missing_key(self):
        """Should return None for missing key."""
        result = self.cache.get("nonexistent")
        self.assertIsNone(result)
    
    def test_expiration(self):
        """Should expire entries after TTL."""
        cache = MemoryCache(default_ttl=1)  # 1 second TTL
        cache.set("key", "value")
        
        # Should exist immediately
        self.assertEqual(cache.get("key"), "value")
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should be expired
        self.assertIsNone(cache.get("key"))
    
    def test_delete(self):
        """Should delete keys."""
        self.cache.set("key", "value")
        self.assertTrue(self.cache.delete("key"))
        self.assertIsNone(self.cache.get("key"))
    
    def test_clear(self):
        """Should clear all entries."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        self.cache.clear()
        
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))
    
    def test_cleanup(self):
        """Should remove expired entries."""
        cache = MemoryCache(default_ttl=1)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        time.sleep(1.1)
        
        removed = cache.cleanup()
        self.assertEqual(removed, 2)
    
    def test_stats(self):
        """Should return stats."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        stats = self.cache.stats()
        self.assertEqual(stats["size"], 2)
        self.assertEqual(stats["default_ttl"], 60)


class TestDiskCache(unittest.TestCase):
    """Test disk-based cache."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.cache = DiskCache(self.temp_dir, default_ttl=60)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_basic_get_set(self):
        """Should store and retrieve values."""
        self.cache.set("key1", "value1")
        result = self.cache.get("key1")
        self.assertEqual(result, "value1")
    
    def test_missing_key(self):
        """Should return None for missing key."""
        result = self.cache.get("nonexistent")
        self.assertIsNone(result)
    
    def test_persistence(self):
        """Should persist across cache instances."""
        self.cache.set("key", "value")
        
        # Create new cache instance with same directory
        new_cache = DiskCache(self.temp_dir)
        result = new_cache.get("key")
        
        self.assertEqual(result, "value")
    
    def test_delete(self):
        """Should delete keys."""
        self.cache.set("key", "value")
        self.assertTrue(self.cache.delete("key"))
        self.assertIsNone(self.cache.get("key"))
    
    def test_stats(self):
        """Should return stats."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        stats = self.cache.stats()
        self.assertEqual(stats["size"], 2)


class TestCacheManager(unittest.TestCase):
    """Test combined cache manager."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.manager = CacheManager(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_set(self):
        """Should use memory cache by default."""
        self.manager.set("key", "value")
        result = self.manager.get("key")
        self.assertEqual(result, "value")
    
    def test_disk_promotion(self):
        """Should promote disk cache to memory."""
        # Set in both
        self.manager.set("key", "value", use_disk=True)
        
        # Clear memory only
        self.manager.memory.clear()
        
        # Should still get from disk
        result = self.manager.get("key")
        self.assertEqual(result, "value")
    
    def test_stats(self):
        """Should return combined stats."""
        self.manager.set("key", "value")
        
        stats = self.manager.stats()
        self.assertIn("memory", stats)
        self.assertIn("disk", stats)


if __name__ == "__main__":
    unittest.main()
