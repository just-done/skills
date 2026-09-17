# Just.

[![Validate](https://github.com/just-done/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/just-done/skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Find a name and a domain for the business you are building. Ask Claude in plain words:
Just Domain checks which domain names are available, shows what each costs to register
and renew, and gives you a link to register the one you choose on justdomain.ai.

- **No account needed to search.** Install the plugin and ask.
- **Nothing is bought in the chat.** You register and pay on justdomain.ai, in your browser.
- **Already own a domain?** Ask whether anything blocks moving it to Just Domain and what
  the move costs.

> **Important**: A domain being available is not a trademark clearance, a company
> registration or legal advice.

Just Domain is operated by Just Done LLC. The plugin uses the same server as the
[Just Domain connector](https://claude.ai/directory/connectors/just-domain) in the Claude
Connectors Directory, published in the MCP Registry as
[`ai.justdomain/just-domain`](https://registry.modelcontextprotocol.io/v0/servers/ai.justdomain%2Fjust-domain/versions/latest).

## Installation

### Claude Code

```
/plugin marketplace add just-done/skills
/plugin install just@just-skills
/reload-plugins
```

### Cowork

1. In the Claude app or on claude.ai, open **Customize**, then **Plugins**.
2. Choose **Add**, then **Add marketplace**. Enter `just-done/skills` and choose **Sync**.
3. Install **Just.** from the marketplace and make sure it is turned on.

## What you'll need to connect

Nothing. The plugin connects to the hosted Just Domain MCP server at
`https://mcp.justdomain.ai/` with no account, key or sign-in. You need an account on
justdomain.ai only when you register a name, in your browser.

## How it works

Ask in plain words, in Claude Code or Cowork. Claude checks the domains with the Just
Domain server and shows which are available and what each costs to register and renew.
When you pick one, you get a link to register it: you create an account or sign in, then
pay on justdomain.ai. The server's two tools, `search_domains` and
`check_domain_transfer`, are read-only: neither can place an order or change a domain.

## Skills

Claude uses a skill when your request matches it, or you can run one by name.

| Skill | What it does |
| --- | --- |
| `/just:find-a-name` | Suggests names for your business, checks their domains, shows which ones you can register and gives you a link to register the one you pick. |
| `/just:just-domain` | Checks specific domains: whether each is available, what it costs to register and renew, and a link to register it. Also checks whether anything blocks moving a domain you own elsewhere to Just Domain, and what the move costs. |

## Example prompts

- "Is brightcrumb.co available, and what does it cost?"
- "I'm opening a sourdough bakery in Austin. Help me find a name and a domain."
- "Check acme.com, acme.io and acme.ai and tell me which ones I can register."
- "Can I move acme.com to Just Domain, and what would it cost?"

## What costs money and where you pay

Checking names is free and needs no account. You pay only to register a domain, and later
to renew it, on justdomain.ai in your browser. Prices are totals for one registration
term: one year on most endings and longer on a few, such as .ai; every result states its
term.

## What this plugin does not do

- Place an order, take a payment or reserve a name. There is no purchase tool on the
  server.
- Renew a domain, change DNS or nameservers, or report your renewal schedule; those live
  in your dashboard on justdomain.ai.
- Start a transfer. It reports whether anything blocks moving a domain and what the move
  would cost; the move itself is arranged by Just Domain support (support@just-done.ai).
- Request, hold or relay an authorization (EPP) code. Unlocking a domain and issuing its
  code are owner actions in a browser; no assistant is ever handed a code.
- Give trademark, legal or brand-conflict advice, look up who owns a taken domain, or
  value a domain.

## MCP server

| Server | Endpoint | Sign-in | Tools |
| --- | --- | --- | --- |
| `just-domain` | `https://mcp.justdomain.ai/` | none | `search_domains`, `check_domain_transfer` (both read-only) |

The server also offers two prompts, `jd-check` and `jd-transfer-check`, and an FAQ
resource, `domain://faq`.

## Privacy and data

The plugin runs no code of its own and connects to one place: the Just Domain server at
`mcp.justdomain.ai`. When you ask about a domain, Claude sends the names to that server,
which, like any web service, also receives your network address and user agent. For each
search, the server sends these to our product analytics: the names checked, how many
results came back and whether any were available, which assistant and version made the
request, an identifier for that chat session, and a pseudonymous identifier derived from
your network address and user agent. Failed searches and request diagnostics also go to
our error monitoring, and the server keeps operational logs. The registration link
carries the same pseudonymous identifier: if you open it and sign in, the searches
recorded under it are linked to your account in our analytics. See the
[privacy policy](https://justdomain.ai/privacy), and send privacy requests to
privacy@just-done.ai.

## Troubleshooting

- **Tools are not listed.** In Claude Code, run `/reload-plugins`, then check `/mcp` for
  `plugin:just:just-domain`. In Cowork, open **Customize**, then **Plugins**, and check that
  **Just.** is turned on and its Just Domain connector shows **Connected**.
- **Cowork asks before each search.** In **Manual** mode, Cowork asks before it uses a tool.
  Choose **Allow once**, or pick another mode for the task.
- **The registration link opens a sign-up page.** This is expected: create an account, or
  sign in if you already have one, and you return to checkout on justdomain.ai with the
  same domain. Opening the link does not charge anything.

## Support

- Questions about registrations, payments or your account: support@just-done.ai
- Documentation: https://justdomain.ai/docs/mcp
- Bugs and feature requests: [GitHub issues](https://github.com/just-done/skills/issues)

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull
request, and follow the [Code of Conduct](CODE_OF_CONDUCT.md). To report a security issue,
see [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE). "Just", "Just." and "Just Domain" are
trademarks of Just Done LLC; the license covers the contents of this repository, not the
trademarks.
