# flake8-ecocode

## What it is

A port to Python of the Python-specific parts of [ecoCode](https://github.com/green-code-initiative/ecoCode).

Java Code has been converted to Python, using the `ast` module.

## What is ecoCode?

ecoCode is a collective project aiming to reduce environmental footprint of software at the code level. The goal of the project is to provide a list of static code analyzers to highlight code structures that may have a negative ecological impact: energy and resources over-consumption, "fatware", shortening terminals' lifespan, etc.

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

