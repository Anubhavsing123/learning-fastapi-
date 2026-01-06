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

---

# Query Parameters

Unlike path parameters (`{name}` in the URL path), **query parameters** are the `?key=value` pairs after the `?` in a URL. In FastAPI, any function argument that is *not* part of the path automatically becomes a query parameter.

### 1. Single required query parameter
```python
@app.get("/item")
async def main1(category: str):
    return {"status": "OK", "category": category}
```
Since `category` isn't in the path (`/item` has no `{category}`), FastAPI treats it as a required query parameter. Call it as `/item?category=books`. Omitting it returns a 422 error.

### 2. Optional query parameter (with a default)
```python
@app.get("/items/")
def get_items(limit: int = 10):
    return {"limit": limit}
```
Giving `limit` a default value (`= 10`) makes it optional. `/items/` returns `{"limit": 10}`; `/items/?limit=5` returns `{"limit": 5}`.

### 3. Multiple query parameters
```python
@app.get("/items/")
async def get_items(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}
```
Just add more typed arguments with defaults. Both become independent, optional query params: `/items/?limit=20&skip=40`. This is the classic pattern for pagination.

### 4. Boolean query parameter
```python
@app.get("items/")
async def get_item(active: bool = True):
    return {"active": active}
```
FastAPI is lenient about how booleans are written in the URL — `?active=true`, `?active=1`, `?active=yes` are all accepted and converted to Python's `True`/`False`. (Small typo here: the path is missing its leading slash — `"items/"` should be `"/items/"`, or requests to it will fail to route as expected.)

### 5. List query parameter — the active example
```python
from fastapi import FastAPI, Query
from typing import List

@app.get("/items/{year}")
async def get_items(year: str, tags: List[str] = Query([])):
    return {"tags": tags}
```
This combines a **path parameter** (`year`) with a **repeatable query parameter** (`tags`):
- `year` comes from the URL path, e.g. `/items/2024`
- `tags` is typed as `List[str]` with a default empty list, wrapped in `Query([])`. This lets the same query key be repeated to build a list: `/items/2024?tags=sale&tags=new&tags=featured` produces `tags = ["sale", "new", "featured"]`
- The `Query(...)` wrapper is what makes FastAPI aware this is a query parameter with special handling (repeatable values); it also supports extra validation like `Query(..., min_length=1)` if you want to require at least one value

Note the function returns only `{"tags": tags}` — `year` is accepted and validated but never included in the response, so it's effectively unused right now (likely intentional while testing, but worth returning it too if you want to confirm it's being read correctly, e.g. `{"year": year, "tags": tags}`).

## Query vs. Path parameters — quick reference

| | Path parameter | Query parameter |
|---|---|---|
| Where | Part of the URL path, e.g. `/items/{id}` | After `?`, e.g. `/items?limit=10` |
| Required? | Always required (part of the route) | Optional if given a default value |
| Declared how | Must appear in `{}` in the decorator path | Any function arg not in the path |
| Good for | Identifying a specific resource (an ID) | Filtering, pagination, sorting, options |

---

# Query Parameters

Unlike path parameters (`{id}` in the URL path itself), **query parameters** come after a `?` in the URL, like `/items?limit=10&skip=0`. In FastAPI, any function argument that isn't declared as part of the path automatically becomes a query parameter.

### Single query parameter
```python
@app.get("/item")
async def main1(category: str):
    return {"status": "OK", "category": category}
```
Since `category` isn't in the path (`/item`), FastAPI treats it as a **required** query parameter. Call it as `/item?category=books`. Omitting it returns a 422 error.

### Optional query parameter (with a default)
```python
@app.get("/items/")
def get_items(limit: int = 10):
    return {"limit": limit}
```
Giving `limit` a default value (`= 10`) makes it optional. `/items/` returns `{"limit": 10}`; `/items/?limit=5` returns `{"limit": 5}`. FastAPI still validates the type — `/items/?limit=abc` fails validation.

### Multiple query parameters
```python
@app.get("/items/")
async def get_items(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}
```
Just add more arguments with defaults. Both are independent and optional: `/items/?limit=5&skip=2`. This `limit`/`skip` pair is the standard pattern for pagination.

