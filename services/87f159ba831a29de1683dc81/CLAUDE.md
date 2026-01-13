# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Build frontend:** `npm run build`
- **Watch frontend:** `npm run watch`
- **Run Python tests:** `pytest`
- **Run Cypress tests:** The project uses Cypress for end-to-end testing, with tests located in the `cypress/integration` directory.
- **Python formatting:** `black`

## Code Architecture

CKAN is a data portal platform built with a Python backend and a Javascript frontend.

- **Backend:** The core application logic is in the `ckan` directory. Extensions are in the `ckanext` directory. The application uses the Pylons web framework.
- **Frontend:** The frontend is a mix of traditional server-rendered pages and Javascript. Frontend assets are in `ckan/public`. The build process uses Gulp to compile Less to CSS. Vendor libraries are managed with npm and are located in `ckan/public/base/vendor`.
