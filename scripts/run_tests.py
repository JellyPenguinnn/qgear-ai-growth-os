from __future__ import annotations

import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "packages" / "qgear-core" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "qgear-ingest" / "src"))
sys.path.insert(0, str(ROOT / "packages" / "qgear-ai" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "api"))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
