
import lancedb
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from projects.llm_os_core.db import DB_URI

def monitor_agents(db_conn: lancedb.LanceDBConnection):
    """
    Monitors the status of all agents.
    """
    agents_tbl = db_conn.open_table("agents")
    print(agents_tbl.to_pandas())

if __name__ == "__main__":
    db_conn = lancedb.connect(DB_URI)
    monitor_agents(db_conn)
