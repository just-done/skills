# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `find-a-name` checks each shortlisted name against the trademark registers with
  `check_trademark` before it checks domains. It shows the verdict, the conflicting marks
  and the date each register was read, and drops a name with an exact live mark unless the
  user holds the rights to it. On a server without `check_trademark`, it uses the Open
  Trademarks API.

## [0.2.0] - 2026-10-18

### Added

- `just-publish` skill: publishes a static website to a live link with Just Publish, lists
  the user's sites, reads a site's files and edits only the files that change, and explains
  how to connect a custom domain from the dashboard. A user without a domain is sent to the
  `just-domain` skill to find and register one.
- Connection to the hosted Just Publish MCP server (`deploy`, `list_sites`,
  `get_site_files`, `update_site_file`) over Streamable HTTP. It requires a one-time
  sign-in to Just Publish.

### Changed

- The plugin and marketplace descriptions and keywords now cover publishing as well as
  domains.
- The metadata checks accept both MCP servers and require the registration hand-off block
  only in the skills that register a domain.

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

[0.2.0]: https://github.com/just-done/skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/just-done/skills/releases/tag/v0.1.0
