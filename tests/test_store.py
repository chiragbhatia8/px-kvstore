import unittest
import os
from utils.store import InMemoryKeyValueStore, FilePersistentStore

class TestInMemoryStore(unittest.TestCase):
    def test_basic_set_get(self):
        store = InMemoryKeyValueStore()
        store.set("a", "1")
        self.assertEqual(store.get("a"), "1")
        store.set("a", "2")
        self.assertEqual(store.get("a"), "2")

    def test_delete(self):
        store = InMemoryKeyValueStore()
        store.set("x", "y")
        store.delete("x")
        self.assertIsNone(store.get("x"))

class TestFilePersistentStore(unittest.TestCase):
    TEST_FILE = "test_store.json"

    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_persistence(self):
        store = FilePersistentStore(filename=self.TEST_FILE)
        store.set("foo", "bar")
        # Re-instantiate to confirm data was saved
        store2 = FilePersistentStore(filename=self.TEST_FILE)
        self.assertEqual(store2.get("foo"), "bar")


if __name__ == "__main__":
    unittest.main()