### Boolean query parameter
```python
@app.get("items/")
async def get_item(active: bool = True):
    return {"active": active}
```
FastAPI is flexible about how booleans are written in the URL — `?active=true`, `?active=1`, `?active=yes`, and `?active=on` (and their opposites) all work.
(Small typo to note: the path is `"items/"` without a leading `/`, which FastAPI will still register, but by convention every route path should start with `/` — e.g. `"/items/"`.)

### List query parameter (the active example)
```python
from fastapi import FastAPI, Query
from typing import List

@app.get("/items/{year}")
async def get_items(year: str, tags: List[str] = Query([])):
    return {"tags": tags}
```
This is the only endpoint currently active. It combines a **path parameter** with a **list-typed query parameter**:
- `year` comes from the URL path — e.g. `/items/2024`
- `tags` is a query parameter that can be repeated to build a list: `/items/2024?tags=sale&tags=new&tags=featured` produces `tags = ["sale", "new", "featured"]`
- `Query([])` sets the default to an empty list when no `tags` are given, so `/items/2024` alone returns `{"tags": []}`

You need `Query(...)` (imported from `fastapi`) specifically to give a list-typed parameter a default value — just writing `tags: List[str] = []` would work too in modern FastAPI, but wrapping it in `Query()` is the more explicit, traditional way, and it also lets you add validation like `Query(..., min_length=1)` or a description for the auto-generated docs.

Note that `year` is declared, and returned in the response — since only `tags` is returned in this version. If you want `year` reflected back too, add it to the return dict: `return {"year": year, "tags": tags}`.

---

# Query Parameters

```python
from fastapi import FastAPI, Query
from typing import List
app = FastAPI()
```

Unlike path parameters (`{id}` in the URL path itself), **query parameters** are the `?key=value` pairs that come after a `?` in a URL — e.g. `/items?limit=5&skip=10`. In FastAPI, any function argument that is **not** part of the path is automatically treated as a query parameter.

### 1. Single required query parameter
```python
@app.get("/item")
async def main1(category: str):
    return {"status": "OK", "category": category}
```
Since `category` isn't in the path (`/item`), FastAPI treats it as a query parameter. Because it has no default value, it's **required** — a request must look like `/item?category=books`, or FastAPI returns a 422 error.

### 2. Optional query parameter (with a default)
```python
@app.get("/items/")
def get_items(limit: int = 10):
    return {"limit": limit}
```
Giving `limit` a default value (`= 10`) makes it **optional**. `/items/` returns `{"limit": 10}`, while `/items/?limit=25` returns `{"limit": 25}`.

### 3. Multiple query parameters
```python
@app.get("/items/")
async def get_items(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}
```
Just declare more arguments — each becomes its own query parameter. This is the standard pattern for pagination: `/items/?limit=20&skip=40`.

### 4. Boolean query parameter
```python
@app.get("items/")
async def get_item(active: bool = True):
    return {"active": active}
```
FastAPI is flexible about how booleans are written in the URL — `?active=true`, `?active=1`, `?active=yes`, and `?active=on` (and their opposites) all get parsed correctly into Python `True`/`False`.
(Small note: this route's decorator is `"items/"` without a leading `/` — FastAPI will still register it, but it's inconsistent with the other routes, which all start with `/`.)

### 5. List query parameter — the active endpoint
```python
@app.get("/items/{year}")
async def get_items(year: str, tags: List[str] = Query([])):
    return {"tags": tags}
```
This combines a **path parameter** (`year`) with a **query parameter that accepts multiple values** (`tags`).

- `year: str` comes from the URL path, e.g. `/items/2024`.
- `tags: List[str] = Query([])` means `tags` is a query parameter that can be repeated — the client sends it as `?tags=sale&tags=new&tags=featured`, and FastAPI collects all of them into a Python list: `["sale", "new", "featured"]`.
- The default `Query([])` means `tags` is optional; if omitted, it defaults to an empty list.

Example request:
```
GET /items/2024?tags=sale&tags=new
```
Response:
```json
{"tags": ["sale", "new"]}
```
Note the response only returns `tags` — `year` is captured by the function but never included in the returned JSON, so a caller can't see which year they queried from the response alone. You'd likely want to add `"year": year` to the returned dict.

