# JupyterClearCheck

![Build Status](https://github.com/guru-desh/JupyterClearCheck/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/github/license/guru-desh/JupyterClearCheck) ![PyPI version](https://img.shields.io/pypi/v/JupyterClearCheck)

A Python CLI to check that a Jupyter Notebook's Outputs' have been cleared.

## Why does this exist?

During the development of a Jupyter Notebook, it is common to run cells multiple times. Every time a cell is run, its output is stored in the `.ipynb` file format. Because the outputs are saved, this can cause merge conflicts in version control systems like Git when multiple people are working on the same notebook.

`nbconvert` can be used to clear the outputs of a notebook, but to our knowledge, there was no package to check if the outputs have been cleared. This package aims to fill that gap. 

This package can be used in a CI/CD pipeline to ensure that the outputs of a notebook have been cleared before merging a pull request reducing merge conflicts on the outputs of a notebook.

## Installation

This package is available on PyPI and can be installed using pip.

```bash
pip install JupyterClearCheck
```

## Usage

You can run the command via `jupyterclearcheck` or `python -m jupyterclearcheck`.

```bash
$ jupyterclearcheck --help

usage: jupyterclearcheck [-h] --notebook NOTEBOOK

Check a Jupyter Notebook for output cells.

options:
  -h, --help           show this help message and exit
  --notebook NOTEBOOK  Path to the Jupyter Notebook file
```

The notebook parameter is required and should be the path to the Jupyter Notebook file.

## Contributing

We welcome contributions! Thank you in advance for your help. Feel free to submit a pull request or open an issue.

### Getting Started for Development

We use Python 3.9 and PDM for dependency management. To get started, install Python 3.9 and then install PDM using pip.

```bash
pip install pdm
```

Once this step is done, PDM can be used to run commands related to the development of this package.

- Install dependencies: `pdm install`
- Run linting and formatting: `pdm run lint_and_format`
- Checking linting, formatting, and type annotations: `pdm run check`
- Run tests: `pdm run test`
- Build package: `pdm build`

#### Running CI pipeline locally

The CI pipeline can be run locally using the following scripts:

- Windows: `./build_and_test.sh`
- Linux/MacOS: `./build_and_test.cmd.`

## Future Work

- [ ] Add shellcheck to lint bash scripts currently in use
- [ ] Add pre-commit hook
- [ ] Add markdown lint
- [ ] Publish on conda-forge
