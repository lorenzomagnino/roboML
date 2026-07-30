from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sh(*args: str) -> str:
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def toml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def project_name() -> str:
    return os.environ.get("PROJECT_NAME") or ROOT.name


def user_name() -> str:
    return os.environ.get("USER_NAME") or sh("git", "config", "user.name")


def user_email() -> str:
    return os.environ.get("USER_EMAIL") or sh("git", "config", "user.email")


def set_project_key(text: str, key: str, value: str) -> str:
    line = f"{key} = {value}"
    pattern = rf"(?m)^({re.escape(key)}\s*=).*$"
    if re.search(pattern, text):
        return re.sub(pattern, line, text, count=1)
    return re.sub(r"(?m)^\[project\]\n", f"[project]\n{line}\n", text, count=1)


def init() -> None:
    name = project_name()
    author = user_name()
    email = user_email()

    (ROOT / "README.md").write_text(f"# {name}\n\nThis is a Research Project\n", encoding="utf-8")

    pyproject = ROOT / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    text = set_project_key(text, "name", toml_string(name))
    text = set_project_key(text, "description", toml_string("This is a Research Project"))
    if author and email:
        text = set_project_key(
            text,
            "authors",
            f"[{{ name = {toml_string(author)}, email = {toml_string(email)} }}]",
        )
    pyproject.write_text(text, encoding="utf-8")


def self_test() -> None:
    assert toml_string('a "b"') == '"a \\"b\\""'
    text = "[project]\nname = \"old\"\n"
    assert set_project_key(text, "name", '"new"') == "[project]\nname = \"new\"\n"
    assert set_project_key("[project]\n", "authors", "[]") == "[project]\nauthors = []\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test() if args.self_test else init()
