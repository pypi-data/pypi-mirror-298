# Poetry Plugin I

[![CI](https://github.com/waketzheng/poetry-plugin-i/actions/workflows/ci.yml/badge.svg)](https://github.com/waketzheng/poetry-plugin-i/actions/workflows/ci.yml)

A [Poetry](https://python-poetry.org/) plugin that support `poetry i` as shortcut of `poetry install`"

Supports Python 3.8+[^1]


## Install

The easiest way to install this plugin is via the `self add` command of Poetry.

```bash
poetry self add poetry-plugin-i
```

If you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.

```bash
pipx inject poetry-plugin-i
```

Otherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.

```bash
pip install poetry-plugin-i
```

## Usage

```bash
poetry i
```
