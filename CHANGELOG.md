# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - Unreleased

### Added

- A portable Agent Plugins manifest (`plugin.json` and `mcp.json` at the root), read by
  Kiro as a Power and by Codex, with the Codex listing fields under `extensions.com.openai`.
  Just Publish connects at `https://mcp.justpublish.ai/`, where clients added by hand sign in.
- `gemini-extension.json` for the Gemini CLI extensions gallery, with both servers over
  Streamable HTTP.
- Cursor support: a Cursor manifest at `.cursor-plugin/plugin.json`, a Cursor marketplace
  file at `.cursor-plugin/marketplace.json` and a Cursor server list at `cursor/mcp.json`.
  In Cursor the plugin connects to Just Domain at `https://mcp.justdomain.ai/` and to Just
  Publish at `https://mcp.justpublish.ai/`, and sends `X-Cursor-Plugin: just` to both.
- The plugin logo at `assets/logo.png` and `assets/logo.svg`.
- Metadata checks for the Cursor files: the keys Cursor's schemas allow, parity with the
  Claude manifest, both server addresses and the header.

### Changed

- `trademark-check` no longer names the US, EU and Israeli registers as covered: its
  description speaks of the registers Open Trademarks has read, and its example reports a
  register that was not read yet. The README describes the trademark check the same way.
- The plugin and marketplace descriptions are shorter and name what each product does:
  Just Domain shows which domain names are available and both prices; Just Publish puts
  the site live at a public link.

## [0.3.0] - Unreleased

### Added

- A listing icon at `.claude-plugin/icon.png`.
- `trademark-check` skill: checks whether a name is taken as a trademark in the US, EU and
  Israeli registers with `check_trademark`, and reports the verdict, the conflicting marks,
  the classes they share and the date each register was read, with the answer's notice.
  It never calls a name clear unless it was checked in the conversation and the registers
  were read today or yesterday, and says plainly when a name could not be checked yet.

### Changed

- The plugin description leads with the business being built, and the homepage is
  https://just-done.ai, which covers both Just Domain and Just Publish.
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

[0.4.0]: https://github.com/just-done/skills/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/just-done/skills/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/just-done/skills/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/just-done/skills/releases/tag/v0.1.0
