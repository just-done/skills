---
name: just-publish
description: >-
  Publishes a static website (HTML, CSS, JavaScript, images) to a live public link with
  Just Publish (justpublish.ai), and changes a site published there before. Lists the
  user's sites, reads a site's files and edits only the files that change. Explains how
  to put a site on the user's own domain, and finds that domain with the just-domain
  skill when they do not have one yet. Use when the user says "publish this site", "put
  this online", "give me a link I can share", "host what we just built", "update my
  site", "change the headline on my website", "what sites do I have" or "put my site on
  my own domain". Publishing is free; the user signs in once. Not for server code,
  databases or frameworks that need a server, such as Next.js with server rendering.
license: MIT
---

# Just Publish

Just Publish (https://justpublish.ai) puts static files online at
`https://{slug}.justpublish.site/`. Publishing is free and there is no build step: files
in, live link out. This skill uses four tools on the `just-publish` MCP server:

- `deploy`: publishes a new site, or replaces every file of an existing one.
- `list_sites`: the sites the signed-in user has published.
- `get_site_files`: the files currently live on one of their sites, and its version.
- `update_site_file`: writes one or a few files and leaves every other file in place.

Every site is filed under the user's Just Publish account. That account is what lets
them find, change and take down the site later, so there is no code or token for them to
keep. For domain names, use the just-domain skill in this plugin; it uses the
`just-domain` server.

## When this skill applies

The user says things like:

- "publish this site" / "put this online" / "make this a website"
- "give me a link for this" / "I want a URL I can share"
- "host what we just built"
- "update my site" / "change the price on my landing page" / "add an about page"
- "what sites do I have?" / "find my portfolio site"
- "put my site on my own domain" / "I want acme.com for my site"

The site must be static: HTML, CSS, JavaScript, images and fonts. Do not use this skill
for a backend (APIs, databases, server-rendered Next.js or Nuxt), or to change a site
that was not published with Just Publish.

## Signing in

The first time a tool is used, the user signs in to Just Publish in the browser, with
Google or a code sent to their email address. In Claude Code, `/mcp` shows
`plugin:just:just-publish`; if it asks for authentication, the user selects it and signs
in. A free account is created on first sign-in.

Never ask the user for an email address, a password, an edit token or any other
credential in the chat. `deploy` takes no email: the site goes under the signed-in
account.

## Publish a new site

1. Collect the site's files. `index.html` at the root is required.
2. If the user did not already ask to publish these files, confirm before the first
   publish. Publishing puts the files on the public internet, where anyone with the link
   can open them.
3. Call `deploy` with `files`, an array of `{ path, content, encoding }`. Paths are
   relative to the site root, such as `index.html` or `assets/logo.png`. Send text files
   as plain strings; send binary files base64-encoded with `"encoding": "base64"`.
4. The result has the live `url` and the `site_id`. Give the user the link in plain
   words. That is what they asked for.

The result also carries an `edit_token`. Do not show it and do not ask the user to save
it: the site belongs to their account, and `update_site_file` and `get_site_files` need
only the `site_id`.

## Change a site that is already live

1. Find the site. If you do not have its `site_id` from earlier in the conversation, call
   `list_sites` and match by link, custom domain or date. If more than one site could be
   the one, ask which, showing each site's link. If `truncated` is true, the user has
   more sites than were returned; the rest are on the dashboard.
2. Read before you write. Call `get_site_files` with the `site_id`. It returns every file
   on the site, the contents of the text files and the site's `version`. To read only
   some files, pass their paths in `paths`; if `truncated` is true, request the missing
   files by path.
3. Edit the files you read. Do not rebuild a page from memory.
4. Call `update_site_file` with the `site_id`, only the files you changed, and
   `expected_version` set to the `version` you just read. Every file you leave out stays
   as it is.
5. Give the user the link and a one-line summary of what changed.

If `update_site_file` reports a conflict, the site changed after you read it. Read it
again with `get_site_files`, apply the change to the new content and try once more.

`update_site_file` cannot delete a file or remove `index.html`. To remove files, the
whole site has to be published again with `deploy`, which needs the `edit_token` that
`deploy` returned when the site was first published. `deploy` replaces the whole site:
every file you leave out is deleted. Before a replacing deploy, read the site with
`get_site_files`, name the files that will be removed and get the user's yes. If you do
not have the `edit_token`, say that you can't remove files from this site here.

## Put a site on the user's own domain

A custom domain, such as acme.com, is connected to a published site from the dashboard,
not from the chat. There is no tool for it.

1. The site must be published first. Publish it if it is not.
2. If the user already owns a domain: send them to the site in the dashboard (the
   `dashboard_url` from `deploy`, or https://justpublish.ai/dashboard), where they choose
   to connect a custom domain. The dashboard shows the DNS records to add where the
   domain is registered. Do not write DNS records from memory.
3. If the user does not have a domain yet: use the just-domain skill. Check the names
   they want with `search_domains`, present the results as that skill says, and for the
   name they choose send its registration block, link last. The user registers and pays
   on justdomain.ai, in their browser. Then they come back to the dashboard and connect
   it.

A custom domain comes with Builder, the $9 a month plan for that site. The free link
keeps working next to it. The domain name itself is bought separately. For anything
else about plans and prices, send the user to https://justpublish.ai/pricing.

Do not say a domain is connected until `list_sites` shows it as the site's
`custom_domain`. A domain that is still being set up is not listed there.

## Limits

- `index.html` at the root of the files is required on every `deploy`.
- Free sites: 50 MB per site, 5 MB per file, 500 files.
- Paths are relative to the site root: no `..`, no backslashes.
- Static only: no build step and no server code. If the project needs a build, build it
  first and publish the output folder.
- A free site with no visitors for 30 days is archived. `list_sites` shows it with the
  status `archived`, and the user can restore it from the dashboard.

## Results and errors

- After a publish or a change, the link is the answer. Keep the rest to a sentence or
  two.
- When a call is rejected, the error states the reason and the fix, such as a missing
  `index.html`, a file that is too large or a path that is not allowed. Say the reason in
  plain words, fix what you can and try again. The full list is at
  https://justpublish.ai/docs/errors.
- Never show the user an `edit_token`, a raw error or a field name.
- Never say a site is live, changed or connected unless a tool result says so.

## If a tool is missing or fails

- Tools not available: say "Just Publish isn't connected in this conversation, so I
  can't publish right now." In Claude Code, add "Run /mcp, select
  plugin:just:just-publish and sign in, then ask again."; anywhere else, "Turn on the
  Just plugin in your settings, then start a new conversation."
- Sign-in required or expired: ask the user to sign in again from `/mcp` in Claude Code,
  or from the plugin's connector settings elsewhere.
- A timeout: try once more without mentioning it. If it fails again, say "I couldn't
  reach Just Publish just now." and offer to try again.

## Not this skill's job

- Buying, renewing or transferring a domain; use the just-domain skill.
- Changing DNS records at a registrar.
- Payment or plan changes; those happen on justpublish.ai, in the browser.
- Hosting server code, databases, forms that need a backend, or user accounts.

## Reference

- `references/mcp-api.md`: the parameters and results of the four tools.
- Documentation: https://justpublish.ai/docs/mcp and
  https://justpublish.ai/docs/mcp/claude
