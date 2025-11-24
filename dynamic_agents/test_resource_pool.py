
import unittest
import os
import shutil
import lancedb
import pyarrow as pa
from . import resource_pool

class TestResourcePool(unittest.TestCase):

    def setUp(self):
        self.db_uri = "./.test_lancedb"
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)
        
        # Initialize the database and resource pool table
        db = lancedb.connect(self.db_uri)
        resource_pool_schema = pa.schema([
            pa.field("resource_id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("type", pa.string()), # e.g., CPU, GPU, Memory
            pa.field("total", pa.float64()),
            pa.field("available", pa.float64()),
        ])
        db.create_table("resource_pool", schema=resource_pool_schema)
        
        # Set the DB_URI for the resource_pool module
        resource_pool.DB_URI = self.db_uri

    def tearDown(self):
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    def test_get_available_resources(self):
        """Test getting available resources."""
        db = lancedb.connect(self.db_uri)
        resource_pool_tbl = db.open_table("resource_pool")
        resource_pool_tbl.add([
            {"resource_id": 1, "name": "CPU", "type": "CPU", "total": 4.0, "available": 2.0},
            {"resource_id": 2, "name": "GPU", "type": "GPU", "total": 1.0, "available": 1.0},
        ])
        
        resources = resource_pool.get_available_resources()
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0]['name'], 'CPU')
        self.assertEqual(resources[0]['available'], 2.0)

if __name__ == '__main__':
    unittest.main()
