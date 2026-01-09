# OpenCRM Python Client

Python wrapper library for the OpenCRM API.

## Installation

```bash
pip install opencrm
```

## Quick Start

```python
from opencrm import OpenCRMClient

client = OpenCRMClient(
    system_name="yoursystem",
    api_key="your-api-key",
    pass_key="your-pass-key",
)

# List leads
leads = client.leads.list()

# Get a specific contact
contact = client.contacts.get(crmid=12345)

# Create a new company
company = client.companies.create(
    accountname="Acme Corp",
    assigned_user_id=1,
)
```

## Authentication

Three authentication methods are supported:

1. **API Keys** (default): Pass `api_key` and `pass_key` to the client
2. **HTTP Headers**: Use `auth_method="headers"`
3. **Session-based**: Use `auth_method="session"` for access key authentication

## License

MIT
