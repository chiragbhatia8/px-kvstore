# Utility Classes Documentation

The `utils` module provides the core functionality of the px-kvstore project. It contains classes for different key-value store implementations and sharding logic.

## Core Features

## In-Memory Storage:
A simple, thread-safe key-value store that keeps data in memory for fast access, ideal for ephemeral or lightweight use cases.

## File-Based Persistence:
Extends the in-memory store by saving key-value pairs to a JSON file, ensuring data durability across server restarts.

## LRU Caching (Optional):
Optimizes frequently accessed keys by adding a Least Recently Used (LRU) caching mechanism, improving read performance for hot data.

## Sharding Across Stores:
Uses consistent hashing to distribute keys across multiple backend stores (e.g., multiple file stores or mixed in-memory and persistent stores). This improves scalability by allowing larger datasets to be distributed and managed efficiently.

## How It Works
The core logic of the service is structured around a modular design:

- Key-Value Stores: Each store (e.g., InMemoryKeyValueStore, FilePersistentStore) implements basic CRUD operations (set, get, delete, etc.), and stores data either in memory or in persistent files.
- ShardedKeyValueStore: This acts as a wrapper, distributing keys across multiple stores using consistent hashing. The key's hash determines which backend store handles the request, enabling horizontal scalability and efficient use of resources.

---

## Key-Value Store Classes

### 1. InMemoryKeyValueStore
**Description**: A simple thread-safe in-memory key-value store.
- Stores all data in memory.
- Does not support persistence or advanced features like encryption or compression.
- Best for lightweight, ephemeral data needs.

---

### 2. FilePersistentStore
**Description**: Extends `InMemoryKeyValueStore` with JSON-based file persistence.
- **Persistence**: Saves all key-value pairs to a JSON file after every write (set/delete).
- **Methods**:
  - `set(key, value)`: Adds or updates a key-value pair and persists changes to disk.
  - `delete(key)`: Removes a key-value pair and persists changes to disk.
  - `save_and_shutdown()`: Saves the data manually before shutting down the server.

---

### 3. CachedStore
**Description**: Extends `InMemoryKeyValueStore` with LRU caching for the `get` method.
- **LRU Cache**: Uses `functools.lru_cache` to cache the most recently accessed keys.
- Improves performance for frequently accessed keys.
- Cache invalidation happens on updates or deletions.

---

## Sharding Logic

### 4. ShardedKeyValueStore
**Description**: A wrapper class that distributes keys across multiple store instances using consistent hashing.
- **Consistent Hashing**: Maps keys to specific shards based on their hash.
- **Scalability**: Supports multiple underlying stores (e.g., file-based, in-memory).
- **Methods**:
  - `set(key, value)`: Stores the key-value pair in the appropriate shard.
  - `get(key)`: Retrieves the value from the correct shard.
  - `delete(key)`: Deletes the key from the shard.

---

## Example Usage
### Sharding Across Two Persistent Stores
```python
from utils.store import FilePersistentStore
from utils.sharding import ShardedKeyValueStore

store1 = FilePersistentStore(filename="shard1.json")
store2 = FilePersistentStore(filename="shard2.json")

sharded_store = ShardedKeyValueStore([store1, store2])
sharded_store.set("key1", "value1")
sharded_store.set("key2", "value2")

print(sharded_store.get("key1"))  # "value1"
print(sharded_store.get("key2"))  # "value2"
