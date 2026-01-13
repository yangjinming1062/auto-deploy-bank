# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

To set up the development environment and run tests, use the following commands:

- `pip install -e '.[test]'`: Install dependencies for development and testing.
- `pytest`: Run the test suite.

## Code Architecture

This repository contains a Datasette plugin that transforms SQL `SELECT` queries returned by another query into clickable links.

The core logic is in `datasette_query_links/__init__.py`:

- The `render_cell` hookimpl is the main entry point. It checks if a cell value is a string that starts with "select".
- If it is, the `is_valid_select` function is called to verify that the SQL is a valid `SELECT` statement. This is done by wrapping the query in `SELECT 1 FROM (...) LIMIT 0` and executing it against the database.
- If the query is valid, the cell content is replaced with a hyperlink to the Datasette query interface, with the SQL query as a parameter.
