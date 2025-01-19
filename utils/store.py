import os
import json
import threading
from functools import lru_cache

###############################################################################
# In-Memory Store
###############################################################################
class InMemoryKeyValueStore:
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def set(self, key, value):
        with self.lock:
            self.store[key] = value

    def get(self, key):
        with self.lock:
            return self.store.get(key)

    def delete(self, key):
        with self.lock:
            return self.store.pop(key, None)

    def all(self):
        with self.lock:
            # return a shallow copy of the entire dictionary
            return dict(self.store)


###############################################################################
# Persistence (JSON on Disk)
###############################################################################
class FilePersistentStore(InMemoryKeyValueStore):
    """
    Extends InMemoryKeyValueStore with JSON-based persistence.
    """
    def __init__(self, filename="store.json"):
        super().__init__()
        self.filename = filename
        self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                self.store = json.load(f)

    def _save(self):
        with self.lock:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.store, f)

    def set(self, key, value):
        super().set(key, value)
        self._save()

    def delete(self, key):
        removed = super().delete(key)
        if removed is not None:
            self._save()
        return removed

    def save_and_shutdown(self):
        """
        Save the data and release resources during server shutdown.
        """
        print("Persisting data to disk before shutdown...")
        self._save()


###############################################################################
# Caching (LRU)
###############################################################################
class CachedStore(InMemoryKeyValueStore):
    """
    Demonstrates using lru_cache for `.get()` calls. 
    The 'store' is still in memory. Each time we call set or delete, 
    we must invalidate or clear the cache to stay in sync.
    """
    def __init__(self):
        super().__init__()
        self._cached_get = self._lru_wrapper()

    def _lru_wrapper(self):
        @lru_cache(maxsize=128)
        def _cached(key):
            return super().get(key)
        return _cached

    def get(self, key):
        return self._cached_get(key)

    def set(self, key, value):
        # invalidate the cache for this key
        self._cached_get.cache_clear()
        super().set(key, value)

    def delete(self, key):
        self._cached_get.cache_clear()
        return super().delete(key)
