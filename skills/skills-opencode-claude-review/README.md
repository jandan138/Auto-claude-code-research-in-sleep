# skills-opencode-claude-review

This package is a **thin override layer** for users who want:

- **OpenCode** as the main executor
- **Claude Code CLI** as the external reviewer
- the local `claude-review` MCP bridge instead of the base pack's neutral reviewer wording

It is designed to sit on top of the base OpenCode package at `skills/skills-opencode/`.

## What this package contains

- Only the review-heavy skill overrides that need a concrete reviewer backend
- No duplicate templates or shared resource directories
- No replacement for the base `skills/skills-opencode/` installation

Current overrides:

- `research-review`
- `novelty-check`
- `research-refine`
- `auto-review-loop`
- `paper-plan`
- `paper-figure`
- `paper-write`
- `auto-paper-improvement-loop`

## Install

1. Install the base OpenCode pack first:

```bash
python3 tools/generate_opencode_pack.py
cp -a skills/skills-opencode/* ~/.opencode/skills/
```

2. Install the Claude-review overlay second:

```bash
python3 tools/generate_opencode_claude_review_overrides.py
cp -a skills/skills-opencode-claude-review/* ~/.opencode/skills/
```

3. Register the Claude-review bridge with your OpenCode MCP configuration using `mcp-servers/claude-review/server.py`.

The bridge contract provides:

- `review_start`
- `review_reply_start`
- `review_status`

## Why this exists

The base `skills/skills-opencode/` pack intentionally stays reviewer-neutral.

This package adds a concrete split:

- executor: OpenCode
- reviewer: Claude Code CLI
- transport: `claude-review` MCP

For long paper and review prompts, this overlay assumes the async flow:

- `review_start`
- `review_reply_start`
- `review_status`
