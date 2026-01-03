# FastAPI Routing Basics

This file demonstrates how to define endpoints (routes) in FastAPI, including path parameters and different parameter types.

## Setup

```python
from fastapi import FastAPI
app = FastAPI()
```

Creates the FastAPI application instance. Every route is registered on this `app` object using a decorator like `@app.get(...)` or `@app.post(...)`.

## The commented-out examples

### 1. Basic GET route
```python
@app.get("/")
def main():
    return {"Message": "hello world"}
```
A GET request to `/` (the root URL) returns a simple JSON message. No parameters involved.

### 2. Route with an integer path parameter
```python
@app.get('/{id}')
def main(id: int):
    return {"kfmem": "mmeom"}
```
`{id}` in the path is a **path parameter**. Declaring the function argument as `id: int` tells FastAPI to automatically convert the URL segment to an integer, and to reject the request with a 422 error if it isn't one (e.g. `/5` works, `/abc` fails).

### 3. Basic POST route
```python
@app.post('/post')
async def main():
    return {}
```
Handles POST requests to `/post`. Defined as `async def`, so FastAPI runs it directly in the event loop rather than in a thread pool — useful once you start doing `await`-based work like database calls.

### 4. Path parameter with `:path` converter
```python
@app.get("/path/{id:path}")
async def main1(id: str):
    return {"msg": id}
```
The `:path` converter tells FastAPI that `id` can contain **slashes**, not just a single URL segment. So `/path/a/b/c` is valid and `id` will be `"a/b/c"`. Without `:path`, a `/` in the URL would look like a different, unmatched route.

### 5. Plain integer path parameter (again)
```python
@app.get('/path/{id}')
async def main2(id: int):
    return {"msg": "second"}
```
Same idea as example 2, just async and under `/path/`. Note: since example 4 (`/path/{id:path}`) is commented out here, if both were active, FastAPI matches routes in the order they're declared — the more general `:path` route could shadow this one for multi-segment URLs.

## The active endpoint

```python
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file": file_path}
```

This is the only route currently enabled. It:
- Listens for GET requests under `/files/...`
- Uses the `:path` converter so `file_path` can include slashes — e.g. a request to `/files/docs/notes/todo.txt` gives `file_path = "docs/notes/todo.txt"`
- Returns the captured path back as JSON: `{"file": "docs/notes/todo.txt"}`

This pattern is commonly used as a starting point for endpoints that serve or look up files by their relative path.

## Key takeaways

| Concept | What it does |
|---|---|
| `@app.get(...)` / `@app.post(...)` | Registers a route for that HTTP method |
| `{name}` in path | Path parameter — captured from the URL |
| `id: int` | Type hint = automatic validation & conversion |
| `{name:path}` | Allows the captured value to contain `/` |
| `async def` | Endpoint runs directly on the event loop (good for `await`-based I/O) |
| `def` (sync) | FastAPI runs it in a thread pool automatically |

---

# Predefined Values with Enum

```python
from fastapi import FastAPI
from enum import Enum
app = FastAPI()

class ProductCategory(str, Enum):
    book = "book"
    clothing = "clothing"
```

Sometimes a path parameter should only accept a fixed set of values (not any string or number). FastAPI supports this by using a Python `Enum`.

- `ProductCategory(str, Enum)` creates an enum where each member is also a `str`. Inheriting from `str` matters — it lets FastAPI serialize the value directly to JSON and compare it naturally to plain strings.
- `book = "book"` and `clothing = "clothing"` define the only two valid values. Any other value sent in the URL will cause FastAPI to automatically return a 422 validation error — you don't have to check it manually.

### Route 1 — just echoing the category
```python
@app.get('/{category}')
async def main(category: ProductCategory):
    return {"respone": "hello", "category": category}
```
Because the parameter is typed as `ProductCategory`, only `/book` or `/clothing` will match successfully. Something like `/shoes` gets rejected before your function body even runs. This also means this route "catches" any single-segment path that happens to be `book` or `clothing` — worth watching for collisions with other single-segment routes like `/{id}` from your earlier file.

### Route 2 — branching on the category value
```python
@app.get("/producut/{category}")
async def main2(category: ProductCategory):
    if category == ProductCategory.book:
        return {"category": category, "msg": "Books are awesome!"}
    elif category == ProductCategory.clothing.value:
        return {"category": category, "msg": "category are awesome!"}
    else:
        return {"category": category, "msg": "Unknown category!"}
```
This shows two equally valid ways to compare an enum member:
- `category == ProductCategory.book` compares against the enum member directly.
- `category == ProductCategory.clothing.value` compares against the plain string `"clothing"` (`.value` unwraps the enum to its underlying string). This works here specifically because `ProductCategory` inherits from `str`.

The `else` branch is actually **unreachable** — since `category` is validated as a `ProductCategory` by FastAPI before the function runs, it can only ever be `book` or `clothing`. There's no third option that could trigger "Unknown category!". It's harmless to leave in as a safety net, but it will never fire with the current enum.

