import unittest
import os
from utils.store import InMemoryKeyValueStore
from utils.sharding import ShardedKeyValueStore

class TestShardedStore(unittest.TestCase):
    def test_shard_distribution(self):
        s1 = InMemoryKeyValueStore()
        s2 = InMemoryKeyValueStore()
        s3 = InMemoryKeyValueStore()
        sharded_store = ShardedKeyValueStore([s1, s2, s3])
        
        # Insert 10 keys
        for i in range(10):
            key = f"key{i}"
            sharded_store.set(key, f"val{i}")
        
        # ensure we can retrieve them
        for i in range(10):
            key = f"key{i}"
            val = sharded_store.get(key)
            self.assertEqual(val, f"val{i}")

        # check distribution
        count_s1 = len(s1.all())
        count_s2 = len(s2.all())
        count_s3 = len(s3.all())
        # We won't test an exact distribution, but ensure it's not all in the same store
        self.assertTrue(count_s1 > 0 and count_s2 > 0 and count_s3 > 0)

if __name__ == "__main__":
    unittest.main()
