# Security Policy

## Supported versions

Security fixes are released for the latest version of the plugin. Please update to the most
recent release before reporting an issue.

| Version | Supported |
| ------- | --------- |
| 0.1.x   | Yes       |

## Reporting a vulnerability

Please report security issues privately. Do not open a public issue, pull request or
discussion for a suspected vulnerability.

- GitHub: [report a vulnerability privately](https://github.com/just-done/skills/security/advisories/new)
- Email: **security@just-done.ai**
- Policy: https://justdomain.ai/security and https://justdomain.ai/.well-known/security.txt

Include a description of the issue and its impact, the affected version, and the steps to
reproduce it. We acknowledge reports within 2 business days, aim to send an initial
assessment within 5 business days and keep you updated until the issue is resolved. Our
default disclosure window is 90 days from the initial report. Research done in good faith
and in line with the policy at https://justdomain.ai/security is covered by the safe harbor
described there. That safe harbor applies to Just Domain's own services only and does not
authorize testing Claude, GitHub or any other third-party service.

## Scope

This repository contains the plugin manifests, skill instructions, documentation and the CI
checks that validate them. The plugin runs no code of its own and stores no credentials.

In scope:

- Skill text that could lead an assistant to request, store or relay an authorization code
  or other credential, to misstate what is charged or registered, or to follow hidden or
  injected instructions.
- Configuration that could point the plugin anywhere other than https://mcp.justdomain.ai/.

The plugin connects to the hosted Just Domain MCP server, which is public, requires no
authentication and is read-only. Vulnerabilities in that server or on justdomain.ai can be
reported to the same address.
