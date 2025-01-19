# API Documentation for px-kvstore

The `px-kvstore` service exposes a simple REST API to interact with a key-value store. Below are the supported endpoints:

---

## 1. PUT /kv
**Description**: Create or update a key-value pair.

**Request**:
- Method: `PUT`
- URL: `/kv`
- Headers: 
  - `Content-Type: application/json`
- Body (JSON):
  ```json
  {
    "key": "someKey",
    "value": "someValue"
  }
  ```

**Response**:
- Status: `200 OK`
- Body:
  ```json
  {
    "someKey": "someValue"
  }
  ```

---

## 2. GET /kv
**Description**: Retrieve key-value pairs.

### a) Retrieve all pairs:
- Method: `GET`
- URL: `/kv`
- Response:
  ```json
  {
    "key1": "value1",
    "key2": "value2"
  }
  ```

### b) Retrieve a specific key:
- Method: `GET`
- URL: `/kv?key=someKey`
- Response:
  ```json
  {
    "someKey": "someValue"
  }
  ```
- If the key does not exist:
  ```json
  {
    "error": "Key not found"
  }
  ```

---

## 3. DELETE /kv
**Description**: Delete a specific key.

**Request**:
- Method: `DELETE`
- URL: `/kv`
- Headers:
  - `Content-Type: application/json`
- Body (JSON):
  ```json
  {
    "key": "someKey"
  }
  ```

**Response**:
- If the key is deleted:
  ```json
  {
    "result": "Key deleted"
  }
  ```
- If the key does not exist:
  ```json
  {
    "error": "Key not found"
  }
  ```

---

## 4. Graceful Shutdown
Pressing `Ctrl+C` during the server’s runtime initiates a **5-second countdown** before the server shuts down. During this period, the server saves all data to disk.

---

## Examples
### a) PUT a key-value pair:
```bash
curl -X PUT -H "Content-Type: application/json" \
     -d '{"key":"example","value":"hello"}' \
     http://localhost:8080/kv
```

### b) GET all key-value pairs:
```bash
curl http://localhost:8080/kv
```

### c) DELETE a key:
```bash
curl -X DELETE -H "Content-Type: application/json" \
     -d '{"key":"example"}' \
     http://localhost:8080/kv
```
```
