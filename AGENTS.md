# Agent instructions

- Setup: `make install`, then `make pre-commit-install`. `make init` is for a
  fresh template only: it rewrites README.md, project metadata, and license
  ownership/year, and removes favicon.svg and CONTRIBUTING.md.
- Tests: `make test` (pytest under `tests/`). Add focused tests for new behavior
  and bug fixes. Run `python init_project.py --self-test` for initializer checks.
- Lint: `make lint`. Format: `make format` (Black, 100-character lines).
  Run `.venv/bin/pre-commit run --all-files` before handing off changes.
- Follow KISS: make the smallest complete change; avoid speculative features,
  abstractions, configuration, and dependencies.
- Keep functions and methods short and focused. Reuse existing helpers; extract
  shared logic when it removes duplication, without adding unnecessary layers.
- Follow nearby code conventions and keep Hydra configs and dataclass schemas
  consistent. Keep config groups limited to environment and training; use Watson
  for logging and saving. Preserve validation, error handling, and reproducibility.
- Update affected callers, tests, and docs. Run relevant checks and report any
  failures or checks you could not run. Do not claim passing tests without evidence.
- Keep credentials, datasets, recordings, and generated outputs out of Git.
  Optional Watson setup: `make install-watson` (Python 3.10+); settings live in
  root `watson.yaml`.
