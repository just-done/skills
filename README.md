# Just.

[![Validate](https://github.com/just-done/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/just-done/skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Find a name and a domain for the business you are building, and put its website online.
Ask Claude in plain words: Just Domain checks which domain names are available, shows what
each costs to register and renew, and gives you a link to register the one you choose on
justdomain.ai. Just Publish puts the site you built live at a public link, changes it when
you ask, and helps you connect your domain.

- **No account needed to search.** Install the plugin and ask.
- **Publishing is free.** Sign in to Just Publish once and every site is filed under your
  account.
- **Nothing is bought in the chat.** You register and pay on justdomain.ai, in your browser.
- **Is the name taken as a trademark?** Ask, and Claude searches the US, EU and Israeli
  trademark registers with [Open Trademarks](https://opentrademarks.org), showing the
  marks it found and the date each register was last read.
- **Already own a domain?** Ask whether anything blocks moving it to Just Domain and what
  the move costs, or connect it to your site.

> **Important**: A domain being available is not a trademark clearance. A trademark check
> is a register search, not legal advice, and neither is a company registration.

Just Domain and Just Publish are operated by Just Done LLC. The plugin uses the same
server as the [Just Domain connector](https://claude.ai/directory/connectors/just-domain)
in the Claude Connectors Directory, published in the MCP Registry as
[`ai.justdomain/just-domain`](https://registry.modelcontextprotocol.io/v0/servers/ai.justdomain%2Fjust-domain/versions/latest),
and the Just Publish server at `https://mcp.justpublish.ai/claude`.

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
3. Under **Discover**, choose **Add** next to **Just.**, and make sure it is turned on.

## What you'll need to connect

- **To search for domains:** nothing. The plugin connects to the hosted Just Domain MCP
  server at `https://mcp.justdomain.ai/` with no account, key or sign-in. You need an
  account on justdomain.ai only when you register a name, in your browser.
- **To publish a site:** a free Just Publish account. The first time Claude publishes, you
  sign in in your browser, with Google or a code sent to your email address. In Claude
  Code, run `/mcp`, select `plugin:just:just-publish` and sign in. A free account is
  created the first time you sign in.

## How it works

Ask in plain words, in Claude Code or Cowork.

- **Domains.** Claude checks the domains with the Just Domain server and shows which are
  available and what each costs to register and renew. When you pick one, you get a link
  to register it: you create an account or sign in, then pay on justdomain.ai.
- **Trademarks.** When you ask about a trademark, or shortlist names to name a business,
  Claude checks each name with `check_trademark` first. The Just Domain server's three
  tools, `search_domains`, `check_domain_transfer` and `check_trademark`, are read-only:
  none can place an order, change a domain or file a trademark.
- **Publishing.** Claude sends your site's files to the Just Publish server and gives you
  the live link, at `https://{name}.justpublish.site/`. To change a site later, Claude
  finds it under your account, reads the files that are live and writes only the ones
  that change. To use your own domain, you connect it from your dashboard on
  justpublish.ai; if you do not have one yet, Claude finds one with Just Domain first.

## Skills

Claude uses a skill when your request matches it, or you can run one by name.

| Skill | What it does |
| --- | --- |
| `/just:find-a-name` | Suggests names for your business, checks your shortlist against trademark registers, checks the domains of the names that remain, shows which ones you can register and gives you a link to register the one you pick. |
| `/just:just-domain` | Checks specific domains: whether each is available, what it costs to register and renew, and a link to register it. Also checks whether anything blocks moving a domain you own elsewhere to Just Domain, and what the move costs. |
| `/just:just-publish` | Publishes a static website to a live link, lists your sites, changes a site that is already live, and explains how to put it on your own domain. |
| `/just:trademark-check` | Checks whether a name is taken as a trademark in the US, EU and Israeli registers: the verdict, the marks it found, the classes they share and the date each register was last read. |

## Example prompts

- "Is brightcrumb.co available, and what does it cost?"
- "I'm opening a sourdough bakery in Austin. Help me find a name and a domain."
- "Check acme.com, acme.io and acme.ai and tell me which ones I can register."
- "Can I move acme.com to Just Domain, and what would it cost?"
- "Publish this site and give me the link."
- "Change the opening hours on my bakery site to 7 to 3."
- "Put my site on brightcrumb.co."
- "Is Brightcrumb taken as a trademark? It's for a bakery."

## What costs money and where you pay

Checking names, domains and trademarks is free and needs no account. You pay only to
register a domain, and later to renew it, on justdomain.ai in your browser. Prices are
totals for one registration term: one year on most endings and longer on a few, such as
.ai; every result states its term.

Publishing is free, for as many sites as you like. Connecting your own domain to a site
comes with Builder, the paid Just Publish plan for that site; see
[justpublish.ai/pricing](https://justpublish.ai/pricing). You start it from your
dashboard on justpublish.ai, in your browser.

## What this plugin does not do

- Place an order, take a payment or reserve a name. There is no purchase tool on either
  server.
- Connect a custom domain or change DNS records. You connect a domain from your Just
  Publish dashboard, which shows the records to add where the domain is registered.
- Host server code, databases or frameworks that need a server. Just Publish serves
  static files.
- Renew a domain, change DNS or nameservers, or report your renewal schedule; those live
  in your dashboard on justdomain.ai.
- Start a transfer. It reports whether anything blocks moving a domain and what the move
  would cost; the move itself is arranged by Just Domain support (support@just-done.ai).
- Request, hold or relay an authorization (EPP) code. Unlocking a domain and issuing its
  code are owner actions in a browser; no assistant is ever handed a code.
- Give legal or brand-conflict advice, or tell you a name is clear to use. A trademark
  check is a register search; it does not see unregistered use, state registers or logos.
- File, watch or oppose a trademark.
- Look up who owns a taken domain, or value a domain.

## MCP server

| Server | Endpoint | Sign-in | Tools |
| --- | --- | --- | --- |
| `just-domain` | `https://mcp.justdomain.ai/` | none | `search_domains`, `check_domain_transfer`, `check_trademark` (all read-only) |
| `just-publish` | `https://mcp.justpublish.ai/claude` | Just Publish account (OAuth) | `deploy`, `list_sites`, `get_site_files`, `update_site_file` |

The Just Domain server also offers two prompts, `jd-check` and `jd-transfer-check`, and an
FAQ resource, `domain://faq`.

## Privacy and data

The plugin runs no code of its own and connects to two places: the Just Domain server at
`mcp.justdomain.ai` and the Just Publish server at `mcp.justpublish.ai`.

When you ask about a domain or a trademark, Claude sends the names, and for a trademark
what you will sell, to the Just Domain server, which, like any web service, also receives
your network address and user agent. For each domain search, the server sends these to our
product analytics: the names checked, how many results came back and whether any were
available, which assistant and version made the request, an identifier for that chat
session, and a pseudonymous identifier derived from your network address and user agent.
Failed searches and request diagnostics also go to our error monitoring, and the server
keeps operational logs. The registration link carries the same pseudonymous identifier: if
you open it and sign in, the searches recorded under it are linked to your account in our
analytics. See the [Just Domain privacy policy](https://justdomain.ai/privacy).

If the server you reach does not offer `check_trademark` yet, Claude makes the same
trademark check with its web tool at `api.opentrademarks.org`, the Open Trademarks API,
which Just Done LLC also operates; that check is covered by the
[Open Trademarks privacy policy](https://opentrademarks.org/privacy).

When you publish, Claude sends your site's files to the Just Publish server, which puts
them online at a public link that anyone can open. Your sites are filed under the Just
Publish account you sign in with. The
[Just Publish privacy policy](https://justpublish.ai/privacy) describes what the server
records and who receives it.

Send privacy requests to privacy@just-done.ai.

## Troubleshooting

- **Tools are not listed.** In Claude Code, run `/reload-plugins`, then check `/mcp` for
  `plugin:just:just-domain` and `plugin:just:just-publish`. In Cowork, open **Customize**,
  then **Plugins**, and check that **Just.** is turned on and its Just Domain and Just
  Publish connectors show **Connected**.
- **Cowork asks before each search.** In **Manual** mode, Cowork asks before it uses a tool.
  Choose **Allow once**, or pick another mode for the task.
- **The registration link opens a sign-up page.** This is expected: create an account, or
  sign in if you already have one, and you return to checkout on justdomain.ai with the
  same domain. Opening the link does not charge anything.
- **Publishing asks you to sign in.** Just Publish files every site under your account.
  In Claude Code, run `/mcp`, select `plugin:just:just-publish` and sign in in your
  browser; sign in again there if your session has expired.

## Support

- Questions about registrations, payments, sites or your account: support@just-done.ai
- Documentation: https://justdomain.ai/docs/mcp and https://justpublish.ai/docs/mcp
- Bugs and feature requests: [GitHub issues](https://github.com/just-done/skills/issues)

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull
request, and follow the [Code of Conduct](CODE_OF_CONDUCT.md). To report a security issue,
see [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE). "Just", "Just.", "Just Domain" and "Just
Publish" are trademarks of Just Done LLC; the license covers the contents of this
repository, not the trademarks.
