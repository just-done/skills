## Summary

<!-- What does this change do, and why is it needed? Link the related issue if there is one. -->

## Type of change

- [ ] Bug fix
- [ ] New or changed skill behavior
- [ ] Documentation
- [ ] Repository or CI maintenance

## Testing

<!-- The commands you ran and what you observed, for example `claude --plugin-dir .` and the prompts you tried. -->

## Checklist

- [ ] `claude plugin validate .claude-plugin/plugin.json --strict` and `claude plugin validate . --strict` pass
- [ ] `agentskills validate` passes for every skill directory
- [ ] `python3 .github/scripts/check_metadata.py` passes
- [ ] If `skills/` or `.mcp.json` changed, the version in `.claude-plugin/plugin.json` is bumped and `CHANGELOG.md` is updated
- [ ] User-facing text describes only what the MCP server returns
