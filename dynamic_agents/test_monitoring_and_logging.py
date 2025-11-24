
import unittest
import os
import shutil
import lancedb
import pyarrow as pa
import datetime
from . import collect_metrics

class TestMonitoringAndLogging(unittest.TestCase):

    def setUp(self):
        self.db_uri = "./.test_lancedb"
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)
        
        # Initialize the database and metrics table
        db = lancedb.connect(self.db_uri)
        metrics_schema = pa.schema([
            pa.field("timestamp", pa.timestamp('ns')),
            pa.field("cpu_percent", pa.float64()),
            pa.field("memory_percent", pa.float64()),
        ])
        db.create_table("metrics", schema=metrics_schema)
        
        # Set the DB_URI for the collect_metrics module
        collect_metrics.DB_URI = self.db_uri

    def tearDown(self):
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    def test_collect_metrics(self):
        """Test collecting system metrics."""
        collect_metrics.collect_metrics()
        db = lancedb.connect(self.db_uri)
        metrics_tbl = db.open_table("metrics")
        metrics = metrics_tbl.to_pandas().to_dict('records')
        self.assertEqual(len(metrics), 1)
        self.assertIn('cpu_percent', metrics[0])
        self.assertIn('memory_percent', metrics[0])

if __name__ == '__main__':
    unittest.main()
