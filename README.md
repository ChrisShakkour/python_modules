# python_modules

## Python virtual environment (Windows PowerShell)

Create a virtual environment in the repo root (first time only):

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow local scripts for your user and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Install dependencies (if/when this repo has any):

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Deactivate when you’re done:

```powershell
deactivate
```