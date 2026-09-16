---
name: find-a-name
description: >-
  Proposes names for a new business, product or project and finds a domain for the
  one the user likes, with Just Domain, a domain registrar. Suggests candidate names,
  shortlists them with the user, checks the exact domains for the shortlist in one
  call, and hands back a link to register the chosen name on justdomain.ai. Use when
  the user says "I need a name for my business", "help me name my company", "find me
  a name and a domain for my bakery", "what should I call this", or has an idea but
  no name yet. Not a trademark or company-registry check. Read-only: nothing is
  ordered, reserved or paid in the chat.
license: MIT
---

# Find a name

Take the user from an idea to a name they like and a domain they can register, in one
conversation. You propose the names; the `search_domains` tool on the Just Domain MCP
server reports which exact domains are available and what they cost; the user registers
the one they choose on justdomain.ai in their browser. Nothing is ordered, reserved or
paid in the chat.

## Quick start

```
User: "I'm opening a sourdough bakery in Austin. Help me find a name and a domain."
-> Ask at most two questions you cannot infer (tone, audience), then move on
-> Propose 8 to 12 candidate names in three styles
-> Ask the user to shortlist 3 to 5 (or shortlist for them if they ask)
-> Build the exact domains: each shortlisted name times the endings that fit
-> Call search_domains once with the whole list in `domains`
-> Show one table: available names first, prices exactly as returned
-> When the user picks one: restate the facts, give its checkout_url last, stop
```

## Step 1 - Understand the business

Read what the user already wrote before asking anything. You need three things: what
the business does, who it is for, and the tone they want (playful, premium, plain). Ask
only for what is missing, in one message, two questions at most. If the user says "just
give me options", infer and go.

## Step 2 - Propose names

Propose 8 to 12 candidates, mixing styles so the user can react to a direction and not
just a word:

- Descriptive: says what the business does (Austin Sourdough Co).
- Compound or evocative: two real words that carry the feeling (Bright Crumb, Ember Bakes).
- Coined: a short invented word that is easy to say and spell.

Rules of the craft:

- Short, pronounceable, spellable after hearing it once. No hyphens, no digits unless
  they mean something to the user.
- Prefer names that stay meaningful as one bare word, because the domain will be that
  word plus an ending.
- Do not call a name "available" before the tool has answered. Names are proposals;
  availability is a tool result.

Ask the user to shortlist 3 to 5. If they ask you to pick, pick 3 and say why in one
line each, about the name and not about price.

## Names that belong to someone else

If a proposed or requested name is, or is built on, a well-known company, product or
personal brand the user has not said they own (for example google, nike, tesla, and
compounds like nikeshoes), do not propose it. If the user asks for one, say plainly that
a domain being available is not a right to use that name, that you cannot judge
trademark or brand conflicts, and ask whether they hold the rights to it. Check it and
hand over a link only after the user says they do. Never look up who owns a taken name.

## Step 3 - Build the exact domains

A domain check needs fully-qualified names. Turn each shortlisted name into domains:

- Lower-case, spaces and punctuation removed: "Bright Crumb" becomes `brightcrumb`.
- Endings: if the user named endings, use those. If not, draw from the endings that
  registered with a link in recent checks (com, net, co, io, ai, dev, app, xyz, shop,
  store, cafe, pizza), pick the three or four that fit, and say in one sentence which
  you chose and why. A local shop may not need `.io`; a developer tool may not need
  `.co`. An ending outside that pool may come back as `not_offered`.
- Keep the batch readable: up to 5 names times 4 endings, 20 domains in one call. The
  tool accepts up to 200, but a table longer than about 40 rows stops helping; run a
  second round instead.

Prefer the `domains` argument (an array of exact names). Use `query` only when the user
typed one bare word and wants "the usual endings"; the server then expands it to com,
io, ai, co and net.

## Step 4 - Call the tool once

Call `search_domains` with `domains` set to the whole list. One call per shortlist. Do
not check names one at a time, and do not check names the user has not shortlisted
unless they asked for a wide sweep.

## Step 5 - Read the result

First compare the names you sent with the `fqdn` values that came back. A name the
server could not parse is dropped from `results` and reported in the top-level
`warnings`; tell the user which names were not checked and why. A missing row is
neither taken nor available.

Each entry in `results` carries what you need:

- `available` (true or false) and `premium` (true or false).
- `price.formatted` and `renewal_price.formatted`: totals for one full registration
  term, not per-year rates.
