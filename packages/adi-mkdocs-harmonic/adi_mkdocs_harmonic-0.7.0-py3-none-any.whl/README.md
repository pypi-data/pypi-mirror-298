# Installing & Using the ADI Harmonic Theme for MkDocs

The `mkdocs-harmonic` theme provides a consistent look and feel for documentation of [Analog Devices](https://analog.com) products generated using [MkDocs](https://www.mkdocs.org/). This guide will walk you through the steps needed to install and configure the theme for your MkDocs based documentation project.

## Installation

### Prerequisites

- [Python 3.10](https://www.python.org/downloads/) or greater

## Install using Pip

```sh
pip install adi-mkdocs-harmonic
```

## Creating and running a skeleton MkDocs project

1. Create a `mkdocs.yml` file in the project directory with the following contents:

    ```yml
    site_name: My Project
    theme:
        name: harmonic
    ```

1. Create a `docs` folder with an `index.md` file in it with the following contents:

    ```md
    ---
    title: My project
    ---

    Some overview text

    ## A subheading

    Subheading text
    ```

1. Run `mkdocs serve` in the terminal and open your web browser to <https://localhost:8000>
