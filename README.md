# SupaPWN

A Windows-based penetration testing tool targeting misconfigured Supabase instances. SupaPWN performs authenticated table enumeration against a provided Supabase project, iterating over an extensive wordlist of common table names to identify and extract accessible data.

> **Legal Disclaimer** — This tool is intended for authorized security assessments, penetration testing engagements, and educational research only. Using SupaPWN against any Supabase instance without explicit written permission from the project owner is illegal and unethical. The authors assume no liability for misuse.

---

## Overview

Many Supabase projects expose their REST API with overly permissive Row Level Security (RLS) policies, or none at all. SupaPWN automates the discovery of accessible tables by attempting to read from a curated list of commonly used table names via the PostgREST API endpoint. Successfully reached tables are saved to disk as JSON files for later review.

### Key Features

- Validates provided credentials before initiating any scan
- Iterates over 500+ table name candidates covering users, authentication, payments, PII, logs, and more
- Handles paginated responses (up to 1,000 rows per request using `Range` headers)
- Saves extracted table contents to structured JSON files, organized by workspace
- Displays real-time scan progress in a graphical interface
- Allows the scan to be stopped mid-execution

---

## Requirements

- Windows 10 or later
- Python 3.10+
- Internet access to the target Supabase project

### Python Dependencies

```
requests
customtkinter
pyperclip
pillow
```

---

## Installation

1. Clone or download this repository and extract the archive.
2. Run the installer to set up dependencies:

```bat
Install.bat
```

This installs all required Python packages listed in `Src/requirements.txt`.

---

## Usage

Launch the application:

```bat
Run.bat
```

In the GUI, fill in the following fields:

| Field | Description |
|---|---|
| **Supabase ID** | The project identifier (e.g. `abcdefghijklmnop`) |
| **Workspace Name** | A local name for this scan session; used as the output directory name |
| **Public API Key** | The project's `anon` or `service_role` API key |
| **Bearer Token** | A valid JWT bearer token for the target project |

Once all fields are filled, click **Launch scan**. The tool will:

1. Validate the credentials against the Supabase auth endpoint.
2. Iterate through the table wordlist, querying each table via `GET /rest/v1/{table}?select=*`.
3. Display accessible tables with row counts and endpoint URLs in the results panel.
4. Save each extracted table to `./Src/Accessed Databases/{workspace}/{table}.json`.

To abort a running scan, click the **Stop** button.

---

## Output

Extracted data is written to:

```
Src/
└── Accessed Databases/
    └── {Workspace Name}/
        ├── users.json
        ├── profiles.json
        └── ...
```

Each file contains the full JSON array returned by the Supabase REST API for that table.

---

## Project Structure

```
SupaPWN/
├── Install.bat            # Dependency installer
├── Run.bat                # Application launcher
└── Src/
    ├── entry.py           # Entry point (spawns main.py without a console window)
    ├── main.py            # Main GUI and scan logic
    ├── requirements.txt   # Python dependencies
    ├── Assets/
    │   ├── Fonts/         # Custom fonts (Horizon, Archivo Black)
    │   └── Img/           # UI assets
    ├── Accessed Databases/ # Scan output directory (created at runtime)
    └── Lib/
        ├── supabase.py    # Supabase API interaction (validation, table extraction)
        ├── wordlist.py    # Table name wordlist (500+ entries)
        ├── messagebox.py  # Custom dialog component
        ├── winutils.py    # Windows title bar and window utilities
        ├── images.py      # Image loading helper
        └── lowlevel.py    # Low-level Windows API calls (fonts, rounded corners)
```

---

## Technical Details

### Credential Validation

Before scanning, SupaPWN sends a `GET` request to:

```
https://{project_id}.supabase.co/auth/v1/token
```

A `405 Method Not Allowed` response confirms that the endpoint is reachable and the API key is accepted, which is used as a signal that the configuration is valid.

### Table Enumeration

Each table name is probed with:

```
GET https://{project_id}.supabase.co/rest/v1/{table}?select=*
```

Pagination is handled automatically using `Range` headers in increments of 1,000 rows until the API returns fewer results than requested or an unsuccessful status code.

A table is considered accessible when the response status is `200` or `206` and the response body is a non-empty JSON array.

### Wordlist

The built-in wordlist in `Lib/wordlist.py` covers over 500 table name patterns across the following categories:

- User and account tables
- Authentication and session data
- Roles and permissions
- Payments, billing, and financial records
- Personally Identifiable Information (PII)
- Content and media
- Application configuration and feature flags
- Logs and audit trails
- Security and abuse management
- Notifications and communication
- E-commerce and inventory
- Miscellaneous SaaS patterns

---

## Limitations

- Windows only (relies on `ctypes.windll` and Windows-specific title bar rendering)
- No proxy or TLS interception support
- Wordlist-based enumeration only; does not attempt to discover table names through schema introspection endpoints
- Does not test for write access or privilege escalation

---

## License

This project is provided for educational and authorized testing purposes. Redistribution and use are permitted provided that any deployment complies with applicable laws and the terms of service of the target platform.