## Query parameters vs. path parameters — quick contrast

| | Path parameter | Query parameter |
|---|---|---|
| Where it appears | Part of the URL path: `/items/{id}` | After `?`: `/items?limit=10` |
| Declared how | Must appear in `{}` in the `@app.get(...)` path | Any function arg not in the path |
| Required by default? | Yes | Only if it has no default value |
| Good for | Identifying a specific resource (e.g. an ID) | Filtering, pagination, options, repeated values |

---

# Query Parameter Validation — Revision Notes

Quick bullet-point summary for revision (progression from basic to advanced):

- **`status_code` on a route**: `@app.get("/item", status_code=status.HTTP_202_ACCEPTED)` — sets the default HTTP response status code for that endpoint.

- **Basic optional query param**: `se: str | None = None` — plain optional param, no validation, just a `None` check in the function body.

- **Validation without `Annotated`**: `se: str | None = Query(default=None, max_length=5)` — pass constraints directly as the default value via `Query(...)`. Works, but mixes "default value" and "metadata" into one place — not the recommended style in modern FastAPI.

- **Validation with `Annotated` (preferred style)**: `se: Annotated[str | None, Query(max_length=5)] = None` — type and validation metadata (`Query(...)`) are separated from the actual default (`= None`). This is the modern recommended pattern.

- **`min_length` + `pattern`**: `Query(min_length=5, pattern="^[a-z]+$")` — enforce minimum length and a regex the value must match (here: lowercase letters only).

- **Multiple values / list query param**: `se: Annotated[List[str] | None, Query(max_length=5)] = None` — lets the client send `?se=a&se=b`; `max_length` here limits the string length of *each* item (not the list length, easy to mix up).

- **`alias`**: `Query(min_length=5, alias="q")` — lets the URL use a different name (`?q=laptop`) than the Python variable name (`se`). Common when you want a short/clean URL param but a descriptive variable internally.

- **`title` / `description`**: pure documentation metadata — shown in the auto-generated `/docs` (Swagger UI), no effect on runtime behavior or validation.

- **`deprecated=True`**: marks the parameter as deprecated in `/docs` (shown with a strike-through/warning), signaling to API consumers it may be removed later — doesn't block the parameter from still working.

- **Duplicate `@app.get("/product")` routes**: multiple functions are decorated with the same path in this file (several commented out, two active with the same name `product`). Only the **last** defined route for a given path+method actually gets registered — earlier ones with the same path are effectively overridden/unreachable. Worth cleaning up so only one active `/product` route remains.

- **Custom validation with `AfterValidator`**:
  ```python
  def check_vali(id: str):
      if not id.startswith('prod-'):
          raise ValueError('ID must start with "prod-"')
      return id

  @app.get('/item')
  async def item(id: Annotated[str | None, AfterValidator(check_vali)] = None):
  ```
  - `AfterValidator` runs your own function *after* FastAPI's built-in type validation succeeds.
  - Raising `ValueError` inside it automatically becomes a 422 response — no manual error handling needed.
  - Must **return** the validated value (`return id`) — if you don't return anything, the parameter becomes `None` even when validation passes.

---

# Query Parameter Validation

```python
from fastapi import FastAPI, status, Query
from typing import Annotated, List
from pydantic import AfterValidator
```

This file builds up the same `/product` search endpoint step by step, each version adding one more layer of validation on top of the query parameter `se`. Only the **last** definition of a route actually runs — FastAPI uses whichever `@app.get("/product")` function was defined last in the file, so all the earlier commented-out versions are the "history" of how the endpoint evolved.

### The progression

