# FastAPI

FastAPI is a modern Python web framework for building APIs.
It’s designed around:

- **Type hints** (Pydantic models + validation)
- **Automatic OpenAPI/Swagger docs**
- **High performance** (ASGI)

This folder contains a small, runnable demo app that covers common FastAPI features.

## Install

```powershell
pip install fastapi uvicorn
```

## Run

From this directory:

```powershell
uvicorn main:app --reload
```

Then open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## What the demo covers

- `GET /` basic route
- Path params: `GET /items/{item_id}`
- Query params: `GET /search?q=...&limit=...`
- Request body validation with Pydantic: `POST /items`
- Response models and status codes
- Headers + cookies
- Simple dependency injection (`Depends`)
- Custom exception + error response

## Quick test examples (PowerShell)

```powershell
Invoke-RestMethod http://127.0.0.1:8000/

Invoke-RestMethod "http://127.0.0.1:8000/items/123?details=true"

Invoke-RestMethod "http://127.0.0.1:8000/search?q=asic&limit=2"

Invoke-RestMethod http://127.0.0.1:8000/items -Method Post -ContentType 'application/json' -Body '{"name":"widget","price":9.99,"tags":["demo"]}'
```

## Notes

- `--reload` is great for dev (auto-restart on file changes).
- In production you typically run behind a process manager and might use multiple workers.
