# python-dotenv (import name: `dotenv`)

`python-dotenv` loads environment variables from a `.env` file into `os.environ`.
That lets you keep configuration (API keys, passwords, feature flags) out of your code and out of git.

## Install

```powershell
pip install python-dotenv
```

## Core ideas

- **Environment variables** live in the process environment (`os.environ`).
- A **`.env` file** is just key/value lines, for example:

  ```env
  API_KEY=abc123
  DEBUG=true
  TIMEOUT_SECONDS=15
  # Quotes are allowed
  GREETING="hello world"
  ```

- `load_dotenv()` reads that file and sets variables in the process.

## Common patterns

### 1) Load `.env` at startup

```python
from dotenv import load_dotenv
load_dotenv()  # loads .env from current working dir (or finds it with find_dotenv)
```

Then read values:

```python
import os
api_key = os.getenv("API_KEY")
```

### 2) Use `find_dotenv()`

When you run scripts from different working directories, use `find_dotenv()` to locate the file:

```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
```

### 3) Don’t override real environment variables

By default, `.env` values do **not** override already-set env vars.
You can override explicitly:

```python
load_dotenv(override=True)
```

### 4) Use `dotenv_values()` (read without mutating env)

```python
from dotenv import dotenv_values
cfg = dotenv_values(".env")
```

This is useful for debugging or for building your own config object.

### 5) Missing values / defaults

```python
timeout = int(os.getenv("TIMEOUT_SECONDS", "10"))
```

## Security notes

- `.env` files are **not encrypted**.
- Put `.env` in `.gitignore`.
- Use real OS env vars for production and CI.

## Demo

Run the example script:

```powershell
python .\main.py
```

The script creates a temporary `.env` file (so it’s safe to run), demonstrates `load_dotenv`, `override`, `find_dotenv`, and `dotenv_values`.
