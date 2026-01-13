# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Installation

To install PyWPS and its dependencies, run:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Testing

To run the test suite:

```bash
python -m unittest tests
```

To run tests with code coverage:

```bash
python -m coverage run --source=pywps -m unittest tests
python -m coverage report -m
```

You can also use `tox` to run tests in different environments:

```bash
tox
```

### Running the Example Service

To run the example service:

```bash
git clone git://github.com/geopython/pywps-flask.git pywps-flask
cd pywps-flask
python demo.py
```

The service will be available at `http://localhost:5000`.

## Code Architecture

PyWPS is an implementation of the OGC Web Processing Service (WPS) standard. Its architecture is based on the concepts of Services and Processes.

- **`Service`**: A `Service` is a container for one or more `Process` objects. It's responsible for handling WPS requests and delegating them to the appropriate `Process`. The main entry point for a PyWPS service is typically a script that instantiates a `Service` with a list of `Process` classes.

- **`Process`**: A `Process` is a Python class that represents a single WPS process. It defines a geospatial operation, its inputs, and its outputs. Key attributes of a `Process` include:
    - `identifier`: A unique identifier for the process.
    - `title`: A human-readable title.
    - `handler`: The method that contains the business logic of the process. It receives a `WPSRequest` and a `WPSResponse` object.
    - `inputs`: A list of `Input` objects that define the process's inputs.
    - `outputs`: A list of `Output` objects that define the process's outputs.

- **Inputs and Outputs**: PyWPS supports three types of inputs and outputs:
    - **`LiteralInput`/`LiteralOutput`**: For simple values like strings, numbers, and booleans.
    - **`ComplexInput`/`ComplexOutput`**: For large data objects, such as vector or raster files. These support different data formats and validation.
    - **`BoundingBoxInput`/`BoundingBoxOutput`**: For defining a geographical area of interest.

- **Asynchronous Execution**: PyWPS supports asynchronous execution of processes, which is useful for long-running tasks. When a process is executed asynchronously, the service immediately returns a response with a status URL. The client can then poll this URL to get updates on the process's status.

- **`pywps/app`**: This directory contains the core application logic, including the `Service`, `Process`, and `WPSRequest` classes.
- **`pywps/inout`**: This directory defines the input and output data structures, such as `LiteralInput`, `ComplexInput`, and `BoundingBoxInput`.
- **`pywps/processing`**: This directory contains the logic for processing jobs, including synchronous and asynchronous execution.
- **`pywps/validator`**: This directory contains validators for different data formats.
- **`docs/`**: This directory contains the project's documentation, which is a valuable resource for understanding the project in more detail.