- `term_years`: how long that term is. 1 on most endings, 2 on `.ai`.
- `checkout_url`: present only on available, non-premium names Just Domain can register
  today.
- `warnings`: machine codes for that row. `requires_additional_data` means the registry
  asks for registrant details Just Domain cannot collect yet: the name is available but
  has no link. `not_offered` means Just Domain does not offer that ending: do not call
  the name taken. `premium_not_supported` and `renewal_price_unavailable` are plain
  facts about the row. Show a code you do not recognise as a note.

`alternatives` (top level) is an always-present list that is normally empty. It can be
non-empty only when every requested name is taken and the server looked at other
endings for the same label; each entry then carries its own prices and a `checkout_url`.
When it is non-empty, show it under its own heading, "The tool also found these
available". Never present an ending the response did not return.

## Step 6 - Present one table

Available names first, then taken names in one short line each. Columns:
Domain | Status | First term | Renews | Notes.

Price discipline, without exception:

- Every figure comes from this tool response and nothing else. No price from memory, no
  estimate, no rounding. If a price is missing, write "price not returned" and move on;
  never fill it in.
- First term: "{price.formatted} for 1 year" or "{price.formatted} for 2 years", from
  `term_years`.
- Renewal, two forms only: when `term_years` is 1, "renews at {renewal_price.formatted}/yr";
  when it is greater than 1, "renews at {renewal_price.formatted} every {term_years} years".
  Never write "/yr" on a multi-year term, and never divide a total to make a per-year
  figure.
- Report prices as facts. No "cheap", "a steal", "expensive".
- A premium name: say it cannot be registered through Just Domain yet. Do not offer a
  way around it.

If the user wants your opinion, give it about the name (memorable, easy to spell, fits
the tone), not about the price, and do not call a name "safe" or "clear".

## Step 7 - Hand over the link and stop

When the user picks a name, send exactly this, with the link as the last line. The first
line uses the two fixed forms from Step 6:

```
{fqdn} is available: {first-term form}, {renewal form}.
Here is the link to register it on justdomain.ai: {checkout_url}
You sign in and pay there, in your browser. Nothing is ordered or charged here, and the name is not reserved for you until you finish checkout.
```

Present the link as a link for the user to open. Do not try to open a browser or run a
command for the user; in some hosts the assistant runs in a sandbox and the user's
browser is out of reach. The tool reported availability at lookup time and it can
change. After the link, stop: no second call to action, no new check.

## When every name is taken

- Show `alternatives` if the tool returned any.
- Offer three kinds of variation, then check the new shortlist in one call: a modifier
  (get, try, hq, app, studio, co), a different second word, or a different ending the
  user is happy with.
- Do not look up who owns a taken name, do not guess at the owner, and do not suggest
  buying the name from its owner or from a marketplace.

## What never happens in the chat

- No order, no payment, no reservation. Registration completes on justdomain.ai in the
  user's browser.
- No claim that a name is reserved or registered until the user says checkout is
  complete.
- No trademark, legal or brand-conflict advice. Domain availability is not a trademark
  clearance, and a domain is not a company registration.
- No WHOIS, RDAP or owner research on taken names; no domain valuation; no aftermarket
  or broker suggestions.
- No hand-written list of "good endings" presented as fact; the tool's response is the
  only source of what is registrable.
- No prices from memory.
- Renewals, DNS and transfers are other topics: renewals and auto-renew live in the
  owner's dashboard on justdomain.ai; for moving a domain the user already owns, use the
  just-domain skill in this plugin.

## If the tool is missing or fails

- Tool not available: tell the user the Just Domain connector is not connected in this
  session, that the plugin needs to be enabled in the client's plugin settings, and
  that the session then needs a restart. Do not guess availability.
- Tool error: report the error text as returned, in one sentence, and offer to retry or
  to check fewer names. An error that starts with `[invalid_query]` means no name in the
  request could be parsed; ask for full names with endings.
- `error` set on the response: show `error_message`; do not treat the rows as valid.

## Reference

- The just-domain skill in this plugin covers single-domain checks, the transfer
  precheck and the full field reference (`skills/just-domain/references/mcp-api.md`).
- Resource `domain://faq` on the server holds current factual answers on pricing terms,
  WHOIS privacy, DNS, refunds, renewals, transfers and what is not supported yet.
- https://justdomain.ai/docs/mcp for humans.
