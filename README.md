# finki-mcp

Model Context Protocol (MCP) servers for FINKI course management and public APIs.

## Structure

- **`local-mcp/`** - Course management MCP server
- **`public-mcp/`** - Submodule linking to [finki-public-apis](https://gitlab.finki.ukim.mk/wp/finki-public-apis)
- **`data/`** - Course participants and staff JSON files

## Quick Start

### Clone with submodules

```bash
git clone --recurse-submodules https://github.com/finki-hub/finki-mcp.git
cd finki-mcp
```

### Local development

```bash
cd local-mcp
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
python -m app.main
```

### Docker

```bash
docker-compose up -d
```

Server runs on `http://localhost:8808`

## Tools

- Get available courses (staff/participants)
- Get course staff/participants information
- Fuzzy query matching support

## Development

- **Language**: Python 3.13+
- **Type checking**: `mypy`
- **Linting**: `ruff`

## License

See [LICENSE](LICENSE) file.
