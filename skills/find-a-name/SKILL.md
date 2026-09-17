---
name: find-a-name
description: >-
  Proposes names for a new business or product and finds a domain for the one the user
  likes, with Just Domain (justdomain.ai). Suggests candidate names, checks their
  domains in one call, shows which can be registered, and hands back a link to register
  the chosen name on justdomain.ai. Use when the user says "I need a name for my
  business", "help me name my company", "find me a name and a domain for my bakery",
  "what should I call my business", or has a business or product idea but no name yet.
  Not a trademark or company-registry check. Read-only: nothing is ordered, reserved or
  paid in the chat.
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
-> Come up with 8 to 12 candidate names in three styles
-> Check every candidate on .com and the one other ending that fits best, in one call
-> Show the domains that can be registered; ask the user to shortlist 3 to 5
-> If the shortlist needs other endings, check them in one more call
-> When the user picks one: the three-line hand-off, link last, stop
```

## Step 1 - Understand the business

Read what the user already wrote before asking anything. You need three things: what
the business does, who it is for, and the tone they want (playful, premium, plain). Ask
only for what is missing, in one message, two questions at most. If the user says "just
give me options", infer and go.

## Step 2 - Come up with names

Come up with 8 to 12 candidates, mixing styles so the user can react to a direction and
not just a word:

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

## Names that belong to someone else

If a candidate or a requested name is, or is built on, a well-known company, product or
personal brand the user has not said they own (for example nike, tesla, disney, and
compounds like nikeshoes), do not propose it. If the user asks for one, say plainly that
a domain being available is not a right to use that name, that you cannot judge
trademark or brand conflicts, and ask whether they hold the rights to it. Check it and
hand over a link only after the user says they do. This plugin does not look up who owns
a taken name.

## Step 3 - Build the exact domains

A domain check needs fully-qualified names. Turn each candidate into domains:

- Lower-case, spaces and punctuation removed: "Bright Crumb" becomes `brightcrumb`.
- First call: each candidate on `.com` plus the one ending that fits the business best,
  up to 24 domains. If the user named endings, use those instead.
- Endings: pick from common choices (com, net, co, io, ai, dev, app, xyz, shop, store,
  cafe) and say in one sentence which you chose and why. A local shop may not need
  `.io`; a developer tool may not need `.co`. Only the response says whether an ending
  can be registered here; some country endings come back without a link.
- Keep a table readable: about 40 rows at most. The tool accepts up to 200 names, but a
  longer table stops helping.

Pass exact names in `domains`. Use `query` only for bare names separated by commas
("brightcrumb, emberbakes"), never with a sentence: the server treats every word as a
name and checks each on com, net, io, ai and co.

## Step 4 - Check, then shortlist

Call `search_domains` once with every candidate's domains in `domains`. Do not check
names one at a time.

Show the domains that can be registered (Step 6), grouped by candidate, and leave out a
candidate with nothing registrable unless the user asks about it. Ask the user to
shortlist 3 to 5. If they ask you to pick, pick 3 and say why in one line each, about the
name and not about price.

If the shortlist needs other endings, check them for the whole shortlist in one more call.

## Step 5 - Read the result

Compare the names you sent with the `fqdn` values returned. Top-level `warnings` explain
any difference:

- `invalid_entry:<reason>:<name>`: that name was not checked. Say which, and ask for a
  full name such as brightcrumb.com.
- `normalized:<name>:<fqdn>`: the server checked `<fqdn>` instead, as it does for a
  subdomain. Say so: a subdomain comes with its domain and is not registered on its own.
- `duplicate:<fqdn>`: the name was checked once.
- `chunk_failed:`: some names could not be checked right now. Name the ones with no row
  and offer to check them again.

A name with no row is neither taken nor available.

Give each row one status, checked in this order. Do not use the row's `status` field.

1. `not_offered` in the row's `warnings`: not offered. Just Domain does not offer that
   ending, whatever `available` says.
2. `available` is false: taken, whatever `premium` or the row's codes say.
3. `premium` is true: a premium name, not available through Just Domain.
4. No `checkout_url`: not available through Just Domain, for the reason the row's code
   gives.
5. Otherwise: available, with a link to register.

Row `warnings` describe the ending or the offer, never whether the name is taken. Never
show a code; use these words instead:

- `not_offered`: "ending not offered"
- `requires_additional_data`: "its registry needs owner details Just Domain doesn't
  collect"
- `restricted` or `demoted`: "registrations for this ending are paused"
- `requirements_unknown`: "this ending can't be registered right now"
- `premium_not_supported`: "premium name"
- `renewal_price_unavailable`: the renewal price was not returned (see Step 6)
- Any other code: "can't be registered right now"

Other fields on each row:

- `price.formatted` and `renewal_price.formatted`: totals for one full registration
  term, not per-year rates.
- `term_years`: how long that term is: 1 on most endings, 2 on a few, such as `.ai`.
- `checkout_url`: the browser link to register.

`alternatives` (top level) is always present and normally empty. It can be non-empty only
when every requested name is taken and the server looked at other endings for the same
label; each entry then carries its own prices and a `checkout_url`. Show those under the
heading "Also available with other endings", and never present an ending the response did
not return.

## Step 6 - Present the results

Show the domains that can be registered in one table. Columns: Domain | Price | Renews |
Notes. Plain words, no symbols or emoji. Below the table:

- One line for taken names, for example "Taken: brightcrumb.com, emberbakes.com."
- If any names can't be registered through Just Domain, one line with each name's reason,
  for example "Not available through Just Domain: bread.shop (premium name),
  brightcrumb.bank (ending not offered)."
- If any names were not checked, one line naming them.
- Once, the first time you show results: "An available domain doesn't mean you have the
  right to use the name for a business. Check for existing trademarks before you commit to
  it."

Price discipline, without exception:

- Every figure comes from this tool response and nothing else. No price from memory, no
  estimate, no rounding. Prices appear only for domains with a `checkout_url`; a price
  on any other row is not an offer.
- Price form: "{price.formatted} for 1 year" when `term_years` is 1, otherwise
  "{price.formatted} for {term_years} years".
- Renewal form: "{renewal_price.formatted}/yr" when `term_years` is 1, otherwise
  "{renewal_price.formatted} every {term_years} years". In the table, the form alone; in
  a sentence, "renews at" before it. If `renewal_price` is null, write "not returned".
  Never write "/yr" on a multi-year term, and never divide a total to make a per-year
  figure.
- If a price is missing, write "price not returned" and move on; never fill it in.
- Report prices as facts. No "cheap", "a steal", "expensive".

If the user wants your opinion, give it about the name (memorable, easy to spell, fits
the tone), not about the price, and do not call a name "safe" or "clear".

## Step 7 - Hand over the link and stop

When the user picks a name, send exactly these three lines, link last:

```
{fqdn} is available: {price form}, renews at {renewal form}.
You create an account or sign in, then pay on justdomain.ai, in your browser. Nothing is ordered, reserved or charged here. The price shown at checkout is the one that applies, and the name is registered to you only after checkout is complete and the registration is confirmed.
Link to register {fqdn}: {checkout_url}
```

If `renewal_price` is null, the first line is "{fqdn} is available: {price form}. The
renewal price was not returned."

Present the link as a link for the user to open. Do not try to open a browser or run a
command for the user; in some hosts the assistant runs in a sandbox and the user's
browser is out of reach. The tool reported availability at lookup time and it can
change. After the link, stop: no second call to action, no new check.

## When every name is taken

- Show `alternatives` if the tool returned any.
- Offer three kinds of variation, then check the new candidates in one call: a modifier
  (get, try, hq, app, studio, co), a different second word, or a different ending the
  user is happy with.
- This plugin does not look up or guess who owns a taken name and does not broker a
  purchase from its owner. If the user wants to pursue a taken name, say that this plugin
  can't help with that step and leave it to them.

## What never happens in the chat

- No order, no payment, no reservation. Registration completes on justdomain.ai in the
  user's browser.
- No claim that a name is reserved or registered, even after the user says checkout is
  complete; justdomain.ai reports when the registration is confirmed.
- No trademark, legal or brand-conflict advice. Domain availability is not a trademark
  clearance, and a domain is not a company registration.
- No WHOIS, RDAP or owner research, domain valuation or aftermarket brokering by this
  plugin.
- No hand-written list of "good endings" presented as fact; the tool's response is the
  only source of what is registrable.
- No prices from memory, and no error code or field name shown to the user.
- No promise that an ending or premium names will be supported later.
- Renewals, DNS and transfers are other topics: renewals and auto-renew live in the
  owner's dashboard on justdomain.ai; for moving a domain the user already owns, use the
  just-domain skill in this plugin.

## If the tool is missing or fails

- Tool not available: say "Just Domain isn't connected in this conversation, so I can't
  check names right now." Then give one next step that fits where you are running: in
  Claude Code, "Run /reload-plugins, then ask again."; anywhere else, "Turn on the Just
  plugin or the Just Domain connector in your settings, then start a new conversation."
  Do not guess availability.
- An error that starts with `[provider_unavailable]`, or a timeout: retry once without
  mentioning it. If it fails again, say "I couldn't check availability just now." and
  offer to try again.
- `[invalid_query]`: none of the entries could be read as a domain name. Ask for full
  names, for example "brightcrumb.com".
- Any other error: say "That check didn't go through." and offer to try again or to check
  fewer names.
- Never show a bracketed code or the raw error text; if the user asks what went wrong,
  say it in plain words. After an error, never call a name available or taken.

## Reference

- The just-domain skill in this plugin covers single-domain checks, the transfer
  precheck and the full field reference (`skills/just-domain/references/mcp-api.md`).
- Resource `domain://faq` on the server holds current factual answers on pricing terms,
  WHOIS privacy, DNS, refunds, renewals, transfers and what is not supported yet.
- Documentation: https://justdomain.ai/docs/mcp
