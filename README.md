# Just plugin

[![Validate](https://github.com/just-done/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/just-done/skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Just Domain is a domain registrar. This plugin, for Claude Code and Cowork, proposes
names for the business you are building, checks whether the matching domain names are
available and what registering and renewing each one costs, and hands you a link to
register the one you choose on justdomain.ai. It can also check whether a domain you
already own at another registrar could move to Just Domain.

Registration happens on justdomain.ai: you sign in and pay there, in your browser. No
order is placed and no payment is taken in the chat.

> **Important**: This plugin checks domain availability and pricing. A domain being
> available is not a company registration, a trademark clearance or legal advice.
> Registration, payment, renewals and moving a domain out happen on justdomain.ai in
> your browser, never in the chat; moving a domain in is arranged with support.

Just Domain is operated by Just Done LLC. The bundled server is the Just Domain connector
listed in the Claude Connectors Directory and in the MCP Registry as
`ai.justdomain/just-domain`.

## Installation

### Claude Code

```
/plugin marketplace add just-done/skills
/plugin install just@just-skills
/reload-plugins
```

## What you'll need to connect

Nothing. The plugin connects to the hosted Just Domain MCP server at
`https://mcp.justdomain.ai/` with no account, key or sign-in. You sign in on
justdomain.ai only when you register a name, in your browser.

## How it works

Two read-only tools and two skills. `search_domains` returns availability, the
registration and renewal price for one full term, and a registration link for available
names. `check_domain_transfer` is a transfer precheck for one domain you already own.
The skills describe when to use each tool, how to present the results and where to stop.

## Skills

| Skill | What it does | Example requests |
| --- | --- | --- |
| `/just:find-a-name` | Proposes names for your business or project, checks the exact domains for your shortlist in one call, and gives you a link to register the one you pick. | "I need a name for my business", "find me a name and a domain for my bakery" |
| `/just:just-domain` | Checks specific domains: available or taken, first-term price, renewal, and a link to register. Checks whether a domain you own elsewhere could move to Just Domain: blockers, current registrar, DNS continuity and transfer price. | "is acme.com available", "check acme.io and acme.ai", "can I move my domain to Just Domain" |

## Example prompts

- "Is brightcrumb.co available, and what does it cost?"
- "I'm opening a sourdough bakery in Austin. Help me find a name and a domain."
- "Check acme.com, acme.io and acme.ai and tell me which ones I can register."
- "Can I move example.org to Just Domain, and what would it cost?"

## What costs money and where you pay

Every check needs no account and costs nothing. The only paid step is registering (and
later renewing) a domain, and that happens on justdomain.ai in your browser. Prices are
shown as totals for one full registration term of that ending: one year on most endings,
two years on .ai.

## What this plugin will never do

- Place an order, take a payment or reserve a name. There is no purchase tool on the
  server.
- Renew a domain, change DNS or nameservers, or report your renewal schedule; those live
  in your dashboard on justdomain.ai.
- Start a transfer. It reports whether a domain could move and what it would cost; the
  move itself is arranged by Just Domain support (support@just-done.ai).
- Request, hold or relay an authorization (EPP) code. Unlocking a domain and issuing its
  code are owner actions in a browser; no assistant is ever handed a code.
- Give trademark, legal or brand-conflict advice, look up who owns a taken domain, or
  value a domain.

## MCP server

| Server | Endpoint | Sign-in | Tools |
| --- | --- | --- | --- |
| `just-domain` | `https://mcp.justdomain.ai/` | none | `search_domains`, `check_domain_transfer` (both read-only) |

The server also exposes the prompts `jd-check` and `jd-transfer-check` and the resources
`domain://faq` and `ui://just-domain/search-results-v4.html`, which Claude Code lists
automatically.

## Privacy and data

The only network destination is the hosted Just Domain MCP server (`mcp.justdomain.ai`).
The plugin sends the domain names you ask about and, like any web request, your client's
network address and user agent reach the server; the plugin itself sends no telemetry.
The server keeps short-lived operational logs, and the registration link it returns
carries a pseudonymous identifier (a one-way hash, never a raw address) so that a later
registration can be attributed to the search. Both are described in the privacy policy:
https://justdomain.ai/privacy

## Troubleshooting

- **Tools are not listed.** In Claude Code, run `/reload-plugins` and check `/mcp` for
  `plugin:just:just-domain`. In other clients, restart the session.
- **The connector shows as Custom.** The server URL must be exactly
  `https://mcp.justdomain.ai/`.
- **The registration link asks you to sign in.** This is expected. You return to the
  checkout page afterwards, and opening the link does not charge anything.

## Support

- Questions about registrations, payments or your account: support@just-done.ai
- Documentation: https://justdomain.ai/docs/mcp
- Bugs and feature requests: [GitHub issues](https://github.com/just-done/skills/issues)

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull
request, and follow the [Code of Conduct](CODE_OF_CONDUCT.md). To report a security issue,
see [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE). Just, Just. and Just Domain are trademarks of
Just Done LLC; the license covers the contents of this repository, not the trademarks.
