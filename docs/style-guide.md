# Style Guide

## Language

* Repository documentation is written in English.
* Source code comments are written in English.
* Public APIs use English identifiers.
* Commit messages follow Conventional Commits.

## Code style

* Python ≥ 3.12
* `ruff format`
* `ruff check`
* `pytest`
* `pyright --strict`

## Git principles
* conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `chore`, `docs:`, `build:`, `ci:`, `style:`, `perf:`
* small commits
* no squash merges
* all changes via pull request
* Semantic versioning, start with `0.0.1`

## Design principles

* Separate the library from cli callable scripts
* Immutable value objects
* No quick hacks
* Test-driven development
* Parser → Object Model → Renderer
* Geometry is independent of SVG/XML
* Separate geometry (e.g. where is a certain object) from style (e.g. what color does it have)
* overload operators so that e.g. `p1+p2` (vector addition of two points) or `s*p` (scalar multiplication of a vector) works
* Minimal dependencies
* Use inheritance only for true "is-a" relationships. Prefer composition for reusable behavior and properties.
* Make invalid states unrepresentable (i.e. don't allow a circle with a negative radius). All value objects check their invariants `__post_init__()`.

