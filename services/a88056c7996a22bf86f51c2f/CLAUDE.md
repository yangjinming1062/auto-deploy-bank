# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TheTimeMachine is a Wayback Machine recon tool used for OSINT, bug bounty hunting, and security research. It scrapes archived URLs, finds exposed backups, and scans for vulnerabilities (XSS, SQLi, LFI, etc.) using pattern matching against archived requests.

## Commands

**Install dependencies:**
```bash
pip3 install -r requirements.txt
```

**Run the tool:**
```bash
python3 thetimemachine.py <target.com> [OPTIONS]
```

**Common options:**
- `--fetch`: Fetch all archived URLs from the Wayback Machine for a target.
- `--backups`: Scan for exposed backup files (config, .bak, .zip, etc.).
- `--attack <type>`: Run attack mode (e.g., `--attack xss`, `--attack sqli`).
- `--listings`: Detect open directory listings.
- `--parameters`: Extract and map GET parameters from URLs.

**Example:**
```bash
python3 thetimemachine.py example.com --fetch --attack xss
```

## Architecture

- **Entry Point:** `thetimemachine.py` handles CLI arguments and orchestrates the workflow.
- **Core Modules (`core/`):**
  - `fetcher.py`: Interacts with the Wayback Machine API to retrieve URLs.
  - `attackmode.py`: Core logic for pattern matching against the `db/` rules.
  - `backupfinder.py`, `lister.py`, `subdomains.py`, `parameters.py`: Specialized scanners for different artifacts.
  - `ui.py`: Handles console output and loading animations.
  - `utils.py`: Shared utilities.
- **Database (`db/`):** Contains text files with payload lists and regex patterns for different vulnerability types (e.g., `xss.txt`, `sqli.txt`).
- **Configuration:** `extensions.txt` defines the file extensions to search for when using `--backups`.
- **Output:** Results are saved in `content/<target>/`.

## Notes

- The tool uses `rich` for console formatting.
- Ensure you have network access to the Wayback Machine API (`web.archive.org`).