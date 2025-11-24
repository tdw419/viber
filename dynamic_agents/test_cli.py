
import unittest
import os
import shutil
import lancedb
import pyarrow as pa
from unittest.mock import patch
from io import StringIO
from . import cli
from projects.llm_os_core import db as llm_os_db

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.db_uri = "./.test_lancedb"
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)
        
        # Initialize the database and all necessary tables
        llm_os_db.DB_URI = self.db_uri # Ensure CLI uses the test DB
        llm_os_db.init_db() # This will create all tables for the test DB

    def tearDown(self):
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_agent_command(self, mock_stdout):
        """
        Test the 'create_agent' command via the CLI.
        """
        with patch('sys.argv', ['cli.py', 'create_agent', 'TestAgent', 'Worker', 'Test Profile']):
            cli.main()
        self.assertIn("Created new agent: TestAgent", mock_stdout.getvalue())
        
        # Verify agent in DB
        db_conn = lancedb.connect(self.db_uri)
        agents_tbl = db_conn.open_table("agents")
        agent_df = agents_tbl.to_pandas()
        self.assertIn("TestAgent", agent_df['name'].values)

    @patch('sys.stdout', new_callable=StringIO)
    def test_monitor_agents_command(self, mock_stdout):
        """
        Test the 'monitor_agents' command via the CLI.
        """
        # First, create an agent so there's something to monitor
        with patch('sys.argv', ['cli.py', 'create_agent', 'MonitorTestAgent', 'Monitor', 'Monitor Profile']):
            cli.main()

        with patch('sys.argv', ['cli.py', 'monitor_agents']):
            cli.main()
        self.assertIn("MonitorTestAgent", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_scale_agents_command(self, mock_stdout):
        """
        Test the 'scale_agents' command via the CLI.
        """
        with patch('sys.argv', ['cli.py', 'scale_agents', '2']):
            cli.main()
        self.assertIn("[Simplified] Scaling agents to 2", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_assign_task_command(self, mock_stdout):
        """
        Test the 'assign_task' command via the CLI.
        """
        # Create a dummy task and agent first
        db_conn = lancedb.connect(self.db_uri)
        tasks_tbl = db_conn.open_table("tasks")
        tasks_tbl.add([{"task_id": 1, "project_id": 1, "status": "PENDING", "created_by_agent_id": 0, "tool_id": 0, "args": "{}", "priority": 1}])
        agents_tbl = db_conn.open_table("agents")
        agents_tbl.add([{"agent_id": 1, "name": "Assignee", "role": "Worker", "prompt_profile": "", "code_ref": ""}])

        with patch('sys.argv', ['cli.py', 'assign_task', '1', '1']):
            cli.main()
        self.assertIn("Assigned task 1 to agent 1", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
