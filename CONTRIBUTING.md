# Contributing

Thank you for your interest in improving the Just plugin. This guide explains how the
repository is organized and what a pull request needs before it can be merged.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md). To report a
security issue, follow [SECURITY.md](SECURITY.md) instead of opening an issue.

## Ways to contribute

- **Report a bug.** Open an issue using the bug report form. Include the client and its
  version, the prompt you used and what happened.
- **Suggest an improvement.** Open an issue using the feature request form before starting a
  larger change, so the approach can be agreed first.
- **Submit a pull request.** Small, focused fixes to skill text and documentation are welcome
  directly.

## Repository layout

| Path                              | Purpose                                                          |
| --------------------------------- | ---------------------------------------------------------------- |
| `.claude-plugin/plugin.json`      | Plugin manifest                                                  |
| `.claude-plugin/marketplace.json` | Marketplace definition, so the repository can be installed directly |
| `.mcp.json`                       | The hosted Just Domain MCP server the plugin connects to         |
| `skills/<name>/SKILL.md`          | One skill per directory                                          |
| `.github/workflows/validate.yml`  | Checks that run on every pull request                            |
| `.github/scripts/`                | Helper scripts used by those checks                              |
| `.github/requirements.txt`        | Pinned Python tools for those checks                             |

## Prerequisites

- [Claude Code](https://code.claude.com/docs/en/overview), for the `claude` CLI
- Python 3.12 or later, with the pinned tools from `.github/requirements.txt`: PyYAML for the
  metadata checks and [skills-ref](https://github.com/anthropics/agentskills), the Agent Skills
  reference validator

```sh
python3 -m pip install --require-hashes -r .github/requirements.txt
```

## Validating a change

Run the same checks as CI before opening a pull request:

```sh
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate . --strict
for dir in skills/*/; do agentskills validate "$dir"; done
python3 .github/scripts/check_metadata.py
```

Both `claude plugin validate` commands must report `Validation passed` with no warnings.

## Testing locally

Load the plugin from your working copy in a terminal session:

```sh
claude --plugin-dir .
```

Run `/mcp` and confirm that `plugin:just:just-domain` is connected, then try the example
prompts from the [README](README.md). After editing a skill, run `/reload-plugins` to pick up
the change.

## Writing skills

- Limit frontmatter to `name`, `description` and `license`. The `name` must match the
  directory name.
- Keep descriptions to 1,024 characters or fewer, without `<`, `>`, `[` or `]`.
- Say what the skill does and when to use it, including phrases a user is likely to say.
- Refer to tools by their bare names, such as `search_domains`, so the same text works in
  every client.
- Describe only what the MCP server returns. Every price shown to a user must come from the
  tool response.
- Keep the registration hand-off wording identical across skills. CI checks this.
- Write in plain language, keep prices out of prose, and use hyphens rather than em dashes.

## Stable identifiers

The plugin name `just`, the marketplace name `just-skills`, the MCP server key `just-domain`
and the repository location are stable identifiers. Changing any of them breaks existing
installations, so pull requests that rename them cannot be accepted.

## Versioning and releases

The project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The version is
set in `.claude-plugin/plugin.json`.

- A pull request that changes anything under `skills/` or `.mcp.json` must bump the version
  and add an entry to [CHANGELOG.md](CHANGELOG.md). Installed copies update only when the
  version changes, and CI enforces the bump.
- The changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
- Releases are tagged `vX.Y.Z` on `main` and published as GitHub releases.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), for example
`fix(skills): use the two-year renewal form for .ai`. Keep the subject line under 72
characters and use the body to explain why the change is needed.

## Pull requests

- Keep each pull request focused on a single change, and complete the pull request template.
- All checks must pass before review.
- A maintainer reviews every pull request. Approved pull requests are squash-merged.

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
