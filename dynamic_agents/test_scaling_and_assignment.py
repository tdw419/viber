
import unittest
from unittest.mock import patch
from io import StringIO
from . import assign_tasks
from . import scale_agents

class TestScalingAndAssignment(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_assign_task(self, mock_stdout):
        """Test assigning a task to an agent."""
        assign_tasks.assign_task(1, 1)
        self.assertIn("[Simplified] Assigning task 1 to agent 1", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_scale_agents(self, mock_stdout):
        """Test scaling the number of agents."""
        scale_agents.scale_agents("dummy_db_uri", 3) # db_uri is now a dummy
        self.assertIn("[Simplified] Scaling agents to 3", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
