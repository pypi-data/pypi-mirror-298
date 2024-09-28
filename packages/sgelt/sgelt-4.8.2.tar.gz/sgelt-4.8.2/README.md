# SGELT: Site GEnerator for Labs and Teams

## Installation

* Create a python virtual environment :

```bash
virtualenv .venv/
```

* Activate it

```bash
source .venv/bin/activate
```

* Install the package and its dependencies :

```bash
pip install sgelt --index-url https://gitlab.math.unistra.fr/api/v4/projects/653/packages/pypi/simple
```

## Build a website

### Files organization

* `config.yml` describes the site configuration
* `content/` dir contains markdown files
* `agenda.json` contains all events data
* `teams.json` contains teams data

### Edit content

* setup configuration in `config.yml`
* edit `content/` dir.
* generate json data files

### Build and serve

To build all site files, run :

```bash
sgelt
```

in the project directory.
Output files will be written in `output/` dir.

### Build and serve

To serve the website and rebuild automatically when the content has changed:

```bash
sgelt -a -s
```

To open the homepage in a web browser, add:

```bash
sgelt -a -s -b
```

### Get help with CLI

```bash
sgelt -h
```

## Tests

### Run tests using tox

Tox setup the appropriate environments and run tests using pytest:

```bash
pip install tox  # install tox
tox  # run
```

### Run tests using pytest

```bash
pip install -e .[tests]  # install dependencies for tests
pytest -sv tests/  # run tests
```
