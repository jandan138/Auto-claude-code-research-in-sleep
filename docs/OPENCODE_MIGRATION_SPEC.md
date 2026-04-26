# OpenCode Migration Specification for ARIS

> Status: reviewed design spec for landing an OpenCode executor without changing ARIS workflow semantics.

## 1. Goal

This specification defines how to add **OpenCode** as a new executor for ARIS.

The goal is **not** to create a new ARIS variant. The goal is to preserve the existing ARIS research workflow, project state model, and review loop behavior while replacing executor-bound surfaces with OpenCode-compatible ones.

In plain terms: OpenCode migration adds a new **execution shell** around the same ARIS workflow core.

## 2. Canonical Sources and Allowed Outputs

### 2.1 Canonical sources

The following repository surfaces are canonical and must be treated as the source of truth:

- the base ARIS skill tree under `skills/`, excluding any derived executor packs or overlays whose paths begin with `skills/skills-`
- canonical support assets referenced by the base skill tree, including shared references under `skills/shared-references/*`
- canonical runtime assets referenced by canonical skills but stored outside the skill tree, such as `templates/*`
- reviewer contract surfaces referenced by canonical skills, as evidenced by existing reviewer bridges under `mcp-servers/*`; executor-specific bridge implementation details are informative, not workflow-defining
- `docs/PROJECT_FILES_GUIDE.md` — canonical project file contract
- `docs/SESSION_RECOVERY_GUIDE.md` — canonical recovery model and recovery priorities

### 2.2 Allowed OpenCode outputs

The migration may produce only the following executor-specific outputs:

- `skills/skills-opencode/*` — generated OpenCode executor pack
- `skills/skills-opencode-<reviewer>/*` — optional reviewer-specific overlay pack, only if reviewer transport requires a separate layer
- `docs/OPENCODE_ADAPTATION.md` — user-facing OpenCode adaptation guide
- a machine-checkable manifest file at the root of each generated pack or overlay pack

These outputs are **derived artifacts**, not new workflow sources.

## 3. Non-Negotiable Invariants

The following must remain unchanged across the migration:

### 3.1 Workflow invariants

- workflow phase structure
- phase order
- stop conditions
- constant semantics
- orchestrator-to-leaf control flow

### 3.2 Project contract invariants

The migration must preserve canonical ARIS project files and their meanings, including but not limited to:

- `CLAUDE.md`
- `IDEA_REPORT.md`
- `IDEA_CANDIDATES.md`
- `findings.md`
- `EXPERIMENT_LOG.md`
- `docs/research_contract.md`
- `refine-logs/EXPERIMENT_PLAN.md`
- `refine-logs/EXPERIMENT_TRACKER.md`
- `AUTO_REVIEW.md`
- `REVIEW_STATE.json`

OpenCode may document aliases or executor-specific loading behavior, but it may not redefine or rename the canonical project-level contract.

### 3.3 Recovery invariants

Long-running workflows must remain resumable. Migration must preserve the ability to continue work from existing state files rather than forcing a fresh restart.

## 4. Allowed Transformations

Only the following transformation categories are allowed when deriving `skills/skills-opencode/*` from `skills/*`:

### 4.1 Skill invocation transformation

Replace executor-specific skill invocation syntax with OpenCode-compatible skill invocation syntax.

Example category:

- Claude-style `/skill-name`
- any executor-specific wrapper syntax that OpenCode does not support

### 4.2 Reviewer transport transformation

Replace reviewer transport instructions that depend on a different executor with OpenCode-compatible transport instructions.

Example category:

- `mcp__codex__codex`
- `mcp__codex__codex-reply`
- `spawn_agent`
- `send_input`

The prompt content, scoring requirements, round logic, stop conditions, and reviewer continuity model must remain semantically unchanged.

Transport parity must preserve the behavior needed by the canonical flow, including when applicable:

- initial review request
- follow-up reply to an existing review thread
- async or status-polling behavior for long-running review calls
- continuity identifiers needed for later rounds or resume

### 4.3 Executor path hint transformation

Replace executor-specific path hints and user setup instructions with OpenCode-compatible ones.

Example category:

- `~/.claude/...`
- `~/.codex/...`
- executor-specific installation text inside generated skills

### 4.4 Frontmatter and tool declaration transformation

Adjust skill frontmatter and tool declarations so they are valid for OpenCode, including dropping fields OpenCode does not support.

This includes existing repo patterns such as unsupported `allowed-tools`, `argument-hint`, or executor-specific YAML/tool blocks that must be rewritten while preserving workflow meaning.

## 5. Forbidden Transformations

The following changes are forbidden:

