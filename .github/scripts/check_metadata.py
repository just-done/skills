#!/usr/bin/env python3
"""Consistency checks for the plugin manifests, the MCP configuration and the skills.

These checks complement `claude plugin validate` and the Agent Skills reference
validator. They keep the plugin limited to its manifests, one hosted MCP server and
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
MCP_SERVER_KEY = "just-domain"
MCP_SERVER_URL = "https://mcp.justdomain.ai/"

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

# The registration hand-off that both skills send, line for line.
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
        if HANDOFF_BLOCK not in text:
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
    if description != description.strip() or not 10 <= len(description) <= 2000:
        error(plugin_path, "description must be 10 to 2000 characters without surrounding whitespace")
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
    if set(servers) != {MCP_SERVER_KEY}:
        error(path, f"only the '{MCP_SERVER_KEY}' server may be configured")
    server = servers.get(MCP_SERVER_KEY)
    if server is None:
        error(path, f"server key '{MCP_SERVER_KEY}' is missing")
        return
    if set(server) != {"type", "url"}:
        error(path, "the server entry may only set type and url")
    if server.get("type") != "http":
        error(path, "server type must be 'http'")
    if server.get("url") != MCP_SERVER_URL:
        error(path, f"server URL must be {MCP_SERVER_URL}")


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
    check_repository()
    if errors:
        print("\n".join(errors))
        return 1
    print("Metadata checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
