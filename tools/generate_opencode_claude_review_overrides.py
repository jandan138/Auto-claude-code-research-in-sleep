#!/usr/bin/env python3
"""Generate Claude-review overlays for the OpenCode base pack."""

from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "skills" / "skills-opencode"
DEST_ROOT = REPO_ROOT / "skills" / "skills-opencode-claude-review"

TARGET_SKILLS = [
    "research-review",
    "novelty-check",
    "research-refine",
    "auto-review-loop",
    "paper-plan",
    "paper-figure",
    "paper-write",
    "auto-paper-improvement-loop",
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)

OVERRIDE_NOTE = (
    "> Override for OpenCode users who want **Claude Code CLI**, not a neutral "
    "review placeholder, to act as the reviewer. Install this package **after** "
    "`skills/skills-opencode/*`."
)

README_CONTENT = (
    """# skills-opencode-claude-review

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
""".strip()
    + "\n"
)

PREREQ_BLOCK = """## Prerequisites

- Install the base OpenCode pack first: generate `skills/skills-opencode/*` and place it where OpenCode can load the skills.
- Then install this overlay package second so it overwrites the same review-heavy skill names.
- Register the Claude-review bridge using `mcp-servers/claude-review/server.py` through your OpenCode MCP configuration.
- This gives OpenCode access to `mcp__claude-review__review_start`, `mcp__claude-review__review_reply_start`, and `mcp__claude-review__review_status`.
""".strip()

REVIEWER_LINE = (
    "- **REVIEWER_MODEL = `claude-review`** — Reviewer invoked through the local "
    "`claude-review` MCP bridge. Set `CLAUDE_REVIEW_MODEL` if you need a specific "
    "Claude model override."
)


def extract_field(frontmatter: str, field: str) -> str:
    pattern = re.compile(rf"^{re.escape(field)}:\s*(.+)$", re.MULTILINE)
    match = pattern.search(frontmatter)
    if not match:
        return ""
    value = match.group(1).strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        try:
            value = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            value = value[1:-1]
    return value


def build_frontmatter(name: str, description: str) -> str:
    safe_desc = description.replace('"', '\\"')
    return f'---\nname: "{name}"\ndescription: "{safe_desc}"\n---\n\n'


