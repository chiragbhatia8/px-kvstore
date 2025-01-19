# API Documentation for Python-based Key-Value Store

This document outlines the API endpoints available in the Python-based Key-Value Store application. Each endpoint allows you to interact with the key-value store for creating, retrieving, updating, and deleting key-value pairs.

## Base URL

The base URL for the API is:
```
http://localhost:8080
```

## Endpoints

### 1. Create or Update a Key-Value Pair

- **HTTP Method**: `PUT`
- **Endpoint**: `/kv`
- **Request Body**:
  ```json
  {
    "key": "someKey",
    "value": "someValue"
  }
  ```
- **Description**: This endpoint creates a new key-value pair or updates an existing one. The request body must contain both a `key` and a `value`.

- **Responses**:
  - **200 OK**: Successfully created or updated the key-value pair.
    ```json
    {
      "someKey": "someValue"
    }
    ```
  - **400 Bad Request**: If the request body is missing the `value` field.
    ```json
    {
      "error": "Missing value"
    }
    ```

### 2. Retrieve a Single Key-Value Pair

- **HTTP Method**: `GET`
- **Endpoint**: `/kv?key=someKey`
- **Query Parameters**:
  - `key`: The key of the value to retrieve.

- **Description**: This endpoint retrieves the value associated with the specified key.

- **Responses**:
  - **200 OK**: Successfully retrieved the key-value pair.
    ```json
    {
      "someKey": "someValue"
    }
    ```
  - **404 Not Found**: If the specified key does not exist.
    ```json
    {
      "error": "Key not found"
    }
    ```

### 3. Retrieve All Key-Value Pairs

- **HTTP Method**: `GET`
- **Endpoint**: `/kv`
- **Description**: This endpoint retrieves all key-value pairs stored in the key-value store.

- **Responses**:
  - **200 OK**: Successfully retrieved all key-value pairs.
    ```json
    {
      "key1": "value1",
      "key2": "value2"
    }
    ```

### 4. Delete a Key-Value Pair

- **HTTP Method**: `DELETE`
- **Endpoint**: `/kv`
- **Request Body**:
  ```json
  {
    "key": "someKey"
  }
  ```
- **Description**: This endpoint removes the specified key and its associated value from the store.

- **Responses**:
  - **200 OK**: Successfully deleted the key-value pair.
    ```json
    {
      "message": "Key deleted"
    }
    ```
  - **404 Not Found**: If the specified key does not exist.
    ```json
    {
      "error": "Key not found"
    }
    ```

## Error Handling

The API returns standard HTTP status codes to indicate the success or failure of a request. Common error responses include:

- **400 Bad Request**: Indicates that the request was malformed or missing required fields.
- **404 Not Found**: Indicates that the requested resource (key) does not exist.

## Example Usage with curl

### PUT a Key-Value Pair
```bash
curl -X PUT -H "Content-Type: application/json" \
  -d '{"key":"foo","value":"bar"}' \
  http://localhost:8080/kv
```

### GET a Single Key
```bash
curl "http://localhost:8080/kv?key=foo"
```

### GET All Keys
```bash
curl http://localhost:8080/kv
```

### DELETE a Key
```bash
curl -X DELETE -H "Content-Type: application/json" \
  -d '{"key":"foo"}' \
  http://localhost:8080/kv
```

## Conclusion

This API provides a simple interface for managing key-value pairs in a Python-based key-value store. For further details or specific use cases, please refer to the source code or additional documentation.