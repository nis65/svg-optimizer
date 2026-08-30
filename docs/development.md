# Needed tools

The following has been tested on a Ubuntu 2204:

* **ruff**: `snap install ruff`
* **pytest** including coverage: `apt install python3-pytest python3-pytest-cov`
* **ristretto** a simple and quick svg viewer: `apt install ristretto`

# Checking the code

Run `run-tests.sh` from the root directory of this repo
* If there are `ruff format` errors, inspect them and if all ok, fix them with `ruff format`. If you don't want `ruff` to reformat a certain part of your code, insert `# fmt: off` and `# fmt: on` tags and check again.
* If there are `ruff check` errors, inspect them. If they can be fixed automatically, use `ruff check --preview --extend-select PLR --output-format=full src --fix`. If not, fix the code manually. If you can't or don't want to fix the code, Use `ruff rule` to find out the required `noqa:` error number.
* If there are coverage errors, you will need to add another test case or, in rare cases, a `# pragma: no cover` tag to the code.
* After all example code was run by `run-tests`, use `ristretto` to inspect graphically the rendered files below `/tmp/svgtests`. You can safely remove that directory when done.
