from __future__ import annotations

import unittest

from scripts.seed_local_data import validate_demo_universe


class SeedDataTests(unittest.TestCase):
    def test_demo_universe_validates(self) -> None:
        self.assertEqual(validate_demo_universe(), [])


if __name__ == "__main__":
    unittest.main()