def normalize_description(text: str) -> str:
    if not text:
        return "Claude-review override for an OpenCode ARIS skill."
    replacements = [
        ("from GPT", "via Claude review"),
        ("GPT-5.4 xhigh review", "Claude-review MCP review"),
        ("iterative GPT-5.4 review", "iterative Claude-review MCP review"),
        ("OpenCode review transport", "Claude review via `claude-review` MCP"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = text.replace(
        "Claude review via Claude review via `claude-review` MCP",
        "Claude review via `claude-review` MCP",
    )
    text = text.replace(
        "Claude review via Claude review",
        "Claude review",
    )
    return text


def append_async_notes(text: str) -> str:
    note = (
        "After this start call, immediately save the returned `jobId` and poll "
        "`mcp__claude-review__review_status` with a bounded `waitSeconds` until "
        "`done=true`. Treat the completed status payload's `response` as the "
        "reviewer output, and save the completed `threadId` for any follow-up round."
    )

    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        if note in block:
            return block
        return f"{block}\n\n{note}"

    return re.sub(
        r"```(?:yaml|text)?\n(?:mcp__claude-review__review_start:|mcp__claude-review__review_reply_start:)[\s\S]*?```",
        repl,
        text,
    )


def transform_body(text: str) -> str:
    replacements = [
        (
            "Use the configured external reviewer transport to start a new review with xhigh reasoning:",
            "Use `mcp__claude-review__review_start` to start a new Claude review with xhigh reasoning:",
        ),
        (
            "Use the configured external reviewer transport to start a new review with comprehensive context:",
            "Use `mcp__claude-review__review_start` to start a new Claude review with comprehensive context:",
        ),
        (
            "Use the configured external reviewer continuation mechanism with the returned `threadId` to continue the conversation:",
            "Use `mcp__claude-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__claude-review__review_status` with the returned `jobId` to continue the conversation:",
        ),
        (
            "Use the configured external reviewer continuation mechanism with the saved threadId:",
            "Use `mcp__claude-review__review_reply_start` with the saved completed `threadId`:",
        ),
        (
            "If this is round 2+, use the configured external reviewer continuation mechanism with the saved threadId to maintain conversation context.",
            "If this is round 2+, use `mcp__claude-review__review_reply_start` with the saved completed `threadId`, then poll `mcp__claude-review__review_status` until `done=true` to maintain conversation context.",
        ),
        (
            "Call REVIEWER_MODEL via the configured external reviewer transport with xhigh reasoning:",
            "Call REVIEWER_MODEL via `mcp__claude-review__review_start` with xhigh reasoning:",
        ),
        (
            "Call REVIEWER_MODEL via `mcp__claude-review__review_start` with xhigh reasoning:",
            "Call REVIEWER_MODEL via `mcp__claude-review__review_start` with xhigh reasoning, then poll `mcp__claude-review__review_status` until `done=true` and use the completed `threadId` for any follow-up round:",
        ),
        (
            "Use REVIEWER_MODEL via the configured external reviewer continuation mechanism (same thread):",
            "Use REVIEWER_MODEL via `mcp__claude-review__review_reply_start` (same thread):",
        ),
        (
            "If no configured external reviewer transport is available,",
            "If `mcp__claude-review__review_start` is not available,",
        ),
        (
            "handles the external reviewer call internally",
            "handles the Claude review call internally",
        ),
        (
            "If using the configured external reviewer continuation mechanism directly",
            "If calling the Claude-review transport directly",
        ),
        (
            "and use the configured external reviewer continuation mechanism for later rounds.",
            "and use `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status` for later rounds.",
        ),
        (
            "re-submit for another round via the configured external reviewer continuation mechanism.",
            "re-submit for another round via `mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status`.",
        ),
        ("external reviewer transport (start):", "mcp__claude-review__review_start:"),
        (
            "external reviewer transport (reply):",
            "mcp__claude-review__review_reply_start:",
        ),
        (
            "configured external reviewer continuation mechanism",
            "`mcp__claude-review__review_reply_start` plus `mcp__claude-review__review_status`",
        ),
        ("configured external reviewer transport", "`claude-review` MCP bridge"),
        ("OpenCode review transport", "Claude review via `claude-review` MCP"),
        ("from GPT", "via Claude review"),
        ("from GPT-5.4", "via Claude-review MCP"),
        ("Claude review-5.4", "Claude-review MCP"),
        ("GPT-5.4 xhigh", "Claude-review MCP"),
        ("GPT-5.4", "Claude-review MCP"),
        ("GPT54_AUTO_REVIEW.md", "AUTO_REVIEW.md"),
        ("Codex/GPT-5.4", "Claude-review MCP"),
        ("codex-reply", "`mcp__claude-review__review_reply_start`"),
        ("Codex review calls", "Claude-review MCP calls"),
        ("Codex", "Claude-review MCP"),
        ("OpenAI model", "Claude-review backend"),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    text = text.replace(
        "Claude review via Claude review via `claude-review` MCP",
        "Claude review via `claude-review` MCP",
    )
    text = text.replace(
        "Claude review via Claude review",
        "Claude review",
    )
    text = text.replace(
        "Claude-review MCP/Claude-review MCP",
        "Claude-review MCP",
    )

    text = re.sub(
        r"^## Prerequisites\n\n(?:- .*\n)+",
        PREREQ_BLOCK + "\n\n",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^-\s*(?:\*\*)?REVIEWER_MODEL(?:\*\*)?.*$",
        REVIEWER_LINE,
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(r"(?m)^\s*model:\s*(?:gpt-5\.4|REVIEWER_MODEL)\s*\n", "", text)
    text = re.sub(
        r"(?m)^\s*```bash\n\s*See docs/OPENCODE_ADAPTATION\.md for reviewer transport setup\.\n\s*```\n",
        "",
        text,
    )
    return append_async_notes(text)


def generate_one(skill_name: str, dest_root: Path) -> None:
    skill_path = SRC_ROOT / skill_name / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError(f"Missing frontmatter: {skill_path}")

    frontmatter = match.group(1)
    body = content[match.end() :].lstrip("\n")
    name = extract_field(frontmatter, "name") or skill_name
    description = normalize_description(extract_field(frontmatter, "description"))

    output = build_frontmatter(name, description)
    output += OVERRIDE_NOTE + "\n\n"
    output += transform_body(body).rstrip() + "\n"

    target_dir = dest_root / skill_name
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "SKILL.md").write_text(output, encoding="utf-8")


def build_manifest() -> dict:
    return {
        "pack_type": "overlay",
        "source_pack": "skills/skills-opencode",
        "target_root": "skills/skills-opencode-claude-review",
        "overlay_depends_on": "skills/skills-opencode",
        "files": [
            {
                "canonical_path": f"skills/{skill}/SKILL.md",
                "base_generated_path": f"skills/skills-opencode/{skill}/SKILL.md",
                "override_path": f"skills/skills-opencode-claude-review/{skill}/SKILL.md",
                "kind": "skill",
                "classification": "direct_reviewer_consumer",
            }
            for skill in TARGET_SKILLS
        ],
        "support_assets": [],
        "runtime_assets_included": [],
    }


def generate_overlay(repo_root: Path, dest_root: Path) -> Path:
    del repo_root
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    for skill in TARGET_SKILLS:
        generate_one(skill, dest_root)

    (dest_root / "README.md").write_text(README_CONTENT, encoding="utf-8")
    manifest_path = dest_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest_path


def main() -> None:
    manifest_path = generate_overlay(REPO_ROOT, DEST_ROOT)
    print(f"Generated OpenCode Claude-review overlay at {DEST_ROOT}")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
