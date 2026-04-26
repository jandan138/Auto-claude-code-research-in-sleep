#!/usr/bin/env python3
"""Generate the base OpenCode skill pack from canonical ARIS skills."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
FIELD_RE_TEMPLATE = r"^{field}:\s*(.+)$"

SUPPORT_ASSET_ROOTS = [
    Path("skills/shared-references"),
    Path("skills/paper-write/templates"),
]

EXTERNAL_REPO_ROOT_DEPENDENCIES = [
    "templates/README.md",
    "templates/RESEARCH_BRIEF_TEMPLATE.md",
    "templates/EXPERIMENT_PLAN_TEMPLATE.md",
    "templates/NARRATIVE_REPORT_TEMPLATE.md",
    "templates/PAPER_PLAN_TEMPLATE.md",
    "templates/RESEARCH_CONTRACT_TEMPLATE.md",
    "docs/PROJECT_FILES_GUIDE.md",
    "docs/SESSION_RECOVERY_GUIDE.md",
]

EXECUTOR_TEXT_REPLACEMENTS = [
    ("Claude Code", "OpenCode"),
    ("Codex MCP", "OpenCode review transport"),
    ("mcp__codex__codex-reply", "opencode_review_reply"),
    ("mcp__codex__codex", "opencode_review_start"),
    ("spawn_agent", "opencode_review_start"),
    ("send_input", "opencode_review_reply"),
    (
        "claude mcp add codex -s user -- codex mcp-server",
        "See docs/OPENCODE_ADAPTATION.md for reviewer transport setup.",
    ),
    ("~/.claude/", "~/.opencode/"),
    ("~/.codex/", "~/.opencode/"),
]

RUNTIME_TEXT_REPLACEMENTS = [
    (
        "**Large file handling**: If the Write tool fails due to file size, immediately retry using Bash (`cat << 'EOF' > file`) to write in chunks. Do NOT ask the user for permission — just do it silently.",
        "**Large file handling**: If a large generated file cannot be written in one pass, retry using any available file-writing method that preserves the intended content without changing workflow semantics.",
    ),
    (
        "**Large file handling**: If the Write tool fails due to file size, use Bash (`cat << 'EOF' > file`) silently.",
        "**Large file handling**: If a large generated file cannot be written in one pass, retry using any available file-writing method that preserves the intended content without changing workflow semantics.",
    ),
    (
        "Fetch and extract content via WebFetch",
        "fetch and extract the page content using available web access",
    ),
    (
        "WebFetch its abstract or landing page",
        "fetch its abstract or landing page using available web access",
    ),
    (
        "WebFetch its abstract and related work section",
        "fetch its abstract and related work section using available web access",
    ),
    (
        "Use the Zotero search tool",
        "Use configured Zotero integration",
    ),
]

REVIEWER_TEXT_REPLACEMENTS = [
    (
        "Send a detailed prompt with xhigh reasoning:",
        "Use the configured external reviewer transport to start a new review with xhigh reasoning:",
    ),
    (
        "Send comprehensive context to the external reviewer:",
        "Use the configured external reviewer transport to start a new review with comprehensive context:",
    ),
    (
        "This gives OpenCode access to `opencode_review_start` and `opencode_review_reply` tools",
        "This adaptation assumes a configured external reviewer transport that can start and continue review threads.",
    ),
    (
        "Use `opencode_review_reply` with the returned `threadId` to continue the conversation:",
        "Use the configured external reviewer continuation mechanism with the returned `threadId` to continue the conversation:",
    ),
    (
        "Use `opencode_review_reply` with the saved threadId:",
        "Use the configured external reviewer continuation mechanism with the saved threadId:",
    ),
    (
        "If this is round 2+, use `opencode_review_reply` with the saved threadId to maintain conversation context.",
        "If this is round 2+, use the configured external reviewer continuation mechanism with the saved threadId to maintain conversation context.",
    ),
    (
        "- **Use `opencode_review_reply`** for Round 2 to maintain conversation context",
        "- **Use the configured external reviewer continuation mechanism** for Round 2 to maintain conversation context",
    ),
    (
        "- Save threadId from first call, use `opencode_review_reply` for subsequent rounds",
        "- Save threadId from the first review call and use the configured external reviewer continuation mechanism for subsequent rounds",
    ),
    (
        "Call REVIEWER_MODEL via OpenCode review transport (`opencode_review_start`) with xhigh reasoning:",
        "Call REVIEWER_MODEL via the configured external reviewer transport with xhigh reasoning:",
    ),
    (
        "Use GPT-5.4 via `opencode_review_reply` (same thread):",
        "Use REVIEWER_MODEL via the configured external reviewer continuation mechanism (same thread):",
    ),
    (
        "If `opencode_review_start` is not available (no OpenAI API key),",
        "If no configured external reviewer transport is available,",
    ),
    (
        "If ``research-review`` is invoked (preferred), it handles the Codex call internally. If calling Codex directly",
        "If ``research-review`` is invoked (preferred), it handles the external reviewer call internally. If using the configured external reviewer continuation mechanism directly",
    ),
    (
        "and use `opencode_review_reply` for later rounds.",
        "and use the configured external reviewer continuation mechanism for later rounds.",
    ),
    (
        "re-submit for another round via `opencode_review_reply`.",
        "re-submit for another round via the configured external reviewer continuation mechanism.",
    ),
    (
        "handles the Codex call internally",
        "handles the external reviewer call internally",
    ),
    (
        "If calling Codex directly",
        "If using the configured external reviewer continuation mechanism directly",
    ),
]


def extract_field(frontmatter: str, field: str) -> str:
    pattern = re.compile(FIELD_RE_TEMPLATE.format(field=re.escape(field)), re.MULTILINE)
    match = pattern.search(frontmatter)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def build_frontmatter(name: str, description: str) -> str:
    safe_description = description.replace('"', '\\"')
    return f'---\nname: "{name}"\ndescription: "{safe_description}"\n---\n\n'


def collect_canonical_skill_dirs(skills_root: Path) -> list[Path]:
    skill_dirs = []
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("skills-"):
            continue
        if (child / "SKILL.md").exists():
            skill_dirs.append(child)
    return skill_dirs


def replace_skill_invocations(body: str, skill_names: list[str]) -> str:
    for skill_name in sorted(skill_names, key=len, reverse=True):
        body = re.sub(
            rf"(?<![:/\w])/(?P<name>{re.escape(skill_name)})(?=[\s`\"'.,;:!?)]|$)",
            rf"`\g<name>`",
            body,
        )
    return body


def protect_urls(text: str) -> tuple[str, dict[str, str]]:
    urls: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        key = f"__URL_{len(urls)}__"
        urls[key] = match.group(0)
        return key

    protected = re.sub(r"https?://[^\s`'\")]+", repl, text)
    return protected, urls


def restore_urls(text: str, urls: dict[str, str]) -> str:
    restored = text
    for key, url in urls.items():
        restored = restored.replace(key, url)
    return restored


def normalize_reviewer_transport_text(text: str) -> str:
    transformed = text
    for old, new in REVIEWER_TEXT_REPLACEMENTS:
        transformed = transformed.replace(old, new)
    transformed = transformed.replace(
        "opencode_review_start:", "external reviewer transport (start):"
    )
    transformed = transformed.replace(
        "opencode_review_reply:", "external reviewer transport (reply):"
    )
    return transformed


def normalize_skill_tool_invocations(text: str, skill_names: list[str]) -> str:
    skill_pattern = "|".join(
        re.escape(name) for name in sorted(skill_names, key=len, reverse=True)
    )

    def repl(match: re.Match[str]) -> str:
        indent = match.group("indent")
        skill = match.group("skill")
        args = match.group("args").strip()
        if "→" in args:
            return match.group(0)
        if args.startswith("->"):
            remainder = args[2:].strip()
            return f"{indent}skill tool → `{skill}` → {remainder}"
        if args:
            return f"{indent}skill tool → `{skill}` with arguments: {args}"
        return f"{indent}skill tool → `{skill}`"

    return re.sub(
        rf"(?m)^(?P<indent>\s*)`(?P<skill>{skill_pattern})`(?P<args>[^\n]*)$",
        repl,
        text,
    )


def transform_text(text: str, skill_names: list[str]) -> str:
    transformed, urls = protect_urls(text)
    for old, new in EXECUTOR_TEXT_REPLACEMENTS:
        transformed = transformed.replace(old, new)
    for old, new in RUNTIME_TEXT_REPLACEMENTS:
        transformed = transformed.replace(old, new)
    transformed = normalize_reviewer_transport_text(transformed)
    transformed = replace_skill_invocations(transformed, skill_names)
    transformed = normalize_skill_tool_invocations(transformed, skill_names)
    return restore_urls(transformed, urls)


def normalize_skill(content: str, skill_names: list[str]) -> str:
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError("Missing skill frontmatter")

    frontmatter = match.group(1)
    body = content[match.end() :].lstrip("\n")
    name = extract_field(frontmatter, "name")
    description = transform_text(extract_field(frontmatter, "description"), skill_names)
    transformed_body = transform_text(body, skill_names)
    return build_frontmatter(name, description) + transformed_body.rstrip() + "\n"


def copy_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def generate_pack(repo_root: Path, dest_root: Path) -> Path:
    skills_root = repo_root / "skills"
    skill_dirs = collect_canonical_skill_dirs(skills_root)
    skill_names = [path.name for path in skill_dirs]

    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    manifest = {
        "pack_type": "base",
        "source_root": "skills",
        "target_root": "skills/skills-opencode",
        "files": [],
        "support_assets": [],
        "support_asset_roots": [str(path) for path in SUPPORT_ASSET_ROOTS],
        "runtime_assets_included": [],
        "external_repo_root_dependencies": EXTERNAL_REPO_ROOT_DEPENDENCIES,
    }

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        source_skill = skill_dir / "SKILL.md"
        target_skill_dir = dest_root / skill_name
        target_skill_dir.mkdir(parents=True, exist_ok=True)
        normalized = normalize_skill(
            source_skill.read_text(encoding="utf-8"), skill_names
        )
        (target_skill_dir / "SKILL.md").write_text(normalized, encoding="utf-8")
        manifest["files"].append(
            {
                "canonical_path": f"skills/{skill_name}/SKILL.md",
                "generated_path": f"skills/skills-opencode/{skill_name}/SKILL.md",
                "kind": "skill",
            }
        )

    for asset_root in SUPPORT_ASSET_ROOTS:
        source_root = repo_root / asset_root
        target_root = dest_root / asset_root.relative_to("skills")
        copy_tree(source_root, target_root)
        for path in sorted(source_root.rglob("*")):
            if path.is_file():
                rel_path = path.relative_to(repo_root).as_posix()
                manifest["support_assets"].append(rel_path)
                manifest["runtime_assets_included"].append(
                    (target_root / path.relative_to(source_root))
                    .relative_to(dest_root)
                    .as_posix()
                )

    manifest_path = dest_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest_path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    dest_root = repo_root / "skills" / "skills-opencode"
    manifest_path = generate_pack(repo_root, dest_root)
    print(f"Generated OpenCode pack at {dest_root}")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()
