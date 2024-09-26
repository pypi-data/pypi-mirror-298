# flake8-ecocode

## What it is

A port to Python of the Python-specific parts of [ecoCode](https://github.com/green-code-initiative/ecoCode).

Java Code has been converted to Python, using the `ast` module.

## Installation

```bash
pip install flake8-ecocode
```

or from source:

```bash
git clone https://github.com/abilian/flake8-ecocode.git
cd flake8-ecocode
pip install .
```

## Development

### Setup

```bash
git clone https://github.com/abilian/flake8-ecocode.git
cd flake8-ecocode
poetry install
```

### Run tests

```bash
make test
make lint
```

or against various Python versions:

```bash
nox
```

## Current status

Only 2 checkers have been converted so far out of 11 currently in [ecoCode-python](https://github.com/green-code-initiative/ecoCode-python).

## Contributing

Please contribute to flake8-ecocode by porting the remaining checkers from ecoCode, and adding more.

The documentation from ecoCode also needs to be ported.

You can also contribute by adding tests, documentation, or improving the code.

## TODO

- [ ] Convert the remaining checkers
- [ ] Add tests
- [ ] Add CI/CD
- [ ] Add documentation

