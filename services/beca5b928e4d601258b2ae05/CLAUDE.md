# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level code architecture and structure

This is a modular Django ERP system built with Python 2.7 and MySQL. The project is divided into several applications, each corresponding to a specific business function.

Here's a breakdown of the key applications:

- **Sale**: Manages sales-related functionalities, including customer relationship management (CRM), sales orders, and sales returns.
- **Purchase**: Handles procurement processes, such as purchase orders, supplier management, and purchase returns.
- **Invent**: Manages inventory, including product information, stock levels, and warehouse management.
- **Organ**: Defines the organizational structure of the company, including departments, positions, and employees.
- **HR**: Manages human resources functions, such as employee profiles, attendance, and payroll.
- **Workflow**: Implements a workflow engine for approval processes across different modules.
- **Basedata**: Contains basic data and configurations used throughout the system.
- **Syscfg**: Manages system-level configurations and settings.
- **Selfhelp**: Provides self-service functionalities for employees.
- **Midware**: Includes custom middleware for handling requests and responses.
- **Plugin**: Supports extensions and plugins to enhance the system's capabilities.

The main settings for the project are located in `mis/settings.py`, and the URL routing is defined in `mis/urls.py`. The templates are stored in the `templates` directory, and the static files are in the `static` directory.

## Common Commands

Here are some common commands for developing in this codebase:

- **Run the development server**:
  ```bash
  python manage.py runserver
  ```

- **Run tests**:
  ```bash
  python manage.py test
  ```

- **Create database migrations**:
  ```bash
  python manage.py makemigrations
  ```

- **Apply database migrations**:
  ```bash
  python manage.py migrate
  ```

- **Change a user's password**:
  ```bash
  python manage.py changepassword <username>
  ```

- **Import the database**:
  ```bash
  mysql -uroot -proot mis < Install/mis.sql
  ```
