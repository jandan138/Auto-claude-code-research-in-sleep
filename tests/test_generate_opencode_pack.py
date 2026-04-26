#!/usr/bin/env python3
"""Contract tests for OpenCode pack generation."""

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "tools" / "generate_opencode_pack.py"


def load_generator_module():
    spec = importlib.util.spec_from_file_location("generate_opencode_pack", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestGenerateOpenCodePack(unittest.TestCase):
    def test_collect_canonical_skill_dirs_excludes_derived_packs(self):
        module = load_generator_module()

        skill_dirs = module.collect_canonical_skill_dirs(REPO_ROOT / "skills")
        names = {path.name for path in skill_dirs}

        self.assertIn("research-review", names)
        self.assertIn("auto-review-loop", names)
        self.assertNotIn("skills-codex", names)
        self.assertNotIn("skills-codex-claude-review", names)
        self.assertTrue(all(not name.startswith("skills-") for name in names))

    def test_generate_pack_writes_manifest_and_required_assets(self):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            manifest_path = module.generate_pack(REPO_ROOT, dest_root)

            self.assertEqual(manifest_path, dest_root / "manifest.json")
            self.assertTrue(manifest_path.exists())
            self.assertTrue(
                (dest_root / "shared-references" / "writing-principles.md").exists()
            )
            self.assertTrue((dest_root / "paper-write" / "templates").is_dir())

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["pack_type"], "base")
            self.assertEqual(manifest["source_root"], "skills")
            self.assertEqual(manifest["target_root"], "skills/skills-opencode")
            self.assertIn(
                "skills/research-review/SKILL.md",
                {entry["canonical_path"] for entry in manifest["files"]},
            )
            self.assertIn(
                "skills/shared-references/writing-principles.md",
                manifest["support_assets"],
            )
            self.assertIn(
                "skills/paper-write/templates", manifest["support_asset_roots"]
            )
            self.assertIn(
                "templates/RESEARCH_BRIEF_TEMPLATE.md",
                manifest["external_repo_root_dependencies"],
            )

    def test_generated_skill_frontmatter_is_normalized(self):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            content = (dest_root / "research-review" / "SKILL.md").read_text(
                encoding="utf-8"
            )

            self.assertIn('name: "research-review"', content)
            self.assertIn(
                'description: "Get a deep critical review of research from GPT via',
                content,
            )
            self.assertNotIn("allowed-tools:", content)
            self.assertNotIn("argument-hint:", content)

    def test_generated_skills_remove_executor_specific_residue(self):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            review_content = (dest_root / "research-review" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            wrapper_content = (dest_root / "idea-discovery" / "SKILL.md").read_text(
                encoding="utf-8"
            )

            self.assertNotIn("mcp__codex__codex", review_content)
            self.assertNotIn("mcp__codex__codex-reply", review_content)
            self.assertNotIn("claude mcp add codex", review_content)
            self.assertNotIn("Claude Code", review_content)
            self.assertIn("external reviewer transport", review_content)
            self.assertIn("external reviewer continuation mechanism", review_content)
            self.assertNotIn("/research-lit", wrapper_content)
            self.assertIn("`research-lit`", wrapper_content)

    def test_skill_invocation_rewrite_does_not_corrupt_urls(self):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            wrapper_content = (dest_root / "idea-discovery" / "SKILL.md").read_text(
                encoding="utf-8"
            )

            self.assertIn("https://arxiv.org/abs/2406.04329", wrapper_content)
            self.assertNotIn("https:/`arxiv`", wrapper_content)

    def test_opencode_adaptation_guide_exists_with_core_constraints(self):
        guide_path = REPO_ROOT / "docs" / "OPENCODE_ADAPTATION.md"

        self.assertTrue(guide_path.exists())
        content = guide_path.read_text(encoding="utf-8")

        self.assertIn("skills/skills-opencode", content)
        self.assertIn("manifest.json", content)
        self.assertIn("CLAUDE.md", content)
        self.assertIn("PROJECT_FILES_GUIDE.md", content)
        self.assertIn("SESSION_RECOVERY_GUIDE.md", content)

    def test_opencode_adaptation_guide_includes_install_use_and_smoke_sections(self):
        guide_path = REPO_ROOT / "docs" / "OPENCODE_ADAPTATION.md"
        content = guide_path.read_text(encoding="utf-8")

        self.assertIn("## Install the generated pack", content)
        self.assertIn("## Use the generated pack", content)
        self.assertIn("## Minimal smoke workflow", content)
        self.assertIn("python3 tools/generate_opencode_pack.py", content)
        self.assertIn("skills/skills-opencode/manifest.json", content)
        self.assertIn("skill tool → `idea-discovery`", content)
        self.assertIn("skill tool → `research-review`", content)

    def test_opencode_adaptation_guide_covers_reviewer_transport_prerequisites(self):
        guide_path = REPO_ROOT / "docs" / "OPENCODE_ADAPTATION.md"
        content = guide_path.read_text(encoding="utf-8")

        self.assertIn("## Reviewer transport prerequisites", content)
        self.assertIn("configured external reviewer transport", content)
        self.assertIn(
            "The base `skills/skills-opencode/*` pack does not install a reviewer backend by itself",
            content,
        )
        self.assertIn("`research-review`", content)

    def test_generated_pack_has_no_forbidden_reviewer_tokens(self):
        module = load_generator_module()
        forbidden = (
            "opencode_review_start",
            "opencode_review_reply",
            "Write tool",
            "WebFetch",
            "Zotero search tool",
            "cat << 'EOF' > file",
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            offenders = []
            for skill_file in sorted(dest_root.rglob("SKILL.md")):
                content = skill_file.read_text(encoding="utf-8")
                for token in forbidden:
                    if token in content:
                        offenders.append(
                            f"{skill_file.relative_to(dest_root)}: {token}"
                        )

            self.assertEqual(offenders, [], "\n".join(offenders))

    def test_generated_pack_has_no_malformed_wrapper_invocations(self):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            offenders = []
            pattern = re.compile(r"skill tool → `[^`]+` with arguments:\s*->")
            for skill_file in sorted(dest_root.rglob("SKILL.md")):
                content = skill_file.read_text(encoding="utf-8")
                if pattern.search(content):
                    offenders.append(str(skill_file.relative_to(dest_root)))

            self.assertEqual(offenders, [], "\n".join(offenders))

    def test_generated_pack_supports_minimal_workflow_smoke_chain(self):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            pipeline_content = (dest_root / "research-pipeline" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            discovery_content = (dest_root / "idea-discovery" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            review_content = (dest_root / "research-review" / "SKILL.md").read_text(
                encoding="utf-8"
            )

            self.assertIn("This internally runs:", pipeline_content)
            self.assertIn(
                "``research-lit`` → ``idea-creator`` → ``novelty-check`` → ``research-review``",
                pipeline_content,
            )
            self.assertIn(
                'skill tool → `idea-discovery` with arguments: "$ARGUMENTS"',
                pipeline_content,
            )
            self.assertIn(
                'skill tool → `research-review` with arguments: "[top idea with hypothesis + pilot results]"',
                discovery_content,
            )
            self.assertIn(
                "Use the configured external reviewer transport to start a new review",
                review_content,
            )
            self.assertIn(
                "Use the configured external reviewer continuation mechanism",
                review_content,
            )

    def test_generated_skills_neutralize_runtime_tool_residue(self):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            pipeline_content = (dest_root / "research-pipeline" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            idea_content = (dest_root / "idea-discovery" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            novelty_content = (dest_root / "novelty-check" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            lit_content = (dest_root / "research-lit" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            poster_content = (dest_root / "paper-poster" / "SKILL.md").read_text(
                encoding="utf-8"
            )

            self.assertNotIn("Write tool", pipeline_content)
            self.assertNotIn("cat << 'EOF' > file", pipeline_content)
            self.assertIn(
                "If a large generated file cannot be written in one pass",
                pipeline_content,
            )
            self.assertNotIn("Write tool", poster_content)
            self.assertNotIn("cat << 'EOF' > file", poster_content)

            self.assertNotIn("WebFetch", idea_content)
            self.assertNotIn("WebFetch", novelty_content)
            self.assertIn(
                "fetch and extract the page content using available web access",
                idea_content,
            )
            self.assertIn(
                "fetch its abstract and related work section using available web access",
                novelty_content,
            )

            self.assertNotIn("Zotero search tool", lit_content)
            self.assertIn("configured Zotero integration", lit_content)

    def test_generated_skills_neutralize_reviewer_and_wrapper_execution_placeholders(
        self,
    ):
        module = load_generator_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode"
            module.generate_pack(REPO_ROOT, dest_root)

            review_content = (dest_root / "research-review" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            loop_content = (dest_root / "auto-review-loop" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            paper_loop_content = (
                dest_root / "auto-paper-improvement-loop" / "SKILL.md"
            ).read_text(encoding="utf-8")
            creator_content = (dest_root / "idea-creator" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            novelty_content = (dest_root / "novelty-check" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            grant_content = (dest_root / "grant-proposal" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            refine_content = (dest_root / "research-refine" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            slides_content = (dest_root / "paper-slides" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            idea_content = (dest_root / "idea-discovery" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            pipeline_content = (dest_root / "research-pipeline" / "SKILL.md").read_text(
                encoding="utf-8"
            )

            self.assertNotIn("opencode_review_start:", review_content)
            self.assertNotIn("opencode_review_reply", review_content)
            self.assertIn(
                "Use the configured external reviewer transport to start a new review",
                review_content,
            )
            self.assertIn(
                "Use the configured external reviewer continuation mechanism",
                review_content,
            )

            self.assertNotIn("opencode_review_start:", loop_content)
            self.assertNotIn("opencode_review_reply", loop_content)
            self.assertIn(
                "Use the configured external reviewer transport to start a new review",
                loop_content,
            )
            self.assertNotIn("opencode_review_reply", paper_loop_content)
            self.assertIn(
                "Use the configured external reviewer continuation mechanism",
                paper_loop_content,
            )
            self.assertNotIn("opencode_review_reply", creator_content)
            self.assertIn(
                "Use REVIEWER_MODEL via the configured external reviewer continuation mechanism",
                creator_content,
            )
            self.assertNotIn("opencode_review_start", novelty_content)
            self.assertIn(
                "Call REVIEWER_MODEL via the configured external reviewer transport",
                novelty_content,
            )
            self.assertNotIn("opencode_review_start", slides_content)
            self.assertIn(
                "If no configured external reviewer transport is available",
                slides_content,
            )
            self.assertNotIn("opencode_review_start", grant_content)
            self.assertNotIn("opencode_review_reply", grant_content)
            self.assertNotIn("Codex call internally", grant_content)
            self.assertIn("external reviewer call internally", grant_content)
            self.assertNotIn("opencode_review_reply", refine_content)
            self.assertIn(
                "use the configured external reviewer continuation mechanism for later rounds",
                refine_content,
            )

            self.assertNotIn('`research-lit` "$ARGUMENTS"', idea_content)
            self.assertIn(
                'skill tool → `research-lit` with arguments: "$ARGUMENTS"', idea_content
            )

            self.assertNotIn("`run-experiment` [experiment command]", pipeline_content)
            self.assertIn(
                "skill tool → `run-experiment` with arguments: [experiment command]",
                pipeline_content,
            )


if __name__ == "__main__":
    unittest.main()
