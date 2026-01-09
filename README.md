# OpenCRM Python Client

A typed Python wrapper library for the [OpenCRM](https://opencrm.co.uk) REST API.

## Features

- Full type hints for IDE/LSP support
- Three authentication methods (API keys, headers, session)
- Fluent query builder for filtering
- Automatic pagination with `iterate()`
- Pydantic models for all CRM records
- Context manager support

## Installation

```bash
pip install opencrm
# or with uv
uv add opencrm
```

## Quick Start

```python
from opencrm import OpenCRMClient, query

# Create client
client = OpenCRMClient(
    system_name="yoursystem",  # Your subdomain: yoursystem.opencrm.co.uk
    api_key="your-api-key",
    pass_key="your-pass-key",
)

# List leads
leads = client.leads.list()

# Get a specific contact
contact = client.contacts.get(crmid=12345)

# Create a new company
new_id = client.companies.create(
    accountname="Acme Corp",
    assigned_user_id=1,
)

# Update a record
client.contacts.update(crmid=12345, email="new@example.com")

# Always close when done
client.close()
```

### Using as Context Manager

```python
with OpenCRMClient(system_name="test", api_key="key", pass_key="pass") as client:
    leads = client.leads.list()
# Automatically closed
```

## Authentication

OpenCRM supports three authentication methods:

### 1. API Keys (Default)

Pass API key and pass key with each request:

```python
client = OpenCRMClient(
    system_name="yoursystem",
    api_key="your-api-key",
    pass_key="your-pass-key",
    auth_method="keys",  # This is the default
)
```

### 2. HTTP Headers

Pass credentials as HTTP headers (KEY1/KEY2):

```python
client = OpenCRMClient(
    system_name="yoursystem",
    api_key="your-api-key",
    pass_key="your-pass-key",
    auth_method="headers",
)
```

### 3. Session-based

Login once and use session access key:

```python
client = OpenCRMClient(
    system_name="yoursystem",
    api_key="your-api-key",
    pass_key="your-pass-key",
    auth_method="session",
)
```

## Filtering with Query Builder

Use the fluent query builder to filter results:

```python
from opencrm import query

# Exact match
new_leads = client.leads.list(
    query=query().equals("leadstatus", "New")
)

# Pattern matching
gmail_contacts = client.contacts.list(
    query=query().like("email", "%@gmail.com")
)

# Starts with
acme_companies = client.companies.list(
    query=query().begins_with("accountname", "Acme")
)

# Contains
urgent_tickets = client.helpdesk.list(
    query=query().contains("title", "urgent")
)

# Keyword search
results = client.leads.list(keywords="john smith")
```

### Available Query Operators

| Method | Operator | Description |
|--------|----------|-------------|
| `equals(field, value)` | `=` | Exact match |
| `like(field, value)` | `LIKE` | Pattern match (use `%` as wildcard) |
| `begins_with(field, value)` | `BEGINS` | Starts with |
| `ends_with(field, value)` | `ENDS` | Ends with |
| `contains(field, value)` | `CONTAINS` | Contains substring |

> **Note:** OpenCRM does not support negative queries (`!=`, `NOT LIKE`) or reliably
> chaining multiple conditions. For complex filtering, retrieve data and filter client-side.

## Pagination

### Manual Pagination

```python
# Get records 0-49
page1 = client.leads.list(limit_start=0, limit_end=50)

# Get records 50-99
page2 = client.leads.list(limit_start=50, limit_end=100)
```

### Automatic Iteration

For large datasets, use `iterate()` which handles pagination automatically:

```python
# Iterate all leads (fetches in batches of 100)
for lead in client.leads.iterate():
    print(lead["firstname"], lead["lastname"])

# With filtering
for contact in client.contacts.iterate(
    query=query().equals("mailingcountry", "UK"),
    batch_size=50,  # Custom batch size
):
    process_contact(contact)
```

### Count Records

```python
total = client.leads.count()
new_count = client.leads.count(query=query().equals("leadstatus", "New"))
```

## Available Resources

| Resource | Description |
|----------|-------------|
| `client.leads` | Lead records |
| `client.contacts` | Contact records |
| `client.companies` | Company/Account records |
| `client.projects` | Project records |
| `client.helpdesk` | Support ticket records |
| `client.opportunities` | Opportunity/Deal records |
| `client.products` | Product records |

Each resource supports these methods:

| Method | Description |
|--------|-------------|
| `list(query, keywords, limit_start, limit_end)` | List records with filtering |
| `get(crmid)` | Get a single record by ID |
| `create(**fields)` | Create a new record |
| `update(crmid, **fields)` | Update an existing record |
| `count(query, keywords)` | Count matching records |
| `iterate(query, keywords, batch_size)` | Iterate with auto-pagination |

## Field Names

OpenCRM uses different field names for different operations:

- **API Field Name**: Used when getting/setting record fields
- **Query String Name**: Used in `query_string` filters

For example, a Lead's assigned user:
- API Field Name: `smownerid`
- Query String Name: `assigned_user_id`

See [OpenCRM's field reference](https://help.opencrm.co.uk/article/20-rest-api-field-reference) for complete mapping.

### Common Fields

When creating records, always set `assigned_user_id` (the numeric user ID):

```python
client.leads.create(
    firstname="John",
    lastname="Doe",
    email="john@example.com",
    assigned_user_id=1,  # Required: record owner
)
```

## Error Handling

```python
from opencrm import OpenCRMClient
from opencrm.exceptions import (
    OpenCRMError,        # Base exception
    APIError,            # API returned an error
    AuthenticationError, # Authentication failed
    NotFoundError,       # Record not found (404)
    RateLimitError,      # Rate limit exceeded (429)
    ConfigurationError,  # Invalid client configuration
    ConnectionError,     # Network/connection error
)

try:
    contact = client.contacts.get(crmid=99999)
except NotFoundError:
    print("Contact not found")
except APIError as e:
    print(f"API error: {e.status_code} - {e.response_body}")
except OpenCRMError as e:
    print(f"Error: {e}")
```

## Configuration Options

```python
client = OpenCRMClient(
    system_name="yoursystem",     # Required: your OpenCRM subdomain
    api_key="your-api-key",       # Required: API key from OpenCRM
    pass_key="your-pass-key",     # Required: API pass key from OpenCRM
    auth_method="keys",           # "keys" | "headers" | "session"
    user_agent="my-app/1.0",      # Custom User-Agent (important!)
    timeout=60.0,                 # Request timeout in seconds
)
```

> **Important:** OpenCRM blocks the default `curl` User-Agent. This library
> automatically sets a custom User-Agent, but you can override it if needed.

## Type Checking

This library is fully typed and includes a `py.typed` marker for PEP 561 compliance.

```python
# mypy/pyright will catch type errors
client = OpenCRMClient(...)
lead: dict[str, Any] = client.leads.get(crmid=123)
```

## Development

```bash
# Clone and install
git clone https://github.com/yourorg/opencrm-python
cd opencrm-python
uv sync --extra dev

# Run tests
uv run pytest

# Type check
uv run mypy src

# Lint
uv run ruff check src
```

## Known Limitations

1. **No negative queries**: OpenCRM doesn't support `!=` or `NOT LIKE`
2. **Single filter only**: Multiple query conditions may produce inconsistent results
3. **No data validation**: The API accepts invalid data without error
4. **User-Agent blocking**: Default curl user agents are blocked by OpenCRM's WAF

## License

MIT
