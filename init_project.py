from __future__ import annotations

import argparse
import os
import re
import subprocess
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent


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
    if not author:
        raise ValueError("Set USER_NAME or git config user.name before running make init.")

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

    license_path = ROOT / "LICENSE"
    text = license_path.read_text(encoding="utf-8")
    text = re.sub(
        r"(?m)^Copyright \(c\) .*$",
        lambda _: f"Copyright (c) {date.today().year} {author}",
        text,
        count=1,
    )
    license_path.write_text(text, encoding="utf-8")

    for filename in ("favicon.svg", "CONTRIBUTING.md"):
        (ROOT / filename).unlink(missing_ok=True)


def self_test() -> None:
    assert toml_string('a "b"') == '"a \\"b\\""'
    text = '[project]\nname = "old"\n'
    assert set_project_key(text, "name", '"new"') == '[project]\nname = "new"\n'
    assert set_project_key("[project]\n", "authors", "[]") == "[project]\nauthors = []\n"

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    with TemporaryDirectory() as directory, patch(f"{__name__}.ROOT", Path(directory)):
        (ROOT / "pyproject.toml").write_text('[project]\nname = "old"\n', encoding="utf-8")
        (ROOT / "LICENSE").write_text(license_text, encoding="utf-8")
        for filename in ("favicon.svg", "CONTRIBUTING.md"):
            (ROOT / filename).touch()
        with patch.dict(os.environ, {"USER_NAME": "New Author", "USER_EMAIL": "a@example.com"}):
            init()
            expected = license_text.splitlines()
            expected[2] = f"Copyright (c) {date.today().year} New Author"
            assert (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines() == expected
            assert not (ROOT / "favicon.svg").exists()
            assert not (ROOT / "CONTRIBUTING.md").exists()
            assert 'name = "New Author"' in (ROOT / "pyproject.toml").read_text(encoding="utf-8")
            init()  # Repeated initialization tolerates already removed template files.
        with patch(f"{__name__}.user_name", return_value=""):
            try:
                init()
            except ValueError:
                pass
            else:
                raise AssertionError("Initialization must require an author name")
        assert (ROOT / "LICENSE").read_text(encoding="utf-8").splitlines() == expected


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test() if args.self_test else init()
