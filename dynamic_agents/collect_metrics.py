
import lancedb
import sys
import os
import pyarrow as pa
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from projects.llm_os_core.db import DB_URI
import psutil

def collect_metrics():
    """
    Collects system metrics and stores them in the database.
    """
    db = lancedb.connect(DB_URI)
    try:
        metrics_schema = pa.schema([
            pa.field("timestamp", pa.timestamp('ns')),
            pa.field("cpu_percent", pa.float64()),
            pa.field("memory_percent", pa.float64()),
        ])
        metrics_tbl = db.create_table("metrics", schema=metrics_schema)
    except Exception:
        metrics_tbl = db.open_table("metrics")

    metrics_tbl.add([{
        "timestamp": datetime.datetime.now(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
    }])
    print("Collected system metrics.")

if __name__ == "__main__":
    collect_metrics()
