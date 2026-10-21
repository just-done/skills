---
name: trademark-check
description: >-
  Checks whether a name is already taken as a trademark, with Open Trademarks
  (opentrademarks.org) through the Just Domain connector: one verdict across the US, EU
  and Israeli trademark registers, the live marks that match or resemble the name, the
  classes they share with what the user will sell, and the date each register was last
  read. Use when the user asks "is this name taken as a trademark", "is Brightcrumb
  trademarked", "does anyone own the trademark for Acme", "check these names against
  trademark registers" or "is there a trademark on my business name". A register search,
  not legal advice or a clearance. Read-only: nothing is filed, registered or watched in
  the chat.
license: MIT
---

# Trademark check

Answer one question: is this name already taken as a trademark? The `check_trademark`
tool on the Just Domain MCP server searches the trademark registers that Open Trademarks
(https://opentrademarks.org) reads and returns one verdict with its evidence. It is
read-only and needs no sign-in: nothing is filed, registered or watched. To name a
business from scratch, use the find-a-name skill in this plugin; it runs this check on
the shortlist before it checks domains.

## The rule

Without exception:

> do not tell the user a name is clear unless it was checked during this conversation and the registers were read today or yesterday; a register search is not legal advice.

- "The registers" means every register in the answer, each by the date part of its
  `loaded_at`, compared with today's date. A register with no `loaded_at` was not read.
- A verdict from memory, from earlier knowledge or from another site does not count.
  Check again.
- Even when the rule allows it, say what was searched and what was found ("No live match
  in the US, EU and Israeli registers, read 2026-10-02"), then the notice. Never "safe",
  "free to use" or "you can use it".

## Quick start

```
User: "Is Brightcrumb taken as a trademark? It's for a bakery."
-> check_trademark with the name and the goods "bakery"
-> One line: the verdict in plain words, then the registers read and their dates
-> The conflicting marks, if any
-> The answer's notice sentence, verbatim
-> Stop, or offer once to check the name's domains
```

## Inputs

- The name as the user wrote it. Several names: one call per name.
- What the business will sell, in a few plain words, as the goods ("sourdough bakery",
  "accounting software"). The check maps it to classes. If the user has not said, ask
  once; if they don't know, check without it and say that every class was searched.
- Classes: only when the user names Nice classes.
- Registers: leave the default, all of them.

## Call

`check_trademark` with the name and the goods. One call per name, no sign-in.

If `check_trademark` is not among your tools (an older server), make the same check with
your web tool: `GET https://api.opentrademarks.org/v1/check?name={name}&goods={goods}`,
both values URL-encoded, `goods` left out when there are none. The answer has the same
fields.

## Read the answer

`verdict` is one of four values. Say it in plain words, never as a code:

- `exact_live_mark`: "exact live mark". A live mark with the same name is registered in
  a class the business would use.
- `similar_live_marks`: "similar live marks". Live marks that look or sound close are
  registered in a class the business would use.
- `no_live_match`: "no live match found" in the registers that were read.
- `not_checked`: "not checked". No register in the check has been read yet; that is not
  a verdict. Say so in those words, and never present it as a match or as no match.

Other fields:

- `conflicts`: the marks behind the verdict. For each: `mark`, `register`, `number`,
  `signals` (how it matched) and `class_overlap` (the classes it shares with the goods),
  plus `office_url`, the office's own record, when present.
- `signals` in plain words: `exact` the same name, `variant` a variant of it, `spelling`
  spelled alike, `sound` sounds alike, `contains` contains the name, `pseudo` the name
  written another way, `hebrew` the name in Hebrew letters.
- `registers`: every register in the check, each with `loaded_at`, the time it was last
  read. Registers: `us` the United States, `eu` the European Union, `il` Israel. One with
  no `loaded_at` was not read, so the verdict says nothing about it.
- `query.classes`: the classes the goods were mapped to. Empty means every class.
- `other_classes`: live marks in classes the business would not use. Not conflicts. Give
  the count; list them only if asked.
- `dead`: marks that are no longer live. Not conflicts. Mention only if asked.
- `notice`: a fixed sentence on what the search covers. Show it verbatim with every
  answer.

## Present the answer

For one name:

```
{Name}: {verdict in plain words}. Registers read: {register} {YYYY-MM-DD}, ... {Registers not read} not read yet.
Classes searched: {classes} (from "{goods}"), or every class.
Marks found: {mark}, {register} no. {number}, {how it matched}, class {class_overlap}. Office record: {office_url}
{notice}
```

- Up to five marks, one line each; say how many more there are.
- No `conflicts`: leave out the "Marks found" line.
- For several names, one table: Name | Verdict | Marks found | Registers read, then the
  notice once.
- If the user asks whether they can use the name anyway, or whether a conflict would
  hold, say that a register search cannot answer that and a trademark attorney can. Do
  not guess.

## After the check: the domain

If the user is naming a business and the verdict is not an exact live mark, you may offer
once, in one line, to check the name's domains. After an exact live mark, offer nothing;
check its domains only if the user asks and says they hold the rights to that mark.

If they want the domains, call `search_domains` once with the name on `.com` and one or
two endings that fit, and give each row one status as the just-domain skill in this
plugin does. Quote a price only for a row with a `checkout_url`, from the response:

- Price form: "{price.formatted} for 1 year" when `term_years` is 1, otherwise
  "{price.formatted} for {term_years} years".
- Renewal form: "{renewal_price.formatted}/yr" when `term_years` is 1, otherwise
  "{renewal_price.formatted} every {term_years} years". Never divide a total.

When the user picks one, send exactly these three lines, link last:

```
{fqdn} is available: {price form}, renews at {renewal form}.
You create an account or sign in, then pay on justdomain.ai, in your browser. Nothing is ordered, reserved or charged here. The price shown at checkout is the one that applies, and the name is registered to you only after checkout is complete and the registration is confirmed.
Link to register {fqdn}: {checkout_url}
```

If `renewal_price` is null, the first line is "{fqdn} is available: {price form}. The
renewal price was not returned." Then stop.

## What never happens in the chat

- No name called clear outside the rule above, and no legal advice. The notice says what
  a register search does not see.
- No trademark is filed, watched, opposed or renewed. No tool here does that.
- No verdict, mark or read date from memory: only from an answer in this conversation.
- No research on a mark's owner beyond what the answer shows, and no view on whether a
  conflict would succeed.
- No error code or field name shown to the user.

## If the tool is missing or fails

- `check_trademark` not available: use the web check under "Call". If you cannot reach
  it either, say "I can't check trademark registers in this conversation." Then give one
  next step: in Claude Code, "Run /reload-plugins, then ask again."; anywhere else, "Turn
  on the Just plugin or the Just Domain connector in your settings, then start a new
  conversation." You can add that the same check is free at https://opentrademarks.org.
- A timeout or an unavailable service: retry once without mentioning it. If it fails
  again, say "I couldn't check that just now." and offer to try again.
- An answer with an `error` instead of a verdict, for example for an empty name: ask for
  the name again.
- Never show the raw error. After an error, never give a verdict.

## Reference

- API: https://api.opentrademarks.org/v1/check with `name`, `goods`, `classes` (Nice
  numbers, comma-separated) and `registers` (`us`, `eu`, `il`).
- Site: https://opentrademarks.org, where the registers page shows when each register
  was last read.
- The just-domain skill in this plugin covers domain checks and the full field
  reference for `search_domains`.
