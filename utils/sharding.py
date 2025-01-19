import hashlib

def consistent_hash(key, buckets):
    """
    Return an index for which bucket to place 'key'.
    """
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    # convert first part of hex digest to int
    numeric = int(h[:8], 16)
    return numeric % buckets

class ShardedKeyValueStore:
    """
    Distributes keys across multiple store backends, each could be on a different host 
    or just separate store objects in memory for demonstration.
    """
    def __init__(self, stores):
        self.stores = stores  # list of store instances, e.g., [FilePersistentStore(...), ...]
        self.num_stores = len(stores)

    def _get_store_for_key(self, key):
        idx = consistent_hash(key, self.num_stores)
        return self.stores[idx]

    def set(self, key, value):
        store = self._get_store_for_key(key)
        store.set(key, value)

    def get(self, key):
        store = self._get_store_for_key(key)
        return store.get(key)

    def delete(self, key):
        store = self._get_store_for_key(key)
        return store.delete(key)

    def all_keys(self):
        # We can collect from each store, but watch for collisions
        results = {}
        for s in self.stores:
            # merge each store's dict
            results.update(s.all())
        return results
