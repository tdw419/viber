
import unittest
import os
import shutil
import lancedb
import pyarrow as pa
from . import create_agent
from . import monitor_agents

class TestAgentManagement(unittest.TestCase):

    def setUp(self):
        self.db_uri = "./.test_lancedb"
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)
        
        # Initialize the database
        db = lancedb.connect(self.db_uri)
        agents_schema = create_agent.pa.schema([
            create_agent.pa.field("agent_id", create_agent.pa.int64()),
            create_agent.pa.field("name", create_agent.pa.string()),
            create_agent.pa.field("role", create_agent.pa.string()),
            create_agent.pa.field("prompt_profile", create_agent.pa.string()),
            create_agent.pa.field("code_ref", create_agent.pa.string()),
        ])
        db.create_table("agents", schema=agents_schema)
        
        create_agent.DB_URI = self.db_uri
        monitor_agents.DB_URI = self.db_uri

    def tearDown(self):
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    def test_create_and_monitor_agent(self):
        """Test creating and monitoring an agent."""
        create_agent.create_agent("Test Agent", "Tester", "This is a test agent.")
        
        # To test monitor_agents, we'll capture stdout
        from io import StringIO
        import sys
        
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            monitor_agents.monitor_agents()
            output = out.getvalue().strip()
            self.assertIn("Test Agent", output)
        finally:
            sys.stdout = saved_stdout

if __name__ == '__main__':
    unittest.main()
