#!/usr/bin/env python3
"""Contract tests for the OpenCode Claude-review overlay generator."""

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "tools" / "generate_opencode_claude_review_overrides.py"


def load_overlay_module():
    spec = importlib.util.spec_from_file_location(
        "generate_opencode_claude_review_overrides", MODULE_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestGenerateOpenCodeClaudeReviewOverrides(unittest.TestCase):
    def test_target_skills_match_core_review_heavy_set(self):
        module = load_overlay_module()

        self.assertEqual(
            module.TARGET_SKILLS,
            [
                "research-review",
                "novelty-check",
                "research-refine",
                "auto-review-loop",
                "paper-plan",
                "paper-figure",
                "paper-write",
                "auto-paper-improvement-loop",
            ],
        )

    def test_generate_overlay_writes_manifest_and_core_files_only(self):
        module = load_overlay_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode-claude-review"
            manifest_path = module.generate_overlay(REPO_ROOT, dest_root)

            self.assertEqual(manifest_path, dest_root / "manifest.json")
            self.assertTrue((dest_root / "README.md").exists())

            entries = sorted(
                path.relative_to(dest_root).as_posix()
                for path in dest_root.rglob("*")
                if path.is_file()
            )
            self.assertEqual(
                entries,
                sorted(
                    [
                        "README.md",
                        "manifest.json",
                        "research-review/SKILL.md",
                        "novelty-check/SKILL.md",
                        "research-refine/SKILL.md",
                        "auto-review-loop/SKILL.md",
                        "paper-plan/SKILL.md",
                        "paper-figure/SKILL.md",
                        "paper-write/SKILL.md",
                        "auto-paper-improvement-loop/SKILL.md",
                    ]
                ),
            )

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["pack_type"], "overlay")
            self.assertEqual(manifest["source_pack"], "skills/skills-opencode")
            self.assertEqual(
                manifest["target_root"], "skills/skills-opencode-claude-review"
            )
            self.assertEqual(manifest["overlay_depends_on"], "skills/skills-opencode")
            self.assertEqual(len(manifest["files"]), 8)
            self.assertTrue(
                all(
                    entry["classification"] == "direct_reviewer_consumer"
                    for entry in manifest["files"]
                )
            )

    def test_overlay_readme_documents_layering_and_bridge_install(self):
        module = load_overlay_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode-claude-review"
            module.generate_overlay(REPO_ROOT, dest_root)

            content = (dest_root / "README.md").read_text(encoding="utf-8")

            self.assertIn("thin override layer", content)
            self.assertIn("skills/skills-opencode/*", content)
            self.assertIn("skills/skills-opencode-claude-review/*", content)
            self.assertIn("mcp-servers/claude-review/server.py", content)
            self.assertIn("review_start", content)
            self.assertIn("review_reply_start", content)
            self.assertIn("review_status", content)

    def test_overlay_converts_reviewer_transport_to_claude_bridge(self):
        module = load_overlay_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode-claude-review"
            module.generate_overlay(REPO_ROOT, dest_root)

            review_content = (dest_root / "research-review" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            novelty_content = (dest_root / "novelty-check" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            refine_content = (dest_root / "research-refine" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            loop_content = (dest_root / "auto-review-loop" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            paper_plan_content = (dest_root / "paper-plan" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            paper_figure_content = (dest_root / "paper-figure" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            paper_write_content = (dest_root / "paper-write" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            auto_paper_content = (
                dest_root / "auto-paper-improvement-loop" / "SKILL.md"
            ).read_text(encoding="utf-8")

            self.assertIn("mcp__claude-review__review_start", review_content)
            self.assertIn("mcp__claude-review__review_reply_start", review_content)
            self.assertIn("mcp__claude-review__review_status", review_content)
            self.assertIn("jobId", review_content)
            self.assertIn("threadId", review_content)
            self.assertNotIn("configured external reviewer transport", review_content)
            self.assertNotIn("gpt-5.4", review_content)
            self.assertNotIn("Must be an OpenAI model", review_content)

            self.assertIn("mcp__claude-review__review_start", novelty_content)
            self.assertIn("mcp__claude-review__review_status", novelty_content)
            self.assertNotIn("configured external reviewer transport", novelty_content)

            self.assertIn("mcp__claude-review__review_start", loop_content)
            self.assertIn("mcp__claude-review__review_reply_start", loop_content)

            stale_model_fields = (
                "model: gpt-5.4",
                "model: REVIEWER_MODEL",
                "REVIEWER_MODEL = `gpt-5.4`",
            )
            for content in (
                review_content,
                novelty_content,
                refine_content,
                loop_content,
                paper_plan_content,
                paper_figure_content,
                paper_write_content,
                auto_paper_content,
            ):
                for token in stale_model_fields:
                    self.assertNotIn(token, content)

    def test_opencode_adaptation_guide_mentions_claude_review_overlay(self):
        content = (REPO_ROOT / "docs" / "OPENCODE_ADAPTATION.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("skills/skills-opencode-claude-review", content)
        self.assertIn("mcp-servers/claude-review/server.py", content)
        self.assertIn("`review_start`", content)
        self.assertIn("`review_reply_start`", content)
        self.assertIn("`review_status`", content)

    def test_overlay_has_no_stale_gpt_or_codex_reviewer_semantics(self):
        module = load_overlay_module()

        forbidden_patterns = [
            re.compile(r"\bGPT-5\.4\b"),
            re.compile(r"from GPT"),
            re.compile(r"\bCodex\b"),
            re.compile(r"codex-reply"),
            re.compile(r"OpenAI model"),
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode-claude-review"
            module.generate_overlay(REPO_ROOT, dest_root)

            offenders = []
            for skill_file in sorted(dest_root.rglob("SKILL.md")):
                content = skill_file.read_text(encoding="utf-8")
                for pattern in forbidden_patterns:
                    if pattern.search(content):
                        offenders.append(
                            f"{skill_file.relative_to(dest_root)}: {pattern.pattern}"
                        )

            self.assertEqual(offenders, [], "\n".join(offenders))

    def test_overlay_has_no_duplicate_claude_review_phrasing(self):
        module = load_overlay_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode-claude-review"
            module.generate_overlay(REPO_ROOT, dest_root)

            offenders = []
            forbidden_substrings = (
                "Claude review via Claude review",
                "Claude-review MCP/Claude-review MCP",
            )
            for skill_file in sorted(dest_root.rglob("SKILL.md")):
                content = skill_file.read_text(encoding="utf-8")
                for token in forbidden_substrings:
                    if token in content:
                        offenders.append(
                            f"{skill_file.relative_to(dest_root)}: {token}"
                        )

            self.assertEqual(offenders, [], "\n".join(offenders))

    def test_overlay_has_no_known_final_residue_strings(self):
        module = load_overlay_module()

        with tempfile.TemporaryDirectory() as tmp_dir:
            dest_root = Path(tmp_dir) / "skills-opencode-claude-review"
            module.generate_overlay(REPO_ROOT, dest_root)

            offenders = []
            forbidden_substrings = (
                "GPT54_AUTO_REVIEW.md",
                "Claude review-5.4",
            )
            for skill_file in sorted(dest_root.rglob("SKILL.md")):
                content = skill_file.read_text(encoding="utf-8")
                for token in forbidden_substrings:
                    if token in content:
                        offenders.append(
                            f"{skill_file.relative_to(dest_root)}: {token}"
                        )

            self.assertEqual(offenders, [], "\n".join(offenders))


if __name__ == "__main__":
    unittest.main()