- changing workflow stage count or order
- changing the meaning of constants
- changing output file names or file purposes
- changing project state file names or their meanings
- changing recovery semantics
- changing reviewer scoring semantics
- changing orchestrator control flow
- manually maintaining `skills/skills-opencode/*` as an independent long-term source
- deriving OpenCode output from `skills/skills-codex/*` instead of from canonical `skills/*`
- treating any path matching `skills/skills-*` as canonical source input

If any forbidden transformation is required for OpenCode to function, the migration is out of bounds for this spec and must be explicitly re-designed.

## 6. Output Architecture

### 6.1 Canonical pack

`skills/*` remains the only canonical workflow pack.

### 6.2 OpenCode executor pack

`skills/skills-opencode/*` is a generated pack containing OpenCode-compatible skill definitions and required support assets derived directly from `skills/*`.

This pack must be treated as compiled output.

For this purpose, "derived directly from `skills/*`" means from the canonical base skill tree only, excluding any existing derived packs or overlays under paths matching `skills/skills-*`.

Each generated pack must include a machine-checkable manifest file at its root. The manifest must be sufficient to prove provenance, coverage, and layering.

### 6.3 Optional reviewer overlay

If OpenCode requires reviewer-specific transport customizations beyond the base executor pack, those customizations must live in a separate overlay:

- `skills/skills-opencode-<reviewer>/*`

This layer may adjust reviewer transport only. It may not alter workflow logic.

Overlay packs are additive and must be applied after the base OpenCode pack. Each overlay must declare which files it overrides and whether each override is:

- a direct reviewer consumer
- a wrapper or pass-through layer that only reroutes reviewer behavior

Wrapper overrides may not change sub-skill order, stop conditions, file writes, or other orchestration semantics.

## 7. Manifest and Coverage Requirements

The migration must include a machine-checkable manifest that accounts for:

- every canonical skill under `skills/*`
- every generated OpenCode skill under `skills/skills-opencode/*`
- every overlay-provided replacement, if overlays exist
- required support assets such as `skills/shared-references/*` or other non-skill resources used by generated skills
- canonical runtime assets referenced by canonical skills but living outside the skill tree, such as `templates/*`, unless explicitly declared as external repo-root dependencies

At minimum, each generated-pack manifest must record:

- pack type (`base` or `overlay`)
- source tree or source pack
- generated target root
- canonical path for each generated or overridden file
- classification for each override, when overlays exist
- required support assets included in the pack
- runtime assets included in the pack or declared as external dependencies
- overlay dependency or installation precedence, when applicable

An unexplained gap between canonical skills and OpenCode skills is a migration failure.

An unexplained omission of a referenced runtime asset is also a migration failure.

The spec explicitly rejects the pattern where only the visible `SKILL.md` files are generated while hidden dependencies or support assets are omitted.

If the OpenCode pack is intended to work as a standalone installed pack, all referenced runtime assets must either be bundled or replaced with an explicitly documented equivalent. If standalone operation is not intended, the manifest and adaptation guide must explicitly declare the required external repo-root dependencies.

## 8. Resume and State Compatibility Requirements

OpenCode migration must preserve resume compatibility across long-running review and writing flows.

### 8.1 State family coverage

At minimum, state compatibility must be defined for every relevant persisted state family used by migrated flows, including the canonical relative paths used in this repository:

- `REVIEW_STATE.json`
- `refine-logs/REFINE_STATE.json`
- `PAPER_IMPROVEMENT_STATE.json`
- `grant-proposal/GRANT_STATE.json`
- `poster/POSTER_STATE.json`
- `slides/SLIDES_STATE.json`

### 8.2 Backward compatibility rule

OpenCode may define a single preferred field naming convention going forward, but it must support reading legacy forms already present in the repository and in prior executor packs.

This specifically includes compatibility with existing variants such as:

- `threadId`
- `thread_id`
- `agent_id`

The migration may not strand existing projects by requiring a clean-room restart.

### 8.3 Recovery protocol compatibility

OpenCode migration must preserve the repository’s documented recovery protocol, not just the raw existence of state files.

That includes compatibility with the recovery guidance in:

- `docs/SESSION_RECOVERY_GUIDE.md`
- `docs/PROJECT_FILES_GUIDE.md`

Specifically, OpenCode adaptation must preserve the role of:

- `CLAUDE.md` `## Pipeline Status` as the top-level recovery snapshot
- `docs/research_contract.md` as focused active-idea context
- the documented read order used on recovery and after compaction

OpenCode may change how this protocol is loaded, but it may not replace the protocol with a different project-state model.

## 9. Wrapper and Orchestrator Priority

Wrapper and orchestrator skills are the highest-risk migration surface.

