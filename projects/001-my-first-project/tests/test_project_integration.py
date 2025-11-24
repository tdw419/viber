
import unittest
import os
import shutil
from unittest.mock import patch
from io import StringIO
import general_agent

class TestProjectIntegration(unittest.TestCase):

    def setUp(self):
        self.projects_dir = "projects"
        if os.path.exists(self.projects_dir):
            shutil.rmtree(self.projects_dir)

    def tearDown(self):
        if os.path.exists(self.projects_dir):
            shutil.rmtree(self.projects_dir)

    def test_project_new_command(self):
        """Test the 'project new' command in the general agent."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', side_effect=['project new My Integration Test Project', 'exit']):
                general_agent.main()
        
        project_dir = "projects/001-my-integration-test-project"
        self.assertTrue(os.path.exists(project_dir))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "spec.md")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "plan.md")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "checklists")))

if __name__ == '__main__':
    unittest.main()