**Small naming notes** (not bugs, just typos worth knowing about since they'll show up in your URLs/code):
- `caterogy` → `category` (parameter name, only in the first route)
- `producut` → `product` (the URL path)
- `respone` → `response` (the JSON key)

---

# CRUD Operations (Create, Read, Update, Delete)

```python
products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "description": "High performance", "category": "Electronics"},
    {"id": 2, "name": "Smartphone", "price": 499.99, "description": "Latest model", "category": "Electronics"},
    {"id": 3, "name": "Coffee Maker", "price": 49.99, "category": "Appliances"},
]
```
A plain Python list acting as an in-memory "database" — it resets every time the server restarts. This is the standard way to prototype CRUD logic before wiring up a real database.

### GET all — Read
```python
@app.get('/product')
async def gat_all_product():
    return products_db
```
Returns the entire list as-is.

### GET one — Read by ID
```python
@app.get('/product/{id}')
async def get_product_id(id: int):
    for product in products_db:
        if product['id'] == id:
            return product
    return {}
```
Loops through the list looking for a matching `id`. Returns `{}` if nothing matches — in a production API you'd normally raise a proper 404 (`HTTPException(status_code=404)`) instead of silently returning an empty object, so the client can tell "not found" apart from "found an empty product".

### POST — Create
```python
@app.post('/products')
async def created_at(new_product: dict):
    products_db.append(new_product)
    return products_db
```
Accepts any JSON object as the request body (typed loosely as `dict`) and appends it to the list, then returns the whole updated list. Note nothing here checks that `new_product` actually has an `id`, or that the `id` isn't already taken — a stricter version would use a Pydantic model to validate shape and auto-generate the `id`.

### PUT — Full update
```python
@app.put('/product/{prodcut_id}')
async def put(product_id: int, new_product: dict):
    for idx, pro in enumerate(products_db):
        if pro['id'] == product_id:
            products_db[idx] = new_product
            return {"status": "new_productupadeted", "product_id": product_id, "new_product": pro}
```
**This route has a real bug**, not just a typo: the path declares `{prodcut_id}` but the function parameter is named `product_id`. FastAPI matches path parameters to function arguments **by name**, so this mismatch means:
- `product_id` is *not* filled from the URL — FastAPI instead treats it as a required **query parameter** (`/product/5?product_id=5`)
- Calling `/product/5` alone will fail with a 422 error ("field required: product_id"), since neither the path segment nor a query param supplies it correctly

Fix: rename either the path placeholder or the function argument so they match, e.g. `@app.put('/product/{product_id}')`.

Also worth noting: `new_product` fully replaces the existing entry (`products_db[idx] = new_product`), so any fields you don't include in the request body will be lost — that's expected behavior for PUT (full replace), as opposed to PATCH (partial update) below. There's also no `else`/fallback if no match is found, so a nonexistent `product_id` silently returns nothing (`None`).

### PATCH — Partial update
```python
@app.patch('/product_id/{prodcut_id}')
async def patch(product_id: int, new_product: dict):
    for pro in products_db:
        if pro["id"] == product_id:
            pro.update(new_product)
            return {"status": "updated", "product_id": product_id, "new_product": pro}
```
Same `prodcut_id` vs `product_id` name-mismatch bug as PUT above. There's an additional issue: the path is `/product_id/{prodcut_id}` — the literal segment is `product_id`, not `product`. So this endpoint actually lives at a URL like `/product_id/5`, not the more natural `/product/5` used by the other routes. That's likely accidental (probably meant to be `/product/{product_id}`).

The update logic itself (`pro.update(new_product)`) is correct for a partial update — it merges the new fields into the existing dict rather than replacing it.

### DELETE — Remove
```python
@app.delete('/product/{prodcut_id}')
async def delete(product_id: int):
    for idx, pro in enumerate(products_db):
        if pro['id'] == product_id:
            products_db.pop(idx)
            return {"status": "delted", "product_id": product_id, "new_product": pro}
```
Same `prodcut_id`/`product_id` mismatch again — fix it the same way (make the path placeholder and function argument match). Functionally, once fixed, this removes the matching product by index and returns confirmation, including the deleted item's original data (captured in `pro` before `.pop()` — `pop(idx)` removes and returns the item, but here the code reads `pro`, the loop variable, rather than the popped value, which happens to hold the same data so it still works).

## Summary of bugs to fix

| Route | Issue |
|---|---|
| PUT `/product/{prodcut_id}` | Path placeholder `prodcut_id` ≠ function arg `product_id` → breaks path-parameter binding |
| PATCH `/product_id/{prodcut_id}` | Same name mismatch, **plus** literal path segment is `product_id` instead of `product` |
| DELETE `/product/{prodcut_id}` | Same name mismatch as PUT |
| GET by ID | Returns `{}` instead of a proper 404 when not found |
| POST | No validation that `new_product` has a valid/unique `id` |

Small spelling notes (harmless, but good to standardize): `gat_all_product` → `get_all_products`, `delted` → `deleted`, `new_productupadeted` → `product_updated`.

## Try it out

Run the app with:
```bash
uvicorn main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for FastAPI's auto-generated interactive API docs (Swagger UI), where you can test the `/files/{file_path}` endpoint directly.