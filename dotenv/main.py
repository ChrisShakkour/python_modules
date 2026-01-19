"""Demo for python-dotenv (import name: dotenv).

Covers:
- load_dotenv() basic usage
- load_dotenv(override=True)
- find_dotenv() for locating files
- dotenv_values() to read without mutating os.environ

This script is intentionally self-contained: it creates a temporary .env file
under the same directory, runs demos, then cleans up.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import dotenv_values, find_dotenv, load_dotenv


HERE = Path(__file__).resolve().parent
TEMP_ENV_PATH = HERE / ".env.demo"


def banner(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def write_demo_env(path: Path) -> None:
    # Keep it ASCII-only and simple to avoid platform encoding surprises.
    path.write_text(
        "\n".join(
            [
                "# demo .env file",
                "API_KEY=demo_key_from_env_file",
                "DEBUG=true",
                "TIMEOUT_SECONDS=15",
                "GREETING=hello world",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def demo_dotenv_values(path: Path) -> None:
    banner("1) dotenv_values() (read without modifying os.environ)")
    cfg = dotenv_values(path)
    print("dotenv_values ->", cfg)
    print("os.getenv('API_KEY') BEFORE load_dotenv ->", os.getenv("API_KEY"))


def demo_load_dotenv(path: Path) -> None:
    banner("2) load_dotenv() basic")
    # By default, this will NOT override already-set environment variables.
    load_dotenv(path)

    print("API_KEY ->", os.getenv("API_KEY"))
    print("DEBUG ->", os.getenv("DEBUG"))
    print("TIMEOUT_SECONDS ->", os.getenv("TIMEOUT_SECONDS"))

    timeout = int(os.getenv("TIMEOUT_SECONDS", "10"))
    debug = os.getenv("DEBUG", "false").lower() in {"1", "true", "yes", "on"}
    greeting = os.getenv("GREETING", "(missing)")

    print("parsed timeout (int) ->", timeout)
    print("parsed debug (bool) ->", debug)
    print("greeting ->", greeting)


def demo_override(path: Path) -> None:
    banner("3) override behavior")

    # Simulate a real environment variable (e.g., set by OS / CI).
    os.environ["API_KEY"] = "real_env_value"

    load_dotenv(path, override=False)
    print("override=False ->", os.getenv("API_KEY"), "(expected: real_env_value)")

    load_dotenv(path, override=True)
    print(
        "override=True  ->",
        os.getenv("API_KEY"),
        "(expected: demo_key_from_env_file)",
    )


def demo_find_dotenv(path: Path) -> None:
    banner("4) find_dotenv()")

    # find_dotenv tries to locate a .env file by walking up parent dirs.
    # Here we point it at our demo file by temporarily copying/renaming to .env.
    # This demonstrates how people typically use it in app entrypoints.
    temp_real_env = path.parent / ".env"
    try:
        temp_real_env.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        found = find_dotenv(usecwd=False)
        print("found .env ->", found)
    finally:
        try:
            temp_real_env.unlink(missing_ok=True)
        except TypeError:
            # Python < 3.8 compatibility; not expected here, but harmless.
            if temp_real_env.exists():
                temp_real_env.unlink()


def main() -> None:
    banner("python-dotenv demo")
    print("Working dir:", os.getcwd())

    write_demo_env(TEMP_ENV_PATH)
    try:
        demo_dotenv_values(TEMP_ENV_PATH)
        demo_load_dotenv(TEMP_ENV_PATH)
        demo_override(TEMP_ENV_PATH)
        demo_find_dotenv(TEMP_ENV_PATH)
    finally:
        try:
            TEMP_ENV_PATH.unlink(missing_ok=True)
        except TypeError:
            if TEMP_ENV_PATH.exists():
                TEMP_ENV_PATH.unlink()


if __name__ == "__main__":
    main()
