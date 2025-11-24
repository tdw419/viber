
import unittest
import os
import shutil
import project_service

class TestProjectService(unittest.TestCase):

    def setUp(self):
        self.projects_dir = "projects"
        if os.path.exists(self.projects_dir):
            shutil.rmtree(self.projects_dir)
        os.makedirs(self.projects_dir)

    def tearDown(self):
        if os.path.exists(self.projects_dir):
            shutil.rmtree(self.projects_dir)

    def test_create_project(self):
        """Test creating a new project."""
        project_service.create_project("My Test Project")
        project_dir = "projects/001-my-test-project"
        self.assertTrue(os.path.exists(project_dir))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "spec.md")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "plan.md")))
        self.assertTrue(os.path.exists(os.path.join(project_dir, "checklists")))

if __name__ == '__main__':
    unittest.main()
