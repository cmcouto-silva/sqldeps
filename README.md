# SQL Dependency Extractor

<p align="left">
<a href="https://github.com/cmcouto-silva/sqldeps/actions/workflows/ci.yml" target="_blank">
    <img src="https://github.com/cmcouto-silva/sqldeps/actions/workflows/ci.yml/badge.svg" alt="Test">
</a>
<a href="https://pypi.org/project/sqldeps" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sqldeps.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/sqldeps" target="_blank">
    <img src="https://img.shields.io/pypi/v/sqldeps?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypistats.org/packages/sqldeps" target="_blank">
    <img src="https://img.shields.io/pypi/dm/sqldeps.svg?label=PyPI%20downloads" alt="PyPI Downloads">
</a>
<a href="https://opensource.org/licenses/MIT" target="_blank">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="PyPI Downloads">
</a>
</p>

An intelligent tool that automatically extracts and maps critical table and column dependencies from SQL scripts using advanced LLM capabilities.


## Overview

SQL Dependency Extractor identifies the minimal set of database objects required for successful query execution while filtering out temporary constructs, CTEs, and created tables. It's designed to help with:

- **Change Management**: Safely modify database schemas by identifying real dependencies
- **Storage Optimization**: Identify truly necessary tables and columns
- **Migration Planning**: Know exactly what needs to be migrated
- **Project Documentation**: Generate comprehensive documentation of which tables and columns a project repository requires

## Core Features

- Extracts only source tables and their required columns from SQL scripts
- Automatically ignores temporary structures (CTEs, derived tables, etc.)
- Optional schema validation against live databases
- Generates clear dependency lists in JSON or CSV format

## Installation

### Requirements

