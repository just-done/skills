# Just Publish MCP server: tool reference

The plugin connects to the Just Publish MCP server at `https://mcp.justpublish.ai/claude`
over Streamable HTTP, under the server key `just-publish`. It serves four tools:
`deploy`, `list_sites`, `get_site_files` and `update_site_file`.

## Sign-in

Every call needs a signed-in user. Authorization is OAuth 2.1 with dynamic client
registration and PKCE, discovered from
`https://mcp.justpublish.ai/.well-known/oauth-protected-resource/claude`. A call without
a token is refused with `401` and that address in the `WWW-Authenticate` header, and the
client starts the sign-in. The user signs in with Google or a code sent to their email
address.

Every site is filed under the signed-in account. `deploy` therefore takes no email
address, and `get_site_files` and `update_site_file` accept `site_id` alone for that
account's own sites, including sites published from another client under the same
verified email address.

## `list_sites`

No parameters.

| Field | Notes |
| --- | --- |
| `sites` | Most recently updated first. Each has `site_id`, `url`, `status` (`live` or `archived`), `created_at`, `last_deploy_at`, `hits_48h` (views in the last 48 hours) and, when one is fully connected, `custom_domain`. |
| `total` | How many sites the user has in total. |
| `returned` | How many are in `sites`. |
| `truncated` | True when the user has more sites than were returned; the rest are on the dashboard. |
| `dashboard_url` | Where the user sees and manages every site in a browser. |

`custom_domain` is absent while a domain is still being set up.

## `deploy`

Publishes a new site, or replaces every file of an existing one.

| Argument | Required | Notes |
| --- | --- | --- |
| `files` | yes | Array of `{ path, content, encoding }`. Must include `index.html` at the root. `encoding` is `utf-8` (the default for text) or `base64` (binary). |
| `site_id` | no | Omit to create a new site. To publish over an existing site, pass it with `edit_token`; `site_id` on its own is rejected. |
| `edit_token` | no | Returned when the site was first published. Needed only to publish over that site. |

Returns `url`, `site_id`, `created`, `files_uploaded`, `total_bytes` and `dashboard_url`,
and `edit_token` on first create. Do not show the token to the user or ask them to save
it.

Publishing over an existing site replaces it: every file left out is deleted.

## `get_site_files`

| Argument | Required | Notes |
| --- | --- | --- |
| `site_id` | yes | From `deploy` or `list_sites`. |
| `edit_token` | no | Only for a site that is not the signed-in user's own. |
| `paths` | no | Read only these files. Omit to read every text file. |

Returns `site_id`, `url`, `version`, `manifest` (every file's `path`, `size_bytes`,
`content_type`, `sha256` and `is_text`), `files` (the text contents) and `truncated`,
which is true when some contents were left out for size; request those by path.

## `update_site_file`

| Argument | Required | Notes |
| --- | --- | --- |
| `site_id` | yes | From `deploy` or `list_sites`. |
| `edit_token` | no | Only for a site that is not the signed-in user's own. |
| `files` | yes | Array of `{ path, content, encoding }`. Only these files are written; every other file stays. |
| `expected_version` | no | The `version` from `get_site_files`. If the site changed since, the update is rejected with a conflict; read again and reapply. |

Returns `site_id`, `url`, `version`, `files_written` and `files_total`. It cannot delete
a file or remove `index.html`.

## Limits

- Free sites: 50 MB per site, 5 MB per file, 500 files.
- `index.html` at the root is required on every `deploy`.
- Paths are relative to the site root: no `..` and no backslashes.

## Errors

A rejected call returns a tool error whose message states the reason and the fix. The
full catalog, with each error and its recovery step, is at
https://justpublish.ai/docs/errors.

## Documentation

- https://justpublish.ai/docs/mcp
- https://justpublish.ai/docs/mcp/claude
