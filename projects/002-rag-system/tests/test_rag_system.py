
import unittest
import os
import shutil
import lancedb
from rag_system import db, embed, query

class TestRAGSystem(unittest.TestCase):

    def setUp(self):
        self.db_uri = "./.test_lancedb"
        self.table_name = "test_documents"
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    def tearDown(self):
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    def test_01_embed(self):
        """Test the embedding function."""
        text = "This is a test sentence."
        embedding = embed.get_embedding(text)
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 384)

    def test_02_db_creation(self):
        """Test the database creation."""
        schema = db.pa.schema(
            [
                db.pa.field("vector", db.pa.list_(db.pa.float32(), 384)),
                db.pa.field("text", db.pa.string()),
            ]
        )
        tbl = db.create_table(self.db_uri, self.table_name, schema)
        self.assertIsNotNone(tbl)

    def test_03_db_add_and_query(self):
        """Test adding documents and querying."""
        # 1. Create table
        schema = db.pa.schema(
            [
                db.pa.field("vector", db.pa.list_(db.pa.float32(), 384)),
                db.pa.field("text", db.pa.string()),
            ]
        )
        db.create_table(self.db_uri, self.table_name, schema)

        # 2. Add documents
        docs = [
            {"text": "This is the first document."},
            {"text": "This is the second document."},
        ]
        for doc in docs:
            doc["vector"] = embed.get_embedding(doc["text"])
        
        db.add_documents(self.db_uri, self.table_name, docs)

        # 3. Query
        query.DB_URI = self.db_uri
        query.TABLE_NAME = self.table_name
        results = query.search_documents("first document")
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn("first document", results[0]["text"])

if __name__ == '__main__':
    unittest.main()
