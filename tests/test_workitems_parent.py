"""`workitems.py create --parent` passes a number or an issue URL through to gh."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"


class ParentPassThrough(unittest.TestCase):
    def run_create(self, parent):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            log = d / "gh.log"
            gh = d / "gh"
            gh.write_text(f"#!/bin/sh\necho \"$@\" >> {log}\necho https://github.com/o/p/issues/9\n")
            gh.chmod(0o755)
            body = d / "body.md"
            body.write_text("x")
            env = {**os.environ, "PATH": f"{d}{os.pathsep}{os.environ['PATH']}", "REPO": "o/p",
                   "GH_PROJECT": "", "GH_SCRUM_MODE": "labels"}
            subprocess.run([sys.executable, str(SCRIPTS / "workitems.py"), "create", "Story", "T", str(body),
                            "--parent", parent], env=env, check=True, capture_output=True, text=True)
            return log.read_text()

    def test_number(self):
        self.assertIn("--parent 12", self.run_create("12"))

    def test_url_in_another_repo(self):
        url = "https://github.com/o/company/issues/2"
        self.assertIn(f"--parent {url}", self.run_create(url))


if __name__ == "__main__":
    unittest.main()
