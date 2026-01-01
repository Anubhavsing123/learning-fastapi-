# Chapter 1 — FastAPI Basics 🚀

## How to Make Endpoints

First, import `FastAPI` and create an application instance:

```python
from fastapi import FastAPI

app = FastAPI()
```

`app` is the main FastAPI application object.

---

## 1. Basic GET Endpoint

```python
@app.get("/")
def main():
    return {"message": "Hello World"}
```

Here:

```text
@app.get("/")     → GET request
"/"               → URL path
main()            → Path operation function
return {...}      → JSON response
```

Open:

```text
http://127.0.0.1:8000/
```

Response:

```json
{
    "message": "Hello World"
}
```

---

## 2. Path Parameter

We can pass values directly through the URL.

```python
@app.get("/{id}")
def main(id: int):
    return {"id": id}
```

Example request:

```text
GET /10
```

Response:

```json
{
    "id": 10
}
```

Here:

```text
/{id}
  │
  └── Path Parameter
```

FastAPI takes `10` from the URL and passes it to:

```python
id: int
```

Because we specified `int`, FastAPI validates that the value is an integer.

For example:

```text
GET /hello
```

will produce a validation error because `hello` cannot be converted to an integer.

---

## 3. POST Endpoint

A POST endpoint is normally used to create data.

```python
@app.post("/post")
async def main():
    return {}
```

Request:

```text
POST /post
```

Response:

```json
{}
```

FastAPI supports both normal functions:

```python
def main():
    ...
```

and asynchronous functions:

```python
async def main():
    ...
```

---

# Path Convertors

FastAPI allows us to capture complete paths using the `path` convertor.

## 4. Path Convertor

```python
@app.get("/path/{id:path}")
async def main1(id: str):
    return {"msg": id}
```

The syntax is:

```text
{id:path}
 │   │
 │   └── path convertor
 │
 └── parameter name
```

Unlike a normal path parameter, `path` can contain `/`.

For example:

```text
GET /path/hello/world/python
```

FastAPI captures:

```text
id = "hello/world/python"
```

Response:

```json
{
    "msg": "hello/world/python"
}
```

---

## Normal Path Parameter vs Path Convertor

Normal parameter:

```python
@app.get("/path/{id}")
async def main2(id: int):
    return {"msg": "second"}
```

Example:

```text
/path/10
```

Here `id` captures only one path segment.

But:

```text
/path/10/20
```

doesn't match that route.

With:

```python
@app.get("/path/{id:path}")
```

this works:

```text
/path/10/20
```

and:

```text
id = "10/20"
```

---

# 5. File Path Example

Your current endpoint:

```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file": file_path}
```

Here `file_path` uses the `path` convertor.

Example:

```text
GET /files/images/profile/user.png
```

FastAPI captures:

```text
file_path = "images/profile/user.png"
```

Response:

```json
{
    "file": "images/profile/user.png"
}
```

So the request flow is:

```text
GET /files/images/profile/user.png
              │
              ▼
@app.get("/files/{file_path:path}")
              │
              ▼
file_path = "images/profile/user.png"
              │
              ▼
read_file(file_path)
              │
              ▼
{"file": "images/profile/user.png"}
```

---

# Endpoint Syntax

The general FastAPI endpoint syntax is:

```python
@app.http_method("/path")
def function_name():
    return response
```

For example:

```python
@app.get("/users")
def get_users():
    return {"users": []}
```

The main HTTP methods are:

| Method | FastAPI | Purpose |
|---|---|---|
| GET | `@app.get()` | Read data |
| POST | `@app.post()` | Create data |
| PUT | `@app.put()` | Replace/update data |
| PATCH | `@app.patch()` | Partially update data |
| DELETE | `@app.delete()` | Delete data |

---

# Complete Chapter Code

```python
from fastapi import FastAPI

app = FastAPI()


# Basic endpoint
@app.get("/")
def main():
    return {"Message": "hello world"}


# Integer path parameter
@app.get("/{id}")
def get_by_id(id: int):
    return {"id": id}


# POST endpoint
@app.post("/post")
async def create_post():
    return {}


# Capture an entire path
@app.get("/path/{id:path}")
async def get_path(id: str):
    return {"msg": id}


# File path example
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file": file_path}
```

## Key Points

- `@app.get()` creates a GET endpoint.
- `@app.post()` creates a POST endpoint.
- `{id}` creates a path parameter.
- `id: int` tells FastAPI to validate `id` as an integer.
- `{file_path:path}` captures multiple URL path segments, including `/`.
- `def` and `async def` can both be used for path operation functions.
- Returning a Python dictionary normally produces a JSON response.