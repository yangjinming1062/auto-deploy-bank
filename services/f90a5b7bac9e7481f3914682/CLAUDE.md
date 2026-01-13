# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

To get started with development, set up a virtual environment and install the required dependencies:

```bash
python -m pip install -r requirements_dev.txt
```

To run the example application:

```bash
make example
```

### Testing

-   Run the standard test suite:
    ```bash
    make test
    ```
-   Run tests with coverage measurement:
    ```bash
    make coverage
    ```
-   Run tests across all supported Python and Django versions:
    ```bash
    tox
    ```
-   Run the Selenium-based frontend tests:
    ```bash
    make test_selenium
    ```

### Linting and Formatting

This project uses `ruff` for linting and `pre-commit` to enforce code style.

-   Install the pre-commit hooks:
    ```bash
    pre-commit install
    ```
-   Run formatting on all files:
    ```bash
    pre-commit run --all-files
    ```

### Documentation

To build the documentation locally:

```bash
tox -e docs -- html
```

The output will be in the `docs/_build/html/` directory.

## Code Architecture

The Django Debug Toolbar has three main components:

-   **`DebugToolbarMiddleware`**: The entry point of the toolbar. It decides whether to instrument a request and injects the toolbar into the response.
-   **`DebugToolbar`**: This class manages all the panels and contains the logic that is aware of all of them.
-   **`Panels`**: These contain most of the complex logic for collecting metrics, sometimes using techniques like monkey-patching. The `SQLPanel` is particularly complex.

The general flow is as follows:
1.  The middleware intercepts a request.
2.  If the request should be instrumented, a `DebugToolbar` instance is created.
3.  The panels collect information during the request/response cycle.
4.  The middleware injects the toolbar's HTML and JavaScript into the final response.

### Architectural Challenges

-   The `SQLPanel` has a complex implementation.
-   Async support is incomplete in some panels.
-   The toolbar is incompatible with Django Channels due to differences in middleware design.
