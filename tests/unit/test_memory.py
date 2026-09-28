"""
Unit tests for Hindsight Memory Client
"""

import sys
import os
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from memory import hindsight_client as hc

class TestHindsightMemory(unittest.TestCase):

    def test_retain_and_recall_basic(self):
        mem_id = hc.retain(
            bank="org-shared",
            key="incident:TEST-INC-99",
            content={
                "verdict": "confirmed",
                "root_cause": "Test DB timeout caused by bad config.",
                "resolution": "Fixed pool config.",
                "citations": ["DOC-WEB-001"],
            },
            acl_ceiling="public-internal",
        )
        self.assertTrue(bool(mem_id))

        hit = hc.recall(
            bank="org-shared",
            query="What caused TEST-INC-99?",
            min_confidence=0.80,
        )
        self.assertIsNotNone(hit)
        self.assertEqual(hit.content.get("verdict"), "confirmed")
        self.assertIn("bad config", hit.content.get("root_cause"))

    def test_acl_ceiling_team_block(self):
        hc.retain(
            bank="team-ml",
            key="incident:ML-PRIVATE-01",
            content={
                "verdict": "confirmed",
                "owner_team": "ml-eng",
                "root_cause": "ML internal weights",
            },
            acl_ceiling="team",
        )

        # web-dev user should be blocked from ml-eng team bank
        hit = hc.recall(
            bank="team-ml",
            query="What is ML-PRIVATE-01?",
            requester_team="web-dev",
        )
        self.assertIsNone(hit)

if __name__ == "__main__":
    unittest.main()
