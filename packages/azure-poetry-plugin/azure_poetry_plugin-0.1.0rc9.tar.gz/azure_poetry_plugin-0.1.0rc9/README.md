# Azure Poetry Plugin

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Tests](https://github.com/dgot/azure-poetry-plugin/actions/workflows/cicd.yaml/badge.svg)](https://github.com/dgot/azure-poetry-plugin/actions/workflows/cicd.yaml)

A poetry plugin for an easy way of configuring azure artifact feeds with Poetry, without any `.NET` dependencies.

## How to install

Poetry plugins are installable in two ways, via `pipx inject` or `poetry self`.

1. `pipx inject poetry azure-poetry-plugin`
2. `poetry self add azure-poetry-plugin`

## How to Use

With a complete url to the artifact feed

```bash
poetry azure add <index-url> --username <value> --access-token <value>
```

Or with the name of the `organization` and artifact `feed-name`.

```bash
poetry azure add --organization "<value>" --feed-name "<value>" --username "<email>" --access-token "<PAT>"
```

## How do i get an Access Token?

You can generate a personal access token by visiting your user profile in your organization on Azure DevOps:

```bash
https://dev.azure.com/$organization/_usersSettings/tokens
```

And click **[+ New Token]**"

### Permissions

The plugin requires the token to have `Packaging: [x] Read` access
