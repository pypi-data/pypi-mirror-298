# Whitebox - GPS Display Plugin

This is a plugin for [whitebox](https://gitlab.com/whitebox-aero) that displays the GPS data using leaflet.js.

## Installation

Clone the repository into the `plugins` directory of whitebox. That's it!

## For Developers

1. Make sure [poetry](https://python-poetry.org/docs/#installation) is installed.
2. Run: `poetry config virtualenvs.in-project true`
3. Ensure you are using supported python version (3.10 and above): `poetry env use 3.10`
4. Run: `poetry install`

## Running Tests

Run: `make test`

## Contribution Guidelines

1. Write tests for each new feature.
2. Ensure coverage is 90% or more.
3. [Google style docstrings](https://mkdocstrings.github.io/griffe/docstrings/#google-style)
   should be used for all functions and classes.
