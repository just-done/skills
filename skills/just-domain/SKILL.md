---
name: just-domain
description: >-
  Checks whether specific domain names are available and what registering and
  renewing each one costs, with Just Domain, a domain registrar, and returns a link
  to register an available name on justdomain.ai in the browser. Also checks whether a
  domain held at another registrar could move to Just Domain: what would block the
  move, who sponsors it today, whether DNS keeps working, and the full-term transfer
  price. Use when the user asks "is example.com available", "check example.io and
  example.ai", "what does this domain cost", "give me a link to register it", "can I
  move my domain to Just Domain" or "why won't my domain transfer". Read-only: it never
  orders, pays, renews, edits DNS, unlocks or transfers a domain in the chat, and never
  asks for or relays an authorization (EPP) code.
license: MIT
---

# Just Domain

Just Domain (https://justdomain.ai) is a domain registrar. This skill uses two read-only
tools on its MCP server:

- `search_domains`: availability and pricing for exact domain names, with a link to
  register the available ones.
- `check_domain_transfer`: a transfer precheck for one domain the user already holds at
  another registrar.

Both look up information only: no order is created, no payment is taken, and nothing
about anybody's domain is changed. Registration completes when the user opens the
returned link in a browser on justdomain.ai. To name a business from scratch, use the
find-a-name skill in this plugin; it ends by calling `search_domains` the same way.

## When this skill applies

The user says things like:

- "is acme.com available?" / "check acme.io and acme.ai"
- "what would acme.com cost?" / "how much is this domain?"
- "give me a link to register acme.com" / "buy acme.com" / "register acme.com": the
  action is to check the name and hand back the link; the user registers in the browser
- "can I move acme.com to Just Domain?" / "why won't my domain transfer?" / "what would
  it cost to transfer acme.ai in?" / "will my site and email keep working if I move it?"

## Quick start

```
User: "is brightcrumb.co available and what does it cost?"
-> search_domains with domains: ["brightcrumb.co"]
-> Read available, premium, price, renewal_price, term_years, checkout_url, warnings
-> Two lines: status, then "{price.formatted} for 1 year, renews at {renewal_price.formatted}/yr"
-> If the user wants it: the handoff block below, link last, stop
```

## Checking availability

### Inputs

- Fully-qualified names, each with its ending: `acme.com`, `acme.io`. Lower-case; strip
  spaces and a leading "www.".
- A bare word ("acme"): add the endings the user named, or `.com` plus one or two
  fitting endings, and check those. If the user pasted free text with bare names and
  wants "the usual endings", pass the text in `query`; the server expands each bare name
  to com, io, ai, co and net. Prefer `domains` whenever the endings are known.
- Many names: one call with all of them in `domains`. Up to 200 per call; keep one
  answer to about 40 rows so the table stays readable.
- If the user typed the command with names after it, treat that text as the list.

### Names that belong to someone else

If a requested name is, or is built on, a well-known company, product or personal brand
the user has not said they own (for example google, nike, tesla, and compounds like
nikeshoes), say plainly that a domain being available is not a right to use that name,
that you cannot judge trademark or brand conflicts, and ask whether they hold the rights
to it. Check it and hand over a link only after the user says they do. Never look up who
owns a taken name.

### Call

`search_domains` with `domains` (array of exact names) or `query` (free text). One call
per request. Nothing to configure and no sign-in: the server is public and read-only.

### Read the result

First compare the names you sent with the `fqdn` values returned. A name the server
could not parse is dropped from `results` and reported in the top-level `warnings`;
tell the user which names were not checked and why. A missing row is neither taken nor
available. If every entry was unparseable the tool returns an error instead (below).

Per entry in `results`:

- `available`: true means it can be registered right now; false means taken (`status`
  is `active`) or otherwise not registrable.
- `premium`: a registry-priced name. Just Domain does not register these yet, and the
  row carries no `checkout_url`.
- `price` and `renewal_price` (`formatted` is the display string): totals for one full
  registration term.
- `term_years`: the length of that term and the period both prices cover. 1 on most
  endings; 2 on `.ai`, whose registry mandates a two-year term with no one-year option.
- `checkout_url`: the browser link to register, present only on available, non-premium
  names Just Domain can register today.
- `warnings`: machine codes for the row. `requires_additional_data` means the registry
  asks for registrant details Just Domain cannot collect yet, so the name is available
  but has no link; `not_offered` means Just Domain does not offer that ending, so do not
  call the name taken whatever `available` says; `premium_not_supported` and
  `renewal_price_unavailable` are plain facts. Show a code you do not recognise as a
  note rather than dropping it.

Top level: `alternatives` is an always-present list that is normally empty; it can be
non-empty only when every requested name is taken and the server looked at other
endings for the same label, and each entry then carries its own prices and a
`checkout_url`. Show them under their own heading only when the list is non-empty, and
never present an ending the response did not return. `error` and `error_message`: when
set, show the message and treat the rows as absent.

## Presenting results

- One name: two lines. Status, then price and renewal in the fixed forms below. Then, if
  the user wants it, the handoff block.
- Several names: one table, available first. Columns: Domain | Status | First term |
  Renews | Notes.
- Fixed forms. First term: "{price.formatted} for 1 year" or "{price.formatted} for
  2 years". Renewal: "renews at {renewal_price.formatted}/yr" when `term_years` is 1;
  "renews at {renewal_price.formatted} every {term_years} years" when it is more.
  Never write "/yr" on a multi-year term. Never divide or multiply a returned figure.
- Every number comes from this response. A missing price is "price not returned", never
  filled in from memory.
- Facts, not adjectives: no "cheap", no "great deal".
- Premium: "premium name; cannot be registered through Just Domain yet".
- Available with no `checkout_url` and not premium: say what the row's warning says,
  for example "available, but this ending needs registrant details Just Domain cannot
  collect yet".

## Registering an available name

Registration is a browser step, never a chat step. When the user wants a name, send
exactly this, with the link as the last line. The first line uses the two fixed forms:

```
{fqdn} is available: {first-term form}, {renewal form}.
Here is the link to register it on justdomain.ai: {checkout_url}
You sign in and pay there, in your browser. Nothing is ordered or charged here, and the name is not reserved for you until you finish checkout.
```

Present the link as a link for the user to open. Do not try to open a browser or run a
command for the user; in some hosts the assistant runs in a sandbox and the user's
browser is out of reach. Do not claim the domain is reserved or purchased until the user
says they finished checkout; the tool reported availability at lookup time and it can
change. After the link, stop.

## Checking a transfer

1. Take one fully-qualified domain the user already owns at another registrar. One per
   `check_domain_transfer` call; each call reads a third-party registry. If the user
   lists several, check them one at a time and say so.
2. Read `supported` and `blockers` before anything else. When `supported` is false or a
   `tld_unsupported` blocker is present, the ending cannot be moved to Just Domain today:
   say so and do not quote a price, even if one is returned. Otherwise an EMPTY
   `blockers` list is the only thing that means the domain is ready to move. Every entry
   has `code`, a plain `detail` sentence and sometimes `eligible_at`. Show `detail` as
   written, including for a code you do not recognise; dropping a blocker you have no
   wording for is how a domain in `pendingDelete` gets reported as ready.
3. Read `source`. If `source.rdap` is false the registry did not answer, so nothing was
   established: say the check could not be completed. Never say "ready" in that case.
4. `registrar` (`name`, `iana_id`): who sponsors the domain today, as the registry
   reports it.
5. `price`: `amount` and `currency` cover `term_years` years, a total, not a per-year
   rate. Quote `term_note` beside it. A `.ai` transfer adds and charges two years because
   its registry works in two-year units; never halve that figure. `expected_new_expiry`
   is a projection from the registry's current expiry, not a confirmed date. A null
   `price` means the price could not be read, which is not the same as free.
6. `dns_continuity.case`: `independent` means the nameservers belong to a DNS provider
   and the move does not touch them; `losing_registrar` means the old registrar
   eventually stops serving the zone and the site or mail breaks late and quietly;
   `unknown` means the nameservers were not recognised, so do not guess. Quote `detail`.
7. Hand over `next_step` and `transfer_url` as a link. Moving a domain in is not
   self-service yet; a person arranges it, and the route is support@just-done.ai. Do not
   describe a payment step for that page or promise what it will do.
8. Verdict line first: "Ready to move" only when `supported` is true, `blockers` is
   empty and `source.rdap` is true; otherwise "Not ready yet: " followed by the first
   blocker's `detail`. Then registrar, DNS continuity in one sentence, the price with its
   term note (when the ending is supported), the expected new expiry as a projection,
   then `next_step` and the link. Stop.

## The one refusal

There is no agent path to unlocking a domain or to obtaining an authorization (EPP)
code. Not through this skill, not through the MCP server, not through any Just Domain
API. An authorization code is a bearer credential for the domain: anyone holding it can
move the name, and a chat transcript is not a place to put one.

Just Domain does let an owner switch a domain's transfer lock off and issue its
authorization code without contacting support. That means one thing: a human owner,
signed in on justdomain.ai, in a browser. It does not mean an API you can reach, and it
does not mean you can do it on their behalf.

So: never ask the user for an authorization code, never offer to hold, store or relay
one, never claim you can unlock a domain or move it yourself. For a domain held
elsewhere the owner gets the code from that registrar; for a domain held at Just Domain,
from their own account. Point them at the browser and stop. Every
`check_domain_transfer` response also carries this rule in `auth_code_policy`; it says
the same thing as this section, and you may quote it to the user.

## Renewals

Auto-renew is a per-domain setting in the owner's dashboard on justdomain.ai. Whether a
charge is scheduled for a domain, and on what date, is stated on that domain's page.
This skill cannot know it: send the user to https://justdomain.ai/dashboard and do not
state a renewal date, a charge or a reminder schedule on your own.

## What never happens in the chat

- No order, payment or reservation. There is no purchase tool and the skill never
  implies one.
- No "registered" or "reserved" unless the user reports finishing checkout.
- No renewal, auto-renew change, DNS or nameserver edit: owner actions in the dashboard.
- No transfer is started, no lock is changed, no authorization code is requested,
  accepted or relayed.
- No "ready" without an empty `blockers` list, a supported ending and a registry answer.
- No price other than the returned total; never per year on a multi-year term.
- No confirmation, receipt or success message the tool did not return.

## Not this skill's job

- Trademark, legal or brand-conflict advice. Availability is not a trademark clearance.
- Company or business registration.
- Registrant or WHOIS research; naming the owner of a taken domain.
- Aftermarket brokering or domain valuation.
- Hand-written lists of endings presented as available.

## If a tool is missing or fails

- Tool not available: say the Just Domain connector is not connected in this session,
  that the plugin needs to be enabled in the client's plugin settings, and that the
  session then needs a restart. Do not guess.
- Error returned: show the error text in one sentence and offer to retry or narrow the
  list. `[invalid_query] Could not parse any valid domains from the request.` means no
  name in the request had a usable ending. A timeout is not a "ready" and not an
  "available".

## Reference

- `references/mcp-api.md`: every field of both tools and the blocker codes.
- Resource `domain://faq` on the server holds current factual answers on pricing terms,
  WHOIS privacy, DNS, refunds, renewals, transfers and what is not supported yet.
- Prompts `jd-check` and `jd-transfer-check` on the server bootstrap a check.
- https://justdomain.ai/docs/mcp and https://justdomain.ai/docs/agent-transfer-check
  for humans.
