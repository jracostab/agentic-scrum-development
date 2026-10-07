"""Hermes path handling and installer safety. Stdlib unittest only.

Run: python3 -m unittest discover -s tests -t .
"""

import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CLEAN = {"COFOUNDER_PROFILE": "", "HERMES_PROFILE": "", "AGENTIC_SCRUM_PROFILE": "",
         "CLAUDE_AGENT_NAME": "", "AGENTIC_SCRUM_AGENT": "", "CLAUDECODE": ""}


class BindingPaths(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "profiles" / "acme-cto").mkdir(parents=True)
        self.sb = load("scrum_bindings")

    def env(self, **kw):
        return mock.patch.dict(os.environ, {**CLEAN, **kw})

    def test_inside_hermes_session_profile_dir_home(self):
        # `hermes -p acme-cto` sets HERMES_HOME to the profile dir and no HERMES_PROFILE.
        with self.env(HERMES_HOME=str(self.root / "profiles" / "acme-cto")):
            self.assertEqual(self.sb.hermes_home(), self.root)
            self.assertEqual(self.sb.profile_name(), "acme-cto")
            self.assertEqual(self.sb.binding_path(),
                             self.root / "profiles" / "acme-cto" / "scrum-bindings.yaml")

    def test_shell_with_install_root_and_hermes_profile(self):
        with self.env(HERMES_HOME=str(self.root), HERMES_PROFILE="acme-de"):
            self.assertEqual(self.sb.binding_path(),
                             self.root / "profiles" / "acme-de" / "scrum-bindings.yaml")

    def test_explicit_profile_still_wins(self):
        with self.env(HERMES_HOME=str(self.root / "profiles" / "acme-cto"), COFOUNDER_PROFILE="tinto"):
            self.assertEqual(self.sb.profile_name(), "tinto")
            self.assertEqual(self.sb.binding_path(),
                             self.root / "profiles" / "tinto" / "scrum-bindings.yaml")


class InstallerPaths(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.inst = load("install_skills")

    def test_skills_root_from_profile_dir_home(self):
        with mock.patch.dict(os.environ, {"HERMES_HOME": str(self.root / "profiles" / "acme-cto")}):
            self.assertEqual(self.inst.hermes_skills_root(), self.root / "skills")

    def test_skills_root_from_install_root(self):
        with mock.patch.dict(os.environ, {"HERMES_HOME": str(self.root)}):
            self.assertEqual(self.inst.hermes_skills_root(), self.root / "skills")


class ReplaceLinkSafety(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.pack = self.tmp / "pack"
        (self.pack / "skills" / "ceo").mkdir(parents=True)
        (self.pack / "SKILL.md").write_text("pack")
        self.inst = load("install_skills")

    def quiet(self):
        return contextlib.redirect_stdout(io.StringIO())

    def test_pack_folder_as_destination_is_left_alone(self):
        with self.quiet():
            self.inst.replace_link(self.pack, self.pack)
        self.assertEqual((self.pack / "SKILL.md").read_text(), "pack")

    def test_refuses_to_replace_a_folder_containing_the_pack(self):
        with self.assertRaises(SystemExit):
            self.inst.replace_link(self.pack / "skills" / "ceo", self.pack)
        self.assertTrue((self.pack / "SKILL.md").exists())

    def test_existing_link_to_pack_is_idempotent(self):
        dest = self.tmp / "skills" / "agentic-scrum"
        with self.quiet():
            self.inst.replace_link(self.pack, dest)
            self.inst.replace_link(self.pack, dest)
        self.assertTrue(dest.is_symlink())
        self.assertEqual(dest.resolve(), self.pack.resolve())

    def test_unrelated_stale_folder_is_still_replaced(self):
        dest = self.tmp / "skills" / "agentic-scrum-ceo"
        dest.mkdir(parents=True)
        (dest / "old.md").write_text("stale")
        with self.quiet():
            self.inst.replace_link(self.pack / "skills" / "ceo", dest)
        self.assertTrue(dest.is_symlink())


if __name__ == "__main__":
    unittest.main()
