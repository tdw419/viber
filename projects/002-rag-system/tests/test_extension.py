
import unittest
import os
import shutil
from extension import rag
from rag_system import config

class TestExtension(unittest.TestCase):

    def setUp(self):
        self.db_uri = config.DB_URI
        self.table_name = config.TABLE_NAME
        self.test_file = "test_doc.txt"
        with open(self.test_file, "w") as f:
            f.write("This is an integration test document.")
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    def tearDown(self):
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_01_rag_add(self):
        """Test the rag add command."""
        rag(['add', self.test_file])
        # Check that the database was created
        self.assertTrue(os.path.exists(self.db_uri))

    def test_02_rag_query(self):
        """Test the rag query command."""
        # Add a document first
        rag(['add', self.test_file])
        # Now query it
        # This is a bit tricky to test without capturing stdout,
        # but we can at least check that it runs without errors.
        try:
            rag(['query', 'integration test'])
        except Exception as e:
            self.fail(f"rag query command failed with an exception: {e}")

if __name__ == '__main__':
    unittest.main()
