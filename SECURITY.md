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

- Email: **security@just-done.ai**
- Policy: https://justdomain.ai/security and https://justdomain.ai/.well-known/security.txt

Include a description of the issue and its impact, the affected version, and the steps to
reproduce it. We acknowledge reports within two business days and keep you informed until
the issue is resolved. Please allow reasonable time for a fix before any public disclosure.

## Scope

This repository contains plugin manifests, skill instructions and documentation. It runs no
code of its own and stores no credentials. The plugin connects to the hosted Just Domain MCP
server at https://mcp.justdomain.ai/, which is public, requires no authentication and is
read-only. Vulnerabilities in that server or on justdomain.ai can be reported to the same
address.
