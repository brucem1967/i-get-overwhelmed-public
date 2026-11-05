"""The always-on hook prints nothing without the flag, and the rules + reader profile (no frontmatter) with it."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class HookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.root / "hooks")
        shutil.copytree(ROOT / "skills", self.root / "skills")
        self.cfg = Path(self.tmp.name) / "claude config"
        self.cfg.mkdir()

    def run_hook(self):
        env = dict(os.environ, CLAUDE_CONFIG_DIR=str(self.cfg))
        return subprocess.run([shutil.which("sh"), str(self.root / "hooks" / "always-on.sh")],
                              capture_output=True, text=True, env=env, timeout=30)

    def test_silent_without_flag(self):
        r = self.run_hook()
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "")

    def test_rules_and_profile_with_flag(self):
        (self.cfg / ".i-get-overwhelmed-always").write_text("")
        (self.root / "skills" / "i-get-overwhelmed" / "READER.md").write_text("## Sam\n- not technical\n")
        r = self.run_hook()
        self.assertEqual(r.returncode, 0)
        out = r.stdout
        self.assertTrue(out.startswith("OVERWHELM MODE ACTIVE"))
        self.assertIn("### 3. One thing at a time", out)
        self.assertNotIn("disable-model-invocation", out)      # frontmatter stripped
        self.assertIn("# Reader profile (follow", out)
        self.assertIn("## Sam", out)

    def test_no_profile_is_fine(self):
        (self.cfg / ".i-get-overwhelmed-always").write_text("")
        r = self.run_hook()
        self.assertEqual(r.returncode, 0)
        self.assertNotIn("# Reader profile (follow", r.stdout)


if __name__ == "__main__":
    unittest.main()
