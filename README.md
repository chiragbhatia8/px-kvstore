# Python Key-Value Store

This is a Python-based Key-Value Store that offers the following features:
- In-Memory storage
- File-based persistence (JSON)
- Optional LRU caching for get operations
- Sharding across multiple store instances using consistent hashing

All functionality is implemented with Python standard library modules only.
For more detail, see [docs/UTILS.md](docs/UTILS.md).

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your_username/px-kvstore.git
   cd px-kvstore
   ```

2. (Optional) Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate   (Linux/Mac)
   or
   venv\Scripts\activate      (Windows)
   ```

3. Install the project (standard or editable mode):
   ```
   pip install .
   or
   pip install -e .
   ```

## Running the Service

You can run the service in three ways:

1. Directly via Python:
   ```
   python main.py
   ```
   By default, it listens on http://0.0.0.0:8080.
   Inside main.py, you can switch which store class to use (in-memory, file-based, naive encryption, etc.) by changing the store instantiation code.

2. CLI entry point:
   If you have installed the project with pip install ., you can run:
   ```
   px-kvstore
   ```
   That will start the same service defined by main.py (via the cli() function).

3. Docker:
   a) Build the Docker image:
      ```
      docker build -t px-kvstore .
      ```
   b) Run the container:
      ```
      docker run -p 8080:8080 px-kvstore
      ```
   The service is accessible on http://localhost:8080.

## Basic Usage Examples (Assuming default endpoints)

- PUT /kv:
  Create or update a key. Request body example:
  ```
  {"key":"feature_toggle","value":"true"}
  ```

- GET /kv?feature_toggle=true:
  Retrieve a single key-value pair.

- GET /kv:
  Retrieve a JSON object containing all key-value pairs.

- DELETE /kv:
  Remove a key by specifying a JSON body containing 
  ```
  {"key":"feature_toggle"}
  ```

A quick example with curl commands (service running on localhost:8080):

1. PUT a key-value:
   ```
   curl -X PUT -H "Content-Type: application/json" \
     -d '{"key":"feature_toggle","value":"true"}' \
     http://localhost:8080/kv
   ```

2. GET a single key:
   ```
   curl "http://localhost:8080/kv?key=feature_toggle"
   ```

3. GET all keys:
   ```
   curl http://localhost:8080/kv
   ```

4. DELETE a key:
   ```
   curl -X DELETE -H "Content-Type: application/json" \
     -d '{"key":"feature_toggle"}' \
     http://localhost:8080/kv
   ```

For more detail, For more detail, see [docs/API.md](docs/API.md).

## Testing

The tests are located in the tests/ directory. To run them, use:
   ```
   python -m unittest discover -s tests
   ```

The tests include:
- Unit tests for each store class (test_store.py)
- Tests for sharding logic (test_sharding.py)

Future Enhancements
1. Cache Expiration
Add TTL (time-to-live) for key-value pairs to automatically expire outdated or unnecessary data. This ensures optimal memory usage and helps manage fast-changing datasets.

2. Advanced Querying
Extend the key-value store to support complex queries such as:
K-Nearest Neighbors (KNN): Allow efficient similarity searches, for example, finding keys with values closest to a given target. This could be implemented using techniques like vector embeddings, spatial indexing (e.g., KD-Trees), or approximate nearest neighbors (ANN).
Partial Matches: Enable wildcard or pattern-based searches for keys or values.
Range Queries: Fetch all keys or values within a specific range, useful for numerical data.

3. Data Compression
Implement compression mechanisms like zlib to reduce storage size and improve I/O performance when handling large datasets.

4. Sharded Expansion
Expand the sharding logic to dynamically rebalance keys when new shards (stores) are added. This allows for seamless horizontal scaling without disrupting ongoing operations.