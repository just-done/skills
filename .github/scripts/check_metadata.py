#!/usr/bin/env python3
"""Consistency checks for the plugin manifests, the MCP configurations and the skills.

These checks complement `claude plugin validate` and the Agent Skills reference
validator. They keep the plugin limited to its manifests, the hosted MCP servers and
skill instructions, and keep the manifests and the skills consistent with each other.
Run from the repository root:

    python3 .github/scripts/check_metadata.py

Exits with status 1 and prints GitHub Actions error annotations on failure.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

PLUGIN_NAME = "just"
MARKETPLACE_NAME = "just-skills"
MCP_CONFIG = "./.mcp.json"
MCP_SERVERS = {
    "just-domain": "https://mcp.justdomain.ai/",
    "just-publish": "https://mcp.justpublish.ai/claude",
}

ALLOWED_PLUGIN_KEYS = {
    "$schema",
    "name",
    "displayName",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "mcpServers",
}
ALLOWED_SKILL_KEYS = {"name", "description", "license"}

# Cursor reads its own manifest and server list. The keys below are the subset of
# Cursor's plugin and marketplace schemas (github.com/cursor/plugins, schemas/) that this
# plugin uses; the schemas reject any key they do not define.
CURSOR_MCP_CONFIG = "./cursor/mcp.json"
CURSOR_SKILLS = "./skills/"
CURSOR_LOGO = "assets/logo.png"
CURSOR_MCP_SERVERS = {
    "just-domain": "https://mcp.justdomain.ai/",
    "just-publish": "https://mcp.justpublish.ai/",
}
CURSOR_PLUGIN_HEADER = {"X-Cursor-Plugin": PLUGIN_NAME}
ALLOWED_CURSOR_PLUGIN_KEYS = {
    "name",
    "displayName",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "logo",
    "category",
    "skills",
    "mcpServers",
}
ALLOWED_CURSOR_AUTHOR_KEYS = {"name", "email"}
ALLOWED_CURSOR_ENTRY_KEYS = {"name", "source", "description"}
# claude.ai and Cowork reject a plugin whose description is longer than this on upload.
MAX_PLUGIN_DESCRIPTION = 500
MAX_SKILL_NAME = 64
MAX_SKILL_DESCRIPTION = 1024
MAX_SKILL_BODY_LINES = 500
SKILL_NAME_PATTERN = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
PLUGIN_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]{1,63}")

# Characters that are invisible or reorder text, so a reviewer cannot see what a model
# reads: the soft hyphen, the Arabic letter mark and Mongolian vowel separator,
# zero-width and directional marks, bidirectional embeddings, overrides and isolates
# (CVE-2021-42574), the word joiner and invisible operators, variation selectors, the
# byte-order mark and the Unicode tag block.
HIDDEN_UNICODE = re.compile(
    "["
    "\u00ad\u061c\u180e"
    "\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u206f"
    "\ufe00-\ufe0f\ufeff"
    "\U000e0000-\U000e007f"
    "]"
)

# Skills that hand off a domain registration, and the block they send, line for line.
HANDOFF_SKILLS = {"find-a-name", "just-domain"}
HANDOFF_BLOCK = (
    "{fqdn} is available: {price form}, renews at {renewal form}.\n"
    "You create an account or sign in, then pay on justdomain.ai, in your browser. "
    "Nothing is ordered, reserved or charged here. The price shown at checkout is the one "
    "that applies, and the name is registered to you only after checkout is complete and "
    "the registration is confirmed.\n"
    "Link to register {fqdn}: {checkout_url}\n"
)

# Keep the plugin payload to manifests, the MCP configuration, skills and documentation:
# no component that runs code or changes how the client behaves.
DISALLOWED_ROOT_ENTRIES = (
    ".lsp.json",
    "CLAUDE.md",
    "agents",
    "bin",
    "commands",
    "hooks",
    "monitors",
    "output-styles",
    "scripts",
    "settings.json",
    "themes",
    "workflows",
)

errors: list[str] = []


def error(path: Path | str, message: str) -> None:
    rel = path.relative_to(ROOT) if isinstance(path, Path) else path
    errors.append(f"::error file={rel}::{message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(path, f"cannot read JSON: {exc}")
        return {}


def check_skills() -> None:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skill_files:
        error("skills", "no skills found")
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            error(path, "frontmatter must start on the first line")
            continue
        frontmatter, _, body = text[4:].partition("\n---\n")
        try:
            meta = yaml.safe_load(frontmatter)
        except yaml.YAMLError as exc:
            error(path, f"frontmatter is not valid YAML: {exc}")
            continue
        if not isinstance(meta, dict):
            error(path, "frontmatter must be a mapping")
            continue
        extra = sorted(set(meta) - ALLOWED_SKILL_KEYS)
        if extra:
            error(path, f"unsupported frontmatter keys: {', '.join(extra)}")
        name = str(meta.get("name", ""))
        if len(name) > MAX_SKILL_NAME or not SKILL_NAME_PATTERN.fullmatch(name):
            error(path, f"name must be 1 to {MAX_SKILL_NAME} lowercase letters, digits and single hyphens")
        if name != path.parent.name:
            error(path, "name must match the skill directory name")
        description = str(meta.get("description", ""))
        if not 1 <= len(description) <= MAX_SKILL_DESCRIPTION:
            error(path, f"description is {len(description)} characters; the limit is {MAX_SKILL_DESCRIPTION}")
        if any(ch in description for ch in "<>[]"):
            error(path, "description must not contain <, >, [ or ]")
        if len(body.splitlines()) > MAX_SKILL_BODY_LINES:
            error(path, f"body exceeds {MAX_SKILL_BODY_LINES} lines")
        if path.parent.name in HANDOFF_SKILLS and HANDOFF_BLOCK not in text:
            error(path, "registration hand-off block is missing or differs from the other skills")


def check_manifests() -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    plugin = load_json(plugin_path)
    marketplace = load_json(marketplace_path)

    extra = sorted(set(plugin) - ALLOWED_PLUGIN_KEYS)
    if extra:
        error(plugin_path, f"unsupported manifest keys: {', '.join(extra)}")

    name = plugin.get("name", "")
    description = plugin.get("description", "")
    version = plugin.get("version", "")

    if name != PLUGIN_NAME:
        error(plugin_path, f"plugin name must remain '{PLUGIN_NAME}'")
    if not PLUGIN_NAME_PATTERN.fullmatch(name):
        error(plugin_path, "plugin name must be lowercase letters, digits and hyphens")
    if description != description.strip() or not 10 <= len(description) <= MAX_PLUGIN_DESCRIPTION:
        error(plugin_path, f"description must be 10 to {MAX_PLUGIN_DESCRIPTION} characters without surrounding whitespace")
    if plugin.get("mcpServers") != MCP_CONFIG:
        error(plugin_path, f"mcpServers must be {MCP_CONFIG}")

    if marketplace.get("name") != MARKETPLACE_NAME:
        error(marketplace_path, f"marketplace name must remain '{MARKETPLACE_NAME}'")
    entries = marketplace.get("plugins", [])
    if len(entries) != 1:
        error(marketplace_path, "marketplace must list exactly one plugin")
    else:
        entry = entries[0]
        if entry.get("name") != name:
            error(marketplace_path, "plugin entry name must match plugin.json")
        if entry.get("source") != "./":
            error(marketplace_path, "plugin entry source must be ./")
        if entry.get("description") != description:
            error(marketplace_path, "plugin entry description must match plugin.json")
        if "version" in entry:
            error(marketplace_path, "set the version in plugin.json only")

    changelog = ROOT / "CHANGELOG.md"
    if not re.search(rf"^## \[{re.escape(version)}\]", changelog.read_text(encoding="utf-8"), re.MULTILINE):
        error(changelog, f"no entry for version {version}")


def check_mcp() -> None:
    path = ROOT / ".mcp.json"
    servers = load_json(path).get("mcpServers", {})
    extra = sorted(set(servers) - set(MCP_SERVERS))
    if extra:
        error(path, f"unexpected servers: {', '.join(extra)}")
    for key, url in MCP_SERVERS.items():
        server = servers.get(key)
        if server is None:
            error(path, f"server key '{key}' is missing")
            continue
        if set(server) != {"type", "url"}:
            error(path, f"the '{key}' entry may only set type and url")
        if server.get("type") != "http":
            error(path, f"the '{key}' server type must be 'http'")
        if server.get("url") != url:
            error(path, f"the '{key}' server URL must be {url}")


def check_cursor() -> None:
    claude = load_json(ROOT / ".claude-plugin" / "plugin.json")
    plugin_path = ROOT / ".cursor-plugin" / "plugin.json"
    marketplace_path = ROOT / ".cursor-plugin" / "marketplace.json"
    mcp_path = ROOT / "cursor" / "mcp.json"
    plugin = load_json(plugin_path)
    marketplace = load_json(marketplace_path)

    extra = sorted(set(plugin) - ALLOWED_CURSOR_PLUGIN_KEYS)
    if extra:
        error(plugin_path, f"unsupported manifest keys: {', '.join(extra)}")
    for key in ("name", "displayName", "version", "repository", "license", "keywords"):
        if plugin.get(key) != claude.get(key):
            error(plugin_path, f"{key} must match .claude-plugin/plugin.json")
    author = plugin.get("author", {})
    if not isinstance(author, dict) or set(author) - ALLOWED_CURSOR_AUTHOR_KEYS:
        error(plugin_path, "author may only set name and email")
    elif any(author.get(key) != claude.get("author", {}).get(key) for key in ALLOWED_CURSOR_AUTHOR_KEYS):
        error(plugin_path, "author name and email must match .claude-plugin/plugin.json")
    description = plugin.get("description", "")
    if description != description.strip() or not 10 <= len(description) <= MAX_PLUGIN_DESCRIPTION:
        error(plugin_path, f"description must be 10 to {MAX_PLUGIN_DESCRIPTION} characters without surrounding whitespace")
    if plugin.get("skills") != CURSOR_SKILLS:
        error(plugin_path, f"skills must be {CURSOR_SKILLS}")
    if plugin.get("mcpServers") != CURSOR_MCP_CONFIG:
        error(plugin_path, f"mcpServers must be {CURSOR_MCP_CONFIG}")
    if plugin.get("logo") != CURSOR_LOGO or not (ROOT / CURSOR_LOGO).is_file():
        error(plugin_path, f"logo must be {CURSOR_LOGO} and the file must exist")

    if marketplace.get("name") != MARKETPLACE_NAME:
        error(marketplace_path, f"marketplace name must remain '{MARKETPLACE_NAME}'")
    if set(marketplace.get("owner", {})) - ALLOWED_CURSOR_AUTHOR_KEYS:
        error(marketplace_path, "owner may only set name and email")
    entries = marketplace.get("plugins", [])
    if len(entries) != 1:
        error(marketplace_path, "marketplace must list exactly one plugin")
    else:
        entry = entries[0]
        if set(entry) - ALLOWED_CURSOR_ENTRY_KEYS:
            error(marketplace_path, "a plugin entry may only set name, source and description")
        if entry.get("name") != PLUGIN_NAME or entry.get("source") != "./":
            error(marketplace_path, f"the plugin entry must be '{PLUGIN_NAME}' at ./")
        if entry.get("description") != description:
            error(marketplace_path, "plugin entry description must match .cursor-plugin/plugin.json")

    servers = load_json(mcp_path).get("mcpServers", {})
    if set(servers) != set(CURSOR_MCP_SERVERS):
        error(mcp_path, f"servers must be exactly: {', '.join(CURSOR_MCP_SERVERS)}")
    for key, url in CURSOR_MCP_SERVERS.items():
        server = servers.get(key)
        if server is None:
            continue
        if set(server) != {"type", "url", "headers"}:
            error(mcp_path, f"the '{key}' entry may only set type, url and headers")
        if server.get("type") != "http":
            error(mcp_path, f"the '{key}' server type must be 'http'")
        if server.get("url") != url:
            error(mcp_path, f"the '{key}' server URL must be {url}")
        if server.get("headers") != CURSOR_PLUGIN_HEADER:
            error(mcp_path, f"the '{key}' entry must send only the header X-Cursor-Plugin: {PLUGIN_NAME}")


def check_repository() -> None:
    for entry in DISALLOWED_ROOT_ENTRIES:
        if (ROOT / entry).exists():
            error(entry, "not allowed at the plugin root")
    tracked = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True
    ).stdout.decode().split("\0")
    for relative in filter(None, tracked):
        path = ROOT / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if HIDDEN_UNICODE.search(text):
            error(path, "contains hidden or bidirectional Unicode characters")


def main() -> int:
    check_skills()
    check_manifests()
    check_mcp()
    check_cursor()
    check_repository()
    if errors:
        print("\n".join(errors))
        return 1
    print("Metadata checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
