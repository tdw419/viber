
import lancedb
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from projects.llm_os_core.db import DB_URI
import pyarrow as pa

def init_resource_pool():
    """
    Initializes the resource_pool table.
    """
    db = lancedb.connect(DB_URI)
    try:
        resource_pool_schema = pa.schema([
            pa.field("resource_id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("type", pa.string()), # e.g., CPU, GPU, Memory
            pa.field("total", pa.float64()),
            pa.field("available", pa.float64()),
        ])
        db.create_table("resource_pool", schema=resource_pool_schema)
        print("Resource Pool table initialized.")
    except Exception:
        pass # Table already exists

def get_available_resources() -> list[dict]:
    """
    Returns a list of available resources.
    """
    db = lancedb.connect(DB_URI)
    resource_pool_tbl = db.open_table("resource_pool")
    return resource_pool_tbl.to_pandas().to_dict('records')

if __name__ == "__main__":
    init_resource_pool()
