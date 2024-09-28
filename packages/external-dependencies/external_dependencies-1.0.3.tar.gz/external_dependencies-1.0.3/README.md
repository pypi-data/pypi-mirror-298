# external_dependencies

external_dependencies : A CLI interface to install external dependencies using apt or static build from s3

## Installation

## Usage


## [DEV] Install the virtual env
`uv sync`
If not already activated then run `uvx pre-commit install` (for more info on it: https://skillcorner.slite.com/app/docs/OFzvpQNh8VBOcQ)

## Test
To run tests you can cd into a package directory and run `uv run pytest`.
Tests will also be run in the CI/CD.

## Versioning and dependencies
Your code should be under the package directory.
If you have set requirements directly in your `pyproject.toml` you can run `uv sync`.
It will create a virtual environment (`.venv/`) with the requirements and create a `uv.lock` file to freeze your dependencies.

In order to add or remove dependencies, you can use:
`uv add boto3`
`uv remove boto3`
You can also add dependencies in the dev group or any arbitrary optional group:
`uv add coverage pirlo poethepoet pytest ruff --dev`
`uv add pandas --optional analysis`

You can also upgrade your virtual environment and update your lock file if there is new versions of dependencies compatible with your requirements:
`uv sync --upgrade`

When you want to release a new version of a package, you must follow this:
- major (breaking change)	1.0.2	--> 2.0.0
- minor (new feature)	    1.0.2	-->	1.1.0
- patch (fix)	            1.0.2	-->	1.0.3
- prerelease (durint test)  1.0.2	-->	1.0.3a0

We try to follow the semantic versioning from https://semver.org/ as recommended by Python Foundation (https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#semantic-versioning-preferred)
