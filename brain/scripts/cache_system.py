"""
MERIDIAN Brain - Cache System (D5.1)
Simple in-memory and disk caching for frequently accessed data.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
from threading import Lock


@dataclass
class CacheEntry:
    """Single cache entry."""
    value: Any
    timestamp: float
    ttl: int  # Time to live in seconds


class MemoryCache:
    """Thread-safe in-memory cache with TTL support."""
    
    def __init__(self, default_ttl: int = 300):
        """
        Initialize memory cache.
        
        Args:
            default_ttl: Default time-to-live in seconds (5 minutes)
        """
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        self._lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                return None
            
            # Check if expired
            if time.time() - entry.timestamp > entry.ttl:
                del self._cache[key]
                return None
            
            return entry.value
    
    def set(self, key: str, value: Any, ttl: int = None):
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        if ttl is None:
            ttl = self._default_ttl
        
        with self._lock:
            self._cache[key] = CacheEntry(
                value=value,
                timestamp=time.time(),
                ttl=ttl
            )
    
    def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key was present and deleted
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self):
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
    
    def cleanup(self):
        """Remove all expired entries."""
        with self._lock:
            now = time.time()
            expired = [
                key for key, entry in self._cache.items()
                if now - entry.timestamp > entry.ttl
            ]
            for key in expired:
                del self._cache[key]
            return len(expired)
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                "size": len(self._cache),
                "default_ttl": self._default_ttl
            }


class DiskCache:
    """Simple disk-based cache for persistence across sessions."""
    
    def __init__(self, cache_dir: str, default_ttl: int = 3600):
        """
        Initialize disk cache.
        
        Args:
            cache_dir: Directory for cache files
            default_ttl: Default time-to-live in seconds (1 hour)
        """
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._default_ttl = default_ttl
    
    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key."""
        # Sanitize key for filesystem
        safe_key = "".join(c for c in key if c.isalnum() or c in "-_.")
        return self._cache_dir / f"{safe_key}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from disk cache."""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                entry = json.load(f)
            
            # Check expiration
            timestamp = entry.get("timestamp", 0)
            ttl = entry.get("ttl", self._default_ttl)
            
            if time.time() - timestamp > ttl:
                cache_path.unlink(missing_ok=True)
                return None
            
            return entry.get("value")
        
        except (json.JSONDecodeError, IOError):
            return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Store value in disk cache."""
        if ttl is None:
            ttl = self._default_ttl
        
        cache_path = self._get_cache_path(key)
        
        entry = {
            "value": value,
            "timestamp": time.time(),
            "ttl": ttl
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(entry, f)
        except (TypeError, IOError):
            pass  # Value might not be JSON serializable
    
    def delete(self, key: str) -> bool:
        """Delete key from disk cache."""
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False
    
    def clear(self):
        """Clear all disk cache entries."""
        for cache_file in self._cache_dir.glob("*.json"):
            cache_file.unlink()
    
    def cleanup(self) -> int:
        """Remove expired entries."""
        removed = 0
        for cache_file in self._cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    entry = json.load(f)
                
                timestamp = entry.get("timestamp", 0)
                ttl = entry.get("ttl", self._default_ttl)
                
                if time.time() - timestamp > ttl:
                    cache_file.unlink()
                    removed += 1
            except (json.JSONDecodeError, IOError):
                # Ignore malformed or unreadable cache files during cleanup; cleanup is best-effort.
                pass
        
        return removed
    
    def stats(self) -> Dict[str, Any]:
        """Get disk cache statistics."""
        count = len(list(self._cache_dir.glob("*.json")))
        return {
            "size": count,
            "cache_dir": str(self._cache_dir),
            "default_ttl": self._default_ttl
        }


class CacheManager:
    """Manages both memory and disk caches."""
    
    def __init__(self, cache_dir: str = None, default_ttl: int = 300):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory for disk cache (None for memory-only)
            default_ttl: Default time-to-live in seconds
        """
        self.memory = MemoryCache(default_ttl)
        self.disk = None
        if cache_dir:
            self.disk = DiskCache(cache_dir, default_ttl)
    
    def get(self, key: str, use_disk: bool = True) -> Optional[Any]:
        """
        Get from cache (memory first, then disk).
        
        Args:
            key: Cache key
            use_disk: Whether to check disk cache
            
        Returns:
            Cached value or None
        """
        # Check memory first
        value = self.memory.get(key)
        if value is not None:
            return value
        
        # Check disk if enabled
        if use_disk and self.disk:
            value = self.disk.get(key)
            if value is not None:
                # Promote to memory
                self.memory.set(key, value)
                return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = None, use_disk: bool = False):
        """
        Store in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live
            use_disk: Whether to also store in disk cache
        """
        self.memory.set(key, value, ttl)
        
        if use_disk and self.disk:
            self.disk.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """Delete from all caches."""
        mem_deleted = self.memory.delete(key)
        disk_deleted = self.disk.delete(key) if self.disk else False
        return mem_deleted or disk_deleted
    
    def clear(self):
        """Clear all caches."""
        self.memory.clear()
        if self.disk:
            self.disk.clear()
    
    def cleanup(self) -> Dict[str, int]:
        """Cleanup expired entries from all caches."""
        mem_removed = self.memory.cleanup()
        disk_removed = self.disk.cleanup() if self.disk else 0
        return {"memory": mem_removed, "disk": disk_removed}
    
    def stats(self) -> Dict[str, Any]:
        """Get combined cache statistics."""
        stats = {
            "memory": self.memory.stats()
        }
        if self.disk:
            stats["disk"] = self.disk.stats()
        return stats
