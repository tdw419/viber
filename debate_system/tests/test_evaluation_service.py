
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from debate_system.services.evaluation_service import EvaluationService
from debate_system.models.debate import Debate
from debate_system.models.agent import Agent

class TestEvaluationService(unittest.TestCase):

    def test_evaluate_debate(self):
        """Test the debate evaluation."""
        service = EvaluationService()
        participants = [Agent(id=1, name="Agent 1")]
        debate = Debate(id=1, topic="Test", participants=participants, messages=["Message 1", "Message 2"])
        score = service.evaluate_debate(debate)
        self.assertEqual(score, 0.2)

if __name__ == '__main__':
    unittest.main()
