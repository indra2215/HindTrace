"""
End-to-End Integration Tests for HindTrace
"""
import os
import sys
from pathlib import Path
import unittest

os.environ.setdefault("GROQ_API_KEY", "gsk_test_dummy_for_testing")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from agents.pipeline import stage1_router
from security.acl.acl_guard import check_acl
from memory.hindsight_client import recall, retain

class TestEndToEndHindTrace(unittest.TestCase):
    def test_pipeline_router(self):
        """Smoke test verifying stage 1 router analyzes query properly."""
        res = stage1_router("Investigating CRITICAL Kubernetes pod crash INC-402", "Marta Silva")
        self.assertIn("investigation_id", res)
        self.assertIn("user_team", res)
        self.assertEqual(res["user_team"], "cloud-eng")
        self.assertIn("INC-402", res["incident_ids"])

    def test_memory_lifecycle(self):
        """Tests retain and recall contract."""
        test_id = "incident:INC-INTEG-99"
        retain(
            bank="org-shared",
            key=test_id,
            content={
                "root_cause": "Memory integration test cause",
                "resolution": "Applied fix A",
                "verdict": "resolved"
            },
            acl_ceiling="public-internal"
        )
        hit = recall(
            bank="org-shared",
            query="What caused INC-INTEG-99?",
            min_confidence=0.80
        )
        self.assertIsNotNone(hit)
        self.assertEqual(hit.content.get("verdict"), "resolved")

    def test_acl_security_enforcement(self):
        """Tests that unauthorized users cannot view restricted documents."""
        # Restricted document allowed only for Nina Park and Marta Silva
        allowed = check_acl("restricted", [], ["Nina Park", "Marta Silva"], "web-dev", "Leo Kim")
        self.assertFalse(allowed)

        allowed_sre = check_acl("restricted", [], ["Nina Park", "Marta Silva"], "cloud-eng", "Marta Silva")
        self.assertTrue(allowed_sre)

if __name__ == "__main__":
    unittest.main()

