# Installation Guide

This guide covers how to install the OpenCRM Python client in your projects.

## Using uv

### Local Path Dependency

For projects on the same machine, add the library by path:

```bash
cd /path/to/your/project
uv add /path/to/opencrm_api
```

This adds to your `pyproject.toml`:

```toml
[project]
dependencies = [
    "opencrm @ file:///path/to/opencrm_api",
]
```

### Editable Install (Recommended for Development)

If you're actively developing the library and want changes to reflect immediately without reinstalling:

```bash
cd /path/to/your/project
uv add --editable /path/to/opencrm_api
```

This creates an editable install in your `pyproject.toml`:

```toml
[project]
dependencies = [
    "opencrm",
]

[tool.uv.sources]
opencrm = { path = "/path/to/opencrm_api", editable = true }
```

### Git Dependency

Once the library is pushed to a Git repository:

```bash
uv add git+https://github.com/yourorg/opencrm-python
```

Or manually in `pyproject.toml`:

```toml
[project]
dependencies = [
    "opencrm @ git+https://github.com/yourorg/opencrm-python",
]
```

For a specific branch or tag:

```toml
[project]
dependencies = [
    "opencrm @ git+https://github.com/yourorg/opencrm-python@main",
    # or
    "opencrm @ git+https://github.com/yourorg/opencrm-python@v0.1.0",
]
```

### From PyPI (Future)

Once published to PyPI:

```bash
uv add opencrm
```

## Using pip

### Local Install

```bash
pip install /path/to/opencrm_api
```

### Editable Install

```bash
pip install -e /path/to/opencrm_api
```

### From Git

```bash
pip install git+https://github.com/yourorg/opencrm-python
```

## Verifying Installation

After installation, verify everything works:

```bash
uv run python -c "from opencrm import OpenCRMClient, query; print('OpenCRM client installed successfully!')"
```

Or in a Python script:

```python
from opencrm import OpenCRMClient, query

# Check version
import opencrm
print(f"OpenCRM version: {opencrm.__version__}")
```

## Quick Start After Installation

```python
from opencrm import OpenCRMClient, query

client = OpenCRMClient(
    system_name="yoursystem",
    api_key="your-api-key",
    pass_key="your-pass-key",
)

# List all leads
leads = client.leads.list()

# Filter with query builder
new_leads = client.leads.list(
    query=query().equals("leadstatus", "New")
)

client.close()
```

See the [README](../README.md) for complete usage documentation.
