#!/usr/bin/env python3
"""Consistency checks for the plugin manifests, the MCP configuration and the skills.

These checks complement `claude plugin validate`, which does not inspect skill
frontmatter limits, the MCP server entry or consistency between manifests.
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
MCP_SERVER_KEY = "just-domain"
MCP_SERVER_URL = "https://mcp.justdomain.ai/"

ALLOWED_SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
MAX_SKILL_DESCRIPTION = 1024
MAX_SKILL_BODY_LINES = 500
PLUGIN_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]{1,63}")

# Zero-width, byte-order-mark and bidirectional control characters (CVE-2021-42574).
HIDDEN_UNICODE = re.compile("[\u200b-\u200f\ufeff\u202a-\u202e\u2066-\u2069]")

HANDOFF_SENTENCE = (
    "Nothing is ordered or charged here, and the name is not reserved for you "
    "until you finish checkout."
)

# Keep the plugin payload limited to manifests, skills and documentation.
DISALLOWED_ROOT_ENTRIES = ("CLAUDE.md", "bin", "hooks", "commands", "agents", "scripts")

# Other client manifests that must stay in step with the Claude Code manifest when present.
PARITY_MANIFESTS = (".codex-plugin/plugin.json", ".cursor-plugin/plugin.json", "plugin.json")

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
        if meta.get("name") != path.parent.name:
            error(path, "name must match the skill directory name")
        description = str(meta.get("description", ""))
        if not 1 <= len(description) <= MAX_SKILL_DESCRIPTION:
            error(path, f"description is {len(description)} characters; the limit is {MAX_SKILL_DESCRIPTION}")
        if any(ch in description for ch in "<>[]"):
            error(path, "description must not contain <, >, [ or ]")
        if len(body.splitlines()) > MAX_SKILL_BODY_LINES:
            error(path, f"body exceeds {MAX_SKILL_BODY_LINES} lines")
        if HANDOFF_SENTENCE not in text:
            error(path, "registration hand-off sentence is missing or differs from the other skills")


def check_manifests() -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    plugin = load_json(plugin_path)
    marketplace = load_json(marketplace_path)

    name = plugin.get("name", "")
    description = plugin.get("description", "")
    version = plugin.get("version", "")

    if name != PLUGIN_NAME:
        error(plugin_path, f"plugin name must remain '{PLUGIN_NAME}'")
    if not PLUGIN_NAME_PATTERN.fullmatch(name):
        error(plugin_path, "plugin name must be lowercase letters, digits and hyphens")
    if description != description.strip() or not 10 <= len(description) <= 2000:
        error(plugin_path, "description must be 10 to 2000 characters without surrounding whitespace")

    if marketplace.get("name") != MARKETPLACE_NAME:
        error(marketplace_path, f"marketplace name must remain '{MARKETPLACE_NAME}'")
    entries = marketplace.get("plugins", [])
    if len(entries) != 1:
        error(marketplace_path, "marketplace must list exactly one plugin")
    else:
        entry = entries[0]
        if entry.get("name") != name:
            error(marketplace_path, "plugin entry name must match plugin.json")
        if entry.get("description") != description:
            error(marketplace_path, "plugin entry description must match plugin.json")
        if "version" in entry:
            error(marketplace_path, "set the version in plugin.json only")

    for relative in PARITY_MANIFESTS:
        path = ROOT / relative
        if not path.exists():
            continue
        other = load_json(path)
        for field, expected in (("name", name), ("version", version), ("description", description)):
            if other.get(field) != expected:
                error(path, f"{field} must match .claude-plugin/plugin.json")

    changelog = ROOT / "CHANGELOG.md"
    if not re.search(rf"^## \[{re.escape(version)}\]", changelog.read_text(encoding="utf-8"), re.MULTILINE):
        error(changelog, f"no entry for version {version}")


def check_mcp() -> None:
    path = ROOT / ".mcp.json"
    servers = load_json(path).get("mcpServers", {})
    server = servers.get(MCP_SERVER_KEY)
    if server is None:
        error(path, f"server key '{MCP_SERVER_KEY}' is missing")
        return
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
