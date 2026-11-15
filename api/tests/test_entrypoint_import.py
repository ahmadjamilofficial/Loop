"""Regression test for importing the Vercel entry point from arbitrary cwd."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ENTRYPOINT = Path(__file__).resolve().parents[1] / "app" / "main.py"


class EntrypointImportTest(unittest.TestCase):
    def test_entrypoint_imports_outside_repository_directory(self) -> None:
        with tempfile.TemporaryDirectory() as working_directory:
            completed = subprocess.run(
                [sys.executable, str(ENTRYPOINT)],
                cwd=working_directory,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(
            completed.returncode,
            0,
            msg=f"Entry point failed to import:\n{completed.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
