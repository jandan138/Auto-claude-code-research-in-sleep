# OpenCode Adaptation Guide

This guide describes the first OpenCode migration slice for ARIS.

It follows `docs/OPENCODE_MIGRATION_SPEC.md` and preserves the canonical workflow and recovery contract while adding a generated base executor pack.

## What this slice provides

- a generated base pack at `skills/skills-opencode/*`
- a machine-checkable manifest at `skills/skills-opencode/manifest.json`
- bundled support assets copied from the canonical skill tree
- explicit external repo-root dependencies that remain outside the generated pack
- an optional reviewer-specific overlay at `skills/skills-opencode-claude-review/*`

The base slice stays reviewer-neutral. Use the optional `claude-review` overlay when you want review-heavy skills to point to a concrete backend.

## Generate the base pack

From the repository root:

```bash
python3 tools/generate_opencode_pack.py
```

This generates `skills/skills-opencode/*` and writes `skills/skills-opencode/manifest.json`.

## Install the generated pack

This repository currently treats the generated OpenCode pack as a repo-local artifact.

Recommended install sequence:

1. Generate the pack from the repository root:

```bash
python3 tools/generate_opencode_pack.py
```

2. Inspect `skills/skills-opencode/manifest.json` to confirm:
   - the canonical skill coverage you expect
   - bundled support assets are present
   - external repo-root dependencies are declared

3. Keep the generated pack alongside the repository while using this base slice. The current slice still depends on canonical repo-root assets such as `templates/*`, `docs/PROJECT_FILES_GUIDE.md`, and `docs/SESSION_RECOVERY_GUIDE.md`.

4. Do **not** treat `skills/skills-opencode/*` as a hand-maintained source tree. Regenerate it from `tools/generate_opencode_pack.py` whenever the canonical skill tree changes.

5. If you want a concrete Claude-backed reviewer path, generate the overlay too:

```bash
python3 tools/generate_opencode_claude_review_overrides.py
```

This writes `skills/skills-opencode-claude-review/*` and `skills/skills-opencode-claude-review/manifest.json`.

## Use the generated pack

The generated base pack is intended to be read as an OpenCode-oriented executor pack, not as a replacement for the canonical ARIS workflow.

Operational guidance:

- use `skills/skills-opencode/*` for OpenCode-facing execution text
- keep `skills/*` as the canonical workflow source of truth
- keep `CLAUDE.md`, `docs/research_contract.md`, and the canonical state files as the project recovery contract
- rely on `skills/skills-opencode/manifest.json` when checking what was bundled versus what still depends on repo-root files

Reviewer-specific transport should stay layered via `skills/skills-opencode-<reviewer>/*` rather than pushed back into the base pack.

The first concrete reviewer overlay in this repository is:

- `skills/skills-opencode-claude-review/*`

## Reviewer transport prerequisites

Some generated skills, especially `research-review` and review-heavy workflows that depend on it, assume a **configured external reviewer transport** is available to OpenCode.

What this means for the current base slice:

- The base `skills/skills-opencode/*` pack does not install a reviewer backend by itself.
- The base pack only rewrites reviewer-facing wording so the generated skills no longer leak old executor-specific tool names.
- If no configured external reviewer transport is available, review-dependent flows should be treated as documentation-level or partial flows rather than fully runnable end-to-end review loops.

For now, use this rule of thumb:

- wrapper and planning flows can be inspected and followed from the generated base pack
- direct reviewer flows such as `research-review` still require a real OpenCode-side reviewer transport before they become fully runnable

This is why the current base pack is described as OpenCode-oriented, not as a fully standalone OpenCode review stack.

## Claude-review overlay

The recommended first concrete reviewer backend is the existing `claude-review` bridge in this repository.

Generate the overlay:

```bash
python3 tools/generate_opencode_claude_review_overrides.py
```

This produces:

- `skills/skills-opencode-claude-review/*`
- `skills/skills-opencode-claude-review/manifest.json`