This includes top-level skills such as:

- `research-pipeline`
- `idea-discovery`
- `paper-writing`
- `experiment-bridge`
- `rebuttal`
- `grant-proposal`
- `research-refine-pipeline`
- `idea-discovery-robot`
- other workflow wrappers with transitive skill chaining

These skills must be audited before leaf skills because they define the end-to-end control chain.

If a leaf skill is correct but the wrapper still depends on an old executor assumption, the migration is incomplete.

## 10. OpenClaw and Cursor Guidance Boundaries

Existing adaptation guides are evidence, not templates of equal authority.

This rule applies to all executor-specific or reviewer-specific adaptation guides already present in the repository, including Cursor, OpenClaw, Codex reviewer overlays, and related variants.

### 10.1 Cursor guidance

`docs/CURSOR_ADAPTATION.md` is valid evidence that executor substitution can remain mostly surface-level when the underlying workflow contract is preserved.

### 10.2 OpenClaw guidance

`docs/OPENCLAW_ADAPTATION.md` is useful only as a fallback reference for staged execution ideas.

Its alternative output scheme (for example `outputs/*.md`) may **not** replace the canonical ARIS project file contract defined in `docs/PROJECT_FILES_GUIDE.md`.

OpenClaw-style remapping is therefore out of scope for the official OpenCode migration.

## 11. Failure Conditions

The migration fails immediately if any of the following is true:

### 11.1 Semantic failure

The generated OpenCode skill changes workflow logic, stage order, stop conditions, constant meaning, state meaning, or output-file meaning.

### 11.2 Residual executor failure

The generated OpenCode pack still contains unresolved executor-bound residues such as:

- `/skill-name`
- `mcp__codex__*`
- `spawn_agent`
- `send_input`
- `~/.claude/...`
- other unsupported executor-specific path or tool assumptions

### 11.3 Resume failure

Existing project state cannot be resumed correctly after migration.

### 11.4 Coverage failure

Canonical skills, support assets, overlays, or wrapper dependencies are missing without explicit manifest justification.

### 11.5 Source-of-truth failure

The OpenCode pack becomes a hand-maintained long-lived mirror rather than generated output derived from canonical `skills/*`.

## 12. Acceptance Conditions

Migration is accepted only if all of the following are demonstrated:

### 12.1 Structural evidence

There is evidence that the directory layout, skill coverage, support asset coverage, and overlay layering are complete.

### 12.2 Semantic evidence

There is evidence that generated OpenCode skills differ from canonical skills only in allowed transformation categories.

### 12.3 Behavioral evidence

There is evidence that orchestrator → leaf → reviewer → state resume remains a closed and functional chain.

### 12.4 Contract evidence

There is evidence that the canonical ARIS file contract still governs the project and was not silently replaced by an executor-specific alternative.

## 13. Review Order

Migration review must follow this order:

### 13.0 Review pack topology and coverage first

Verify manifest completeness, generated-pack topology, overlay precedence, and support-asset presence before semantic review begins.

### 13.1 Review wrappers and orchestrators first

Verify that top-level workflow control still chains correctly into all required sub-skills.

### 13.2 Review resume behavior second

Verify that state files and reviewer thread continuity remain compatible with existing projects.

### 13.3 Review generated semantic parity third

Verify that the OpenCode pack is a legal derived artifact rather than a drifted rewrite.

### 13.4 Review support assets and runtime references next

Verify that non-skill runtime assets and shared references required by generated skills are present and correctly layered.

### 13.5 Review documentation last

Verify that user setup and installation documentation are complete and consistent.

This order is mandatory because it follows system risk order:

1. broken pack topology or missing assets invalidate later review
2. broken wrapper chain breaks the whole workflow
3. broken resume behavior breaks continuity for long-running research
4. broken semantic parity causes silent protocol drift
5. broken documentation causes delayed usability failures

## 14. Implementation Consequence

Any implementation step taken after this spec is approved must be justified in terms of this document.

That means:

- new generator work must reference the allowed transformations in this spec
- any OpenCode adaptation doc must preserve the canonical file contract defined here
- any reviewer overlay must prove it changes reviewer transport only
- any proposed shortcut that changes workflow semantics must be rejected or re-scoped before implementation

## 15. Summary

This specification defines a constrained migration, not a free-form port.

OpenCode support is valid only if ARIS remains the same system under a different executor shell.

The migration is therefore successful only when:

- canonical `skills/*` remains the sole workflow source of truth
- OpenCode output is generated, not independently authored
- project file and recovery contracts remain intact
- wrapper control flow, reviewer flow, and resume flow remain continuous
- drift is prevented by explicit structural, semantic, and behavioral review gates