**Software:**
- [UV](https://github.com/astral-sh/uv) - Python package manager
- [Git](https://git-scm.com/) - Version control

**API Keys/Tokens** (required only for frameworks you'll use):
- [Groq](https://console.groq.com/keys)
- [OpenAI](https://platform.openai.com/settings/organization/api-keys)
- [DeepSeek](https://platform.deepseek.com/api_keys)

> Note: [Groq](https://groq.com/) is the only framework that allows accessing hosted LLMs for free (no billing info required). See the [rate limits](https://console.groq.com/docs/rate-limits) for the Free Tier.

### Install Stable Version from PyPI

```bash
uv pip install sqldeps
```

From TestPyPI:
```bash
uv pip install sqldeps --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/
```

### Install Development Version

Clone the repository and install dependencies:

```bash
git clone git@gitlab.com:gibbs-lab/database/sql-dependency-extractor.git
cd sql-dependency-extractor
uv sync && source .venv/bin/activate
```

Create a `.env` file with your API keys (see `.env.example`):

```
# Database credentials
DB_HOST = "host"
DB_PORT = "5432"
DB_NAME = "database"
DB_USER = "username"
DB_PASSWORD = "password"

# API Keys
GROQ_API_KEY = "groq_token"
OPENAI_API_KEY = "openai_token"
DEEPSEEK_API_KEY = "deepseek_token"
```

Alternatively, you can provide database credentials with a YAML file (see example in `configs/database.yml`).

## Web Application - Showcase

A Streamlit-based web interface is available for demonstrating SQL dependency extraction capabilities. The web app allows users to:

- Upload SQL files or enter SQL queries directly
- Select LLM frameworks, models and custom prompts
- Visualize extracted dependencies in real-time
- Optionally validate against a database schema
- Download results in CSV or JSON format

Note: The web application is primarily for demonstration and interactive exploration of single SQL queries. For processing multiple files or entire project folders, the CLI or API approach is recommended for better performance and flexibility.

To run the web app (requires additional dependencies):

```bash
# Install with web app dependencies
# uv pip install sqldeps[app] # *after uploading to PyPI
uv sync --extra app

# Run the Streamlit app
streamlit run app/main.py
```

## Quick Start

### API Usage

```python
from sqldeps.llm_parsers import create_extractor

# Create extractor with default settings (framework="Groq" and model="llama-3.3-70b-versatile")
extractor = create_extractor()

# Extract dependencies from a SQL query
sql_query = """
SELECT u.name, u.email, o.order_date
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed'
"""
dependencies = extractor.extract_from_query(sql_query)

# Or extract from a file
dependencies = extractor.extract_from_file('path/to/query.sql')

# Print results
print(dependencies.to_dict())
```

### CLI Usage

For command line usage:

```bash
sqldeps path/to/query.sql
```

Basic example with default settings (Groq with llama-3.3-70b-versatile):
```bash
sqldeps data/examples/db_examples/cainas_query.sql
```

Specifying parameters with database validation:
```bash
sqldeps \
    data/examples/db_examples/cainas_query.sql \
    --framework=deepseek \
    --db-match-schema \
    --db-target-schemas cainas \
    --db-credentials configs/database.yml \
    -o cainas_deps.csv
```

Process a folder recursively:
```bash
sqldeps \
    data/examples/folders_with_sql_files \
    --framework=openai \
    --model=gpt-4o-mini \
    -r \
    -o folder_deps.csv
```

### All CLI Options

```
$ sqldeps --help
                                                                                                                                            
 Usage: sqldeps [OPTIONS] FPATH                                                                                                             
                                                                                                                                            
 Extract SQL dependencies from file or folder.                                                                                              
 This tool analyzes SQL files to identify table and column dependencies, optionally validating them against a real database schema.         
                                                                                                                                            
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    fpath      PATH  SQL file or directory path [default: None] [required]                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --framework                                       TEXT  LLM framework to use [groq, openai, deepseek] [default: groq]                    │
│ --model                                           TEXT  Model name for the selected framework [default: None]                            │
│ --prompt                                          FILE  Path to custom prompt YAML file [default: None]                                  │
│ --recursive           -r                                Recursively scan folder for SQL files                                            │
│ --db-match-schema         --no-db-match-schema          Match dependencies against database schema [default: no-db-match-schema]         │
│ --db-target-schemas                               TEXT  Comma-separated list of target schemas to validate against [default: public]     │
│ --db-credentials                                  FILE  Path to database credentials YAML file [default: None]                           │
│ --output              -o                          PATH  Output file path for extracted dependencies [default: dependencies.json]         │
│ --install-completion                                    Install completion for the current shell.                                        │
│ --show-completion                                       Show completion for the current shell, to copy it or customize the installation. │
│ --help                                                  Show this message and exit.                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Supported Models

| Framework | Model | Input Price ($/1M tokens) | Output Price ($/1M tokens) |
|-----------|-------|---------------------------|----------------------------|
| Groq      | gemma2-9b-it | 0.20 | 0.20 |
| Groq      | llama-3.3-70b-versatile (default) | 0.59 | 0.79 |
| Groq      | llama-3.1-8b-instant | 0.05 | 0.79 |
| Groq      | mixtral-8x7b-32768 | 0.24 | 0.24 |
| Groq      | deepseek-r1-distill-llama-70b | 0.75 | 0.99 |
| OpenAI    | gpt-4o | 2.50 | 10.00 |
| OpenAI    | gpt-4o-mini | 0.15 | 0.60 |
| DeepSeek  | deepseek-chat | 0.27 | 1.10 |

For up-to-date pricing details, please check: [Groq](https://groq.com/pricing/), [OpenAI](https://platform.openai.com/docs/pricing), [DeepSeek](https://api-docs.deepseek.com/quick_start/pricing).

## Example of Use Cases

### Project Documentation

For large projects with many SQL files, you can use SQL Dependency Extractor to generate comprehensive documentation of database dependencies:

```bash
# Scan an entire project directory recursively
sqldeps /path/to/project -r -o project_dependencies.json

# Or process specific folders with SQL queries
sqldeps /path/to/project/queries -r --db-match-schema -o project_db_report.csv
```

This documentation helps teams understand exactly which database objects are required by their code, making schema changes safer and migrations more predictable.

## Example Output

The tool extracts dependencies in a structured format:

```json
{
  "tables": [
    "customers",
    "orders",
    "products"
  ],
  "columns": {
    "customers": [
      "customer_id",
      "email",
      "name"
    ],
    "orders": [
      "customer_id",
      "order_date",
      "order_id",
      "product_id"
    ],
    "products": [
      "name",
      "price",
      "product_id"
    ]
  }
}
```

## Testing

Run unit tests:
```bash
pytest -vv
```

You can specify custom framework, models, and SQL files for testing. Please refer to [merge request !13](https://gitlab.com/gibbs-lab/database/sql-dependency-extractor/-/merge_requests/13) for details.

## Current Limitations

- Currently, only hosted LLMs are available for usage
- Currently, only PostgreSQL is supported for schema validation

## Roadmap

- Annotate more SQL files to re-evaluate model performance
- Implement support for more SQL dialects (MySQL, etc.)
- Add feature to allow user integration of local & hosted LLMs through custom Python code using `BaseSQLExtractor`
- Allow users to use specific SQL dialect connections through custom Python code using `SQLBaseConnector`

## License

TBD