Install order for the reviewer path is:

1. base pack: `skills/skills-opencode/*`
2. overlay pack: `skills/skills-opencode-claude-review/*`

The bridge implementation lives at:

- `mcp-servers/claude-review/server.py`

The Claude-review bridge contract exposes:

- `review_start`
- `review_reply_start`
- `review_status`

The overlay uses that bridge to replace neutral reviewer wording in the core review-heavy skills with concrete `mcp__claude-review__review_start`, `mcp__claude-review__review_reply_start`, and `mcp__claude-review__review_status` instructions.

## What the manifest records

The manifest records:

- canonical skill coverage
- bundled support assets from the canonical skill tree
- external repo-root dependencies such as `templates/*`
- target pack location and provenance

Review the generated `manifest.json` before copying the pack elsewhere.

## Generated wording conventions

The generated base pack intentionally rewrites obvious executor-specific runtime prose into more neutral capability wording.

In practice this means:

- slash-command references are rewritten into skill-name references that the OpenCode adaptation can interpret
- obvious Codex or Claude transport names are removed from the generated base pack
- runtime-facing instructions like `Write tool`, `WebFetch`, or `Zotero search tool` are rewritten into executor-neutral wording when the workflow semantics are unchanged
- reviewer-facing placeholder tool names are rewritten toward neutral external-reviewer wording in the base pack
- single-line wrapper command blocks are rewritten toward explicit skill-tool instructions when the underlying workflow intent is unchanged

This keeps the base pack closer to a runnable OpenCode-oriented pack without claiming support for a reviewer overlay that has not been implemented yet.

## Recovery and project contract

OpenCode support does **not** replace the ARIS project-state contract.

Keep using the canonical project files and recovery flow documented in:

- `docs/PROJECT_FILES_GUIDE.md`
- `docs/SESSION_RECOVERY_GUIDE.md`

In particular:

- keep `CLAUDE.md` as the project dashboard
- keep `CLAUDE.md` `## Pipeline Status` as the top-level recovery snapshot
- keep `docs/research_contract.md` as focused active-idea context
- keep canonical state files and their meanings unchanged

## Current external dependencies

This first slice keeps some runtime assets at repo root instead of bundling them into the generated pack. See `skills/skills-opencode/manifest.json` for the exact list.

At minimum, expect repo-root references to include templates under `templates/*`.

## Minimal smoke workflow

The current base slice is strong enough to support a minimal documentation-level smoke chain:

1. Start from the generated pipeline entry:

```text
skill tool → `idea-discovery` with arguments: "$ARGUMENTS"
```

2. Inside `idea-discovery`, the generated pack should still chain the canonical workflow:

```text
``research-lit`` → ``idea-creator`` → ``novelty-check`` → ``research-review``
```

3. For a direct review step, the generated `research-review` skill should describe:

```text
Use the configured external reviewer transport to start a new review
Use the configured external reviewer continuation mechanism
```

4. For a direct critical-review call from idea validation, the generated pack should expose:

```text
skill tool → `research-review` with arguments: "[top idea with hypothesis + pilot results]"
```

This smoke workflow does not prove a reviewer backend is installed. It proves the generated base pack preserves a coherent short chain from wrapper entry to external-review wording without leaking old executor-specific residue.

If the `claude-review` overlay is installed, the review-heavy skills in that overlay should point to the concrete Claude-review MCP backend instead of the base pack’s neutral reviewer wording.

## Verification

Run the contract tests:

```bash
python3 -m unittest tests.test_generate_opencode_pack -v
python3 -m unittest tests.test_generate_opencode_claude_review_overrides -v
```

Then regenerate the pack and inspect the diff:

```bash
python3 tools/generate_opencode_pack.py
python3 tools/generate_opencode_claude_review_overrides.py
git diff -- skills/skills-opencode skills/skills-opencode-claude-review docs/OPENCODE_ADAPTATION.md
```
