# Just Domain - tool field reference

Endpoint `https://mcp.justdomain.ai/`, MCP over Streamable HTTP, no sign-in. Both
tools are read-only: no order is created and no payment is taken through them.

## `search_domains`

| Argument | Type | Required | Notes |
|---|---|---|---|
| `domains` | array of strings | preferred | 1-200 fully-qualified names, each with its ending, e.g. `["acme.com", "acme.io"]`. Exactly these names are checked. |
| `query` | string | fallback | Free text: one or more names, comma- or space-separated. A name given without an ending is expanded to com, io, ai, co and net. Ignored when `domains` is supplied. |

Top-level fields on every response: `domains` (the list as parsed), `results`,
`alternatives`, `warnings`, `error`, `error_message`, `component_hint` (always
`domain_search_results`) and `next_action` (always `none`).

`results`, one entry per parsed domain:

| Field | Type | Notes |
|---|---|---|
| `fqdn` | string | The fully-qualified name as checked. |
| `name` | string | The label before the ending. |
| `tld` | string | The ending, without a leading dot. |
| `available` | boolean | Whether the domain can be registered right now. |
| `status` | string | Provider status, e.g. `free`, `active`, `premium`. |
| `premium` | boolean | Registry-priced name. Just Domain does not register these yet. |
| `term_years` | integer | Length of ONE registration term for this ending, and the period `price` and `renewal_price` each cover. `1` on almost every ending; `2` on `.ai`. |
| `price` | object or null | Registration price for one full term: `{ amount_minor, currency, formatted }`. |
| `renewal_price` | object or null | Price of one further term, same basis as `price`. |
| `requires_additional_data` | boolean or null | Null in practice; the row's `warnings` carry the signal. |
| `checkout_url` | string or null | Present only on available, non-premium names Just Domain can register today: the URL the user opens in a browser to register on justdomain.ai. |
| `warnings` | array of strings | Row codes: `requires_additional_data` (the registry needs registrant details Just Domain cannot collect yet; available, no link), `not_offered` (Just Domain does not offer this ending; never "taken"), `premium_not_supported`, `renewal_price_unavailable`. Show unknown codes as notes. |

`alternatives` is an always-present list, normally empty; it can be non-empty only when
every requested name is taken and the server looked at other endings for the same
label. Each entry has the same shape as a result row and carries a `checkout_url`.

Top-level `warnings` report names dropped from the request, for example a bare label
in a mixed batch (`invalid_entry:missing_tld:<label>` or similar); compare the names
sent with the `fqdn` values returned. When no name at all can be parsed the tool returns
an error: `[invalid_query] Could not parse any valid domains from the request.`

Prices are term totals, not annual rates. On `.ai` the registry mandates a two-year
minimum term, so a quoted `.ai` figure is a two-year total. Never divide or multiply a
returned price.

## `check_domain_transfer`

| Argument | Type | Required | Notes |
|---|---|---|---|
| `domain` | string | yes | ONE fully-qualified domain the user already owns at another registrar. One per call. |

Answered from two public sources only: the registry's RDAP record and Just Domain's
price list. It reads no account.

| Field | Type | Notes |
|---|---|---|
| `domain` / `tld` | string | The name as checked. |
| `supported` | boolean | Whether Just Domain can accept this ENDING at all. When false, do not quote `price` even if an amount is returned. |
| `ready` | boolean | True only when `blockers` is empty; derived from that list. |
| `checked_at` | string | ISO-8601 instant the facts were read. |
| `blockers` | array | `{ code, detail, eligible_at }`. An empty array is the only thing that means ready. |
| `registrar` | object | `{ name, iana_id }`: who sponsors the domain today. |
| `nameservers` | array of strings | The current delegation. |
| `dns_continuity` | object | `{ case, provider, detail }`, case = `independent`, `losing_registrar` or `unknown`. |
| `price` | object or null | `{ amount, currency, term_years, term_note, expected_new_expiry, is_premium }`. Null when the price could not be read, which is not the same as free. For an unsupported ending the amount may read 0.00: do not quote it. |
| `source` | object | `{ rdap, registrar_pricing }`: which sources answered. |
| `transfer_url` | string | The page a person opens to take this further. |
| `next_step` | string | One sentence matched to this domain's state. |
| `auth_code_policy` | string | The authorization-code rule, restated in every payload; it says what the skill says. |

Blocker codes: `locked`, `within_60_days`, `redemption`, `expired`, `tld_unsupported`,
`premium`, `not_registered`, `pending_transfer`, `pending_delete`, `unknown`. Render
`detail` for any code you do not recognise. `source.rdap: false` means the registry did
not answer, so nothing was established.

The transfer price is a term total. A `.ai` transfer adds and charges two years.
`expected_new_expiry` is a projection, not a confirmed date. Moving a domain in is not
self-service yet; the route is support@just-done.ai. No authorization (EPP) code is
ever returned, accepted or requested through this server.

## Limits

- At most 200 domains per `search_domains` call; exactly one domain per
  `check_domain_transfer` call.
- Every price is a total for one full term, never a per-year rate.
- Both tools are read-only. There is no registration, renewal, transfer, unlock, DNS or
  account tool on this server, and none is reachable by any other method here.

Product documentation for humans: https://justdomain.ai/docs/mcp