1. **No validation** — `se: str | None = None`. Just an optional string, no rules on its content.
2. **Validation without `Annotated`** — `se: str | None = Query(default=None, max_length=5)`. The default value and the validation rule are combined inside `Query(...)` and assigned directly to the parameter.
3. **Validation with `Annotated`** — `se: Annotated[str | None, Query(max_length=5)] = None`. `Annotated` separates the *type* (`str | None`) from the *metadata/validation* (`Query(...)`), with the actual default moved outside to `= None`. This is the style FastAPI's docs now recommend, since it keeps typing tools happier and separates "what type is this" from "how should FastAPI validate/document it".
4. **Regex pattern** — adds `min_length=5, pattern="^[a-z]+$"` inside `Query(...)`, restricting input to 5+ lowercase letters only.
5. **Multiple values (list)** — `se: Annotated[List[str] | None, Query(max_length=5)] = None`. Lets the client send `?se=phone&se=laptop`, collected into a list, then checks each search term against each product.
6. **Alias** — `Query(min_length=5, alias="q")`. The client must use `?q=...` in the URL, while the Python variable stays named `se` internally. Useful when you want a short/different public parameter name than your internal variable name.
7. **Metadata (`title`, `description`)** — purely cosmetic; these don't affect validation, they show up in the auto-generated docs at `/docs` to describe the parameter for API consumers.
8. **Deprecated** — `deprecated=True` (the version that's actually active). Marks the parameter as deprecated in the `/docs` UI (usually shown struck-through), signaling to API consumers they should stop using it, without breaking anything for those still passing it.

### Active endpoint
```python
@app.get("/product")
async def product(
    se: Annotated[
        str | None,
        Query(min_length=5, alias="q", title="Search Item",
              description="About the product detail", deprecated=True)
    ] = None
):
    ...
```
So right now, searching products requires calling `/product?q=laptop` (not `?se=laptop`, because of the `alias`), the search term must be at least 5 characters, and `/docs` will flag `q` as deprecated.

### Custom validation with `AfterValidator`
```python
def check_vali(id: str):
    if not id.startswith('prod-'):
        raise ValueError('ID must start with "prod-"')
    return id

@app.get('/item')
async def item(id: Annotated[str | None, AfterValidator(check_vali)] = None):
    if id:
        return {id: "id", "msg": "vlid id"}
    return {"msg": "not valid id"}
```
`AfterValidator` lets you plug a plain Python function in as a validation step, run *after* FastAPI's normal type checking. Here, `check_vali` rejects any `id` that doesn't start with `"prod-"` by raising a `ValueError` — FastAPI turns that into a 422 response automatically. This is useful for validation logic too specific for `Query(...)`'s built-in options (`min_length`, `pattern`, etc.).

Small bug to note: the response `{id: "id", "msg": "vlid id"}` uses the *value* of `id` as the dictionary **key**, with the string `"id"` as its value — almost certainly backwards from the intent. It likely should be `{"id": id, "msg": "valid id"}`.

## Revision summary table

| # | Feature | Implemented in | What it does |
|---|---|---|---|
| 1 | Basic optional query param | `/product` (v1, commented) | `se: str \| None = None` — no validation |
| 2 | `Query()` without `Annotated` | `/product` (v2, commented) | `se: str \| None = Query(default=None, max_length=5)` |
| 3 | `Query()` with `Annotated` | `/product` (v3, commented) | `Annotated[str \| None, Query(max_length=5)] = None` |
| 4 | Regex/length validation | `/product` (v4, commented) | `Query(min_length=5, pattern="^[a-z]+$")` |
| 5 | Multiple/list values | `/product` (v5, commented) | `Annotated[List[str] \| None, Query(max_length=5)]` — repeat `?se=` |
| 6 | Alias | `/product` (v6, commented) | `Query(alias="q")` — public name `q`, internal name `se` |
| 7 | Metadata for docs | `/product` (v7, commented) | `title`, `description` shown in `/docs` |
| 8 | Deprecated flag | `/product` (**active**) | `deprecated=True` — flags param as deprecated in `/docs` |
| 9 | Custom validator function | `/item` (**active**) | `AfterValidator(check_vali)` — enforces `id` starts with `"prod-"` |

---

# Path Parameter Validation

```python
from fastapi import FastAPI, Path, Query
from typing import Annotated
```

`Path` is the path-parameter equivalent of `Query` — it lets you attach validation rules and documentation metadata to a path parameter, the same way `Query` does for query parameters. This file builds the idea up in stages (all but the last are commented out).

### The progression

1. **No validation**
```python
@app.get("/item/{product_id}")
async def get_allproduct(product_id: int):
    for pro in products_db:
        if pro["id"] == product_id:
            return pro
        return {"error": "not found"}
```
Just a typed path parameter — any integer is accepted. **Bug here:** `return {"error": "not found"}` sits *inside* the `if` block's `else`-less body at the wrong indentation level — it actually runs on the very first loop iteration whenever `pro["id"] != product_id`, so if `product_id=3`, the loop checks product 1, immediately returns `"not found"`, and never even reaches product 3. It should be outside/after the `for` loop.

2. **Numeric range validation**
```python
async def get_allproduct(product_id: Annotated[int, Path(ge=1, le=3)]):
```
`ge=1, le=3` means "greater than or equal to 1, less than or equal to 3." Requests like `/item/0` or `/item/10` are rejected with a 422 before the function body runs. (This version also fixes the indentation bug from step 1 by moving the `return {"error": "not found"}` outside the loop.)

3. **Adding metadata**
```python
Path(ge=1, le=3, title="this is new product line", description="this is new product line")
```
`title`/`description` are purely for the auto-generated `/docs` page — same idea as with `Query`, no effect on validation.

4. **Combining path and query parameters**
```python
@app.get("/item/{product_id}")
async def get_allproduct(
    product_id: Annotated[int, Path(ge=1, le=3, title="This is product ID",
                                     description="Product ID must be between 1 and 3")],
    search_id: Annotated[str | None, Query(min_length=5, alias="q", title="Search Item",
                                            description="About the product detail",
                                            deprecated=True)] = None
):
    for pro in products_db:
        if pro["id"] == product_id:
            if search_id:
                if search_id.lower() in pro["name"].lower():
                    return pro
                return {"message": "Search not matched"}
            return pro
    return {"error": "Product not found"}
```
This shows a route using both kinds of parameter together: `product_id` (required, validated path param, 1–3 only) and `search_id` (optional, validated query param, aliased to `q`). If a product matching `product_id` is found, and `search_id` was also given, it further checks whether the search term appears in that product's name — a kind of "find by ID, then confirm by name" filter.

### Active endpoint
```python
from fastapi import FastAPI, Path
app = FastAPI()

@app.get("/products/{product_id}")
async def get_product(
    product_id: int = Path(
        title="Product ID",
        description="Unique product ID",
        example=101,
        gt=0,
        le=1000
    )
):
    return {"product_id": product_id}
```
The currently active route. Differences from the earlier drafts:
- Uses `Path(...)` assigned directly to `product_id` (not wrapped in `Annotated`) — both styles work; `Annotated` is the newer, more type-checker-friendly convention, but this direct-assignment style is still fully valid FastAPI.
- `gt=0, le=1000` = "greater than 0, up to and including 1000" (a wider, more realistic ID range than the earlier `ge=1, le=3`).
- `example=101` adds a sample value shown in the `/docs` UI — purely illustrative, doesn't affect validation.
- This version doesn't look anything up in `products_db` (it's not even defined in this file) — it just echoes the validated `product_id` back.

## Revision summary table

| # | Feature | Implemented in | What it does |
|---|---|---|---|
| 1 | Plain path param, no validation | `/item/{product_id}` (v1, commented) | `product_id: int` — accepts any integer; has an indentation bug |
| 2 | Numeric range (`ge`, `le`) | `/item/{product_id}` (v2, commented) | `Path(ge=1, le=3)` — restricts to 1–3 |
| 3 | Metadata (`title`, `description`) | `/item/{product_id}` (v3, commented) | Docs-only, no validation effect |
| 4 | Path + Query combined | `/item/{product_id}` (v4, commented) | `product_id` (Path, 1–3) + `search_id` (Query, aliased `q`, deprecated) |
| 5 | `Path()` direct assignment, wider range, `example` | `/products/{product_id}` (**active**) | `Path(gt=0, le=1000, example=101)` — no `Annotated`, no DB lookup |

## Try it out

Run the app with:
```bash
uvicorn main:app --reload
```

Then visit `http://127.0.0.1:8000/docs` for FastAPI's auto-generated interactive API docs (Swagger UI), where you can test the `/files/{file_path}` endpoint directly.