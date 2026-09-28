"""
Unit tests for ACL Guardrails (Trap T6)
"""

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from security.acl.acl_guard import check_acl, filter_allowed_chunks

class TestACLGuard(unittest.TestCase):

    def test_public_internal_allowed_for_all(self):
        allowed = check_acl("public-internal", [], [], "web-dev", "Leo Kim")
        self.assertTrue(allowed)

    def test_team_tier_blocks_other_teams(self):
        # cloud-eng doc should block web-dev
        allowed = check_acl("team", ["cloud-eng"], [], "web-dev", "Leo Kim")
        self.assertFalse(allowed)

        # cloud-eng doc should allow cloud-eng
        allowed_own = check_acl("team", ["cloud-eng"], [], "cloud-eng", "Marta Silva")
        self.assertTrue(allowed_own)

    def test_restricted_tier_trap_t6(self):
        # RET-001 is restricted to Nina Park and Marta Silva
        allowed_leo = check_acl("restricted", [], ["Nina Park", "Marta Silva"], "web-dev", "Leo Kim")
        self.assertFalse(allowed_leo)

        allowed_nina = check_acl("restricted", [], ["Nina Park", "Marta Silva"], "web-dev", "Nina Park")
        self.assertTrue(allowed_nina)

if __name__ == "__main__":
    unittest.main()
