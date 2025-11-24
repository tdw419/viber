
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from debate_system.services.debate_service import DebateService
from debate_system.models.agent import Agent

class TestDebateService(unittest.TestCase):

    def test_create_debate(self):
        """Test creating a new debate."""
        service = DebateService()
        participants = [Agent(id=1, name="Agent 1"), Agent(id=2, name="Agent 2")]
        debate = service.create_debate("Test Topic", participants)
        self.assertEqual(debate.id, 1)
        self.assertEqual(debate.topic, "Test Topic")
        self.assertEqual(len(debate.participants), 2)

    def test_get_debate(self):
        """Test getting a debate by its ID."""
        service = DebateService()
        participants = [Agent(id=1, name="Agent 1")]
        debate = service.create_debate("Another Topic", participants)
        retrieved_debate = service.get_debate(debate.id)
        self.assertEqual(retrieved_debate.id, debate.id)

    def test_agent_interaction(self):
        """Test the agent interaction methods."""
        service = DebateService()
        participants = [Agent(id=1, name="Agent 1"), Agent(id=2, name="Agent 2")]
        debate = service.create_debate("Interaction Test", participants)
        
        service.post_message(debate.id, 1, "Hello, everyone.")
        service.post_message(debate.id, 2, "Hello, Agent 1.")
        
        messages = service.get_messages(debate.id)
        self.assertEqual(len(messages), 2)
        self.assertIn("Agent 1: Hello, everyone.", messages[0])
        self.assertIn("Agent 2: Hello, Agent 1.", messages[1])

if __name__ == '__main__':
    unittest.main()
