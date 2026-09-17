# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-17

### Added

- `find-a-name` skill: proposes names for a business, checks their domains, shows which ones
  can be registered and returns a link to register the chosen name on justdomain.ai.
- `just-domain` skill: checks specific domains, reports the registration and renewal price
  for the full term, returns a registration link, and checks whether anything blocks moving
  a domain registered elsewhere to Just Domain.
- Connection to the hosted Just Domain MCP server (`search_domains`, `check_domain_transfer`)
  over Streamable HTTP.
- Marketplace definition for installing the plugin directly from this repository.

[0.1.0]: https://github.com/just-done/skills/releases/tag/v0.1.0
