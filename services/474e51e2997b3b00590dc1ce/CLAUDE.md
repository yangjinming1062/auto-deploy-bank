# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

This is the Django REST Framework, a powerful and flexible toolkit for building Web APIs. The framework is designed to be highly customizable, allowing developers to use regular function-based views or more powerful generic views, viewsets, and routers.

The core of the framework includes:

*   **Serializers**: For converting complex data types to native Python datatypes that can then be easily rendered into JSON, XML or other content types.
*   **Views**: For handling requests and returning responses.
*   **Routers**: For automatically generating URL configurations for viewsets.
*   **Authentication and Permissions**: For securing the API.

The codebase is primarily located in the `rest_framework/` directory.

## Common Development Tasks

### Running tests

The test suite is run using `pytest` via the `runtests.py` script.

To run the full test suite:

```bash
python runtests.py
```

To run a specific test file:

```bash
python runtests.py tests/test_authtoken.py
```

To run a specific test case or function:

```bash
python runtests.py TestAuthToken.test_create_token
```

The project also uses `tox` to run tests against multiple Python and Django versions. To run the tests for a specific environment:

```bash
tox -e py311-django51
```

### Building the documentation

The documentation is built using `mkdocs`. To build the documentation:

```bash
mkdocs build
```
