# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Oscar is a domain-driven e-commerce framework for Django. It is structured so that any part of the core functionality can be customized to suit the needs of your project.

## Common Commands

The following commands are available in the `Makefile`:

*   `make install`: Install requirements for local development and production.
*   `make test`: Run tests.
*   `make lint`: Run linting checks.
*   `make sandbox`: Install requirements and create a sandbox.
*   `make docs`: Compile documentation.
*   `make clean`: Remove files not in source control.

## Code Architecture

The main application logic is located in the `src/oscar` directory. The project is divided into several Django apps, which can be found in `src/oscar/apps`. These include:

*   `address`
*   `analytics`
*   `basket`
*   `catalogue`
*   `checkout`
*   `communication`
*   `customer`
*   `dashboard`
*   `offer`
*   `order`
*   `partner`
*   `payment`
*   `search`
*   `shipping`
*   `voucher`
*   `wishlists`

## Dependencies

The project's dependencies are listed in the `pyproject.toml` file. Key dependencies include:

*   `django>=4.2,<5.3`
*   `pillow>=6.0`
*   `django-extra-views>=0.13,<0.17`
*   `django-haystack>=3.0b1`
*   `django-treebeard>=4.3.0`
*   `Babel>=1.0,<3.0`
*   `purl>=0.7`
*   `phonenumbers`
*   `django-phonenumber-field>=4.0.0,<9.0.0`
*   `factory-boy>=3.3.1,<4.0.0`
*   `django-tables2>=2.3,<=2.7`
*   `django-widget-tweaks>=1.4.1`

## Contribution Guidelines

To contribute, please follow these steps:

1.  Fork the project repository on GitHub.
2.  Clone your forked repository to your local machine.
3.  Create a new branch for your changes.
4.  Make your changes, and commit them with clear commit messages.
5.  Push your changes to your forked repository.
6.  Open a pull request on the original project repository, explaining your changes.

Further details can be found in `docs/source/internals/contributing/index.rst`.
