# Security Policy

## Supported versions

Security fixes are released for the latest version of the plugin. Please update to the most
recent release before reporting an issue.

| Version | Supported |
| ------- | --------- |
| 0.2.x   | Yes       |
| 0.1.x   | No        |

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
checks that validate them. The plugin runs no code of its own and stores no credentials; the
client keeps the Just Publish sign-in.

In scope:

- Skill text that could lead an assistant to request, store or relay an authorization code
  or other credential, to misstate what is charged or registered, to publish or replace
  files the user did not ask to put online, or to follow hidden or injected instructions.
- Configuration that could point the plugin anywhere other than https://mcp.justdomain.ai/
  and https://mcp.justpublish.ai/claude.

The plugin connects to two hosted MCP servers. The Just Domain server is public, requires
no authentication and is read-only. The Just Publish server requires the user to sign in and
publishes and edits that user's sites. Vulnerabilities in either server, on justdomain.ai
or on justpublish.ai can be reported to the same address.
