
import lancedb
import pyarrow as pa
from typing import List
import pandas as pd

DB_URI = "./.lancedb_os"

def init_db():
    """Initializes the LLM OS database and creates the core tables."""
    db = lancedb.connect(DB_URI)

    # Projects table
    try:
        projects_schema = pa.schema([
            pa.field("project_id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("description", pa.string()),
            pa.field("status", pa.string()),
        ])
        db.create_table("projects", schema=projects_schema)
    except Exception:
        pass # Table already exists

    # Code Files table
    try:
        code_files_schema = pa.schema([
            pa.field("file_id", pa.int64()),
            pa.field("project_id", pa.int64()),
            pa.field("path", pa.string()),
            pa.field("content", pa.string()),
            pa.field("version", pa.int64()),
            pa.field("embedding", pa.list_(pa.float32(), 768)),
        ])
        db.create_table("code_files", schema=code_files_schema)
    except Exception:
        pass # Table already exists

    # Tools table
    try:
        tools_schema = pa.schema([
            pa.field("tool_id", pa.int64()),
            pa.field("project_id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("type", pa.string()),
            pa.field("entrypoint_path", pa.string()),
            pa.field("args_schema", pa.string()),
            pa.field("description", pa.string()),
            pa.field("capabilities_embedding", pa.list_(pa.float32(), 768)),
        ])
        db.create_table("tools", schema=tools_schema)
    except Exception:
        pass # Table already exists

    # Tasks table
    try:
        tasks_schema = pa.schema([
            pa.field("task_id", pa.int64()),
            pa.field("project_id", pa.int64()),
            pa.field("status", pa.string()),
            pa.field("created_by_agent_id", pa.int64()),
            pa.field("tool_id", pa.int64()),
            pa.field("args", pa.string()),
            pa.field("priority", pa.int64()),
        ])
        db.create_table("tasks", schema=tasks_schema)
    except Exception:
        pass # Table already exists

    # Task Results table
    try:
        task_results_schema = pa.schema([
            pa.field("task_id", pa.int64()),
            pa.field("stdout", pa.string()),
            pa.field("stderr", pa.string()),
            pa.field("exit_code", pa.int64()),
            pa.field("artifacts_ref", pa.string()),
            pa.field("summary", pa.string()),
        ])
        db.create_table("task_results", schema=task_results_schema)
    except Exception:
        pass # Table already exists

    # Agents table
    try:
        agents_schema = pa.schema([
            pa.field("agent_id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("role", pa.string()),
            pa.field("prompt_profile", pa.string()),
            pa.field("code_ref", pa.string()),
        ])
        db.create_table("agents", schema=agents_schema)
    except Exception:
        pass # Table already exists

def search_table(db_uri: str, table_name: str, query: str) -> pd.DataFrame:
    """Performs a vector search on a table."""
    db = lancedb.connect(db_uri)
    tbl = db.open_table(table_name)
    return tbl.search(query).to_pandas()

def get_table_contents(db_uri: str, table_name: str) -> pd.DataFrame:
    """Returns the contents of a table as a pandas DataFrame."""
    db = lancedb.connect(db_uri)
    tbl = db.open_table(table_name)
    return tbl.to_pandas()

def get_tables(db_uri: str) -> List[str]:
    """Returns a list of all table names in the database."""
    db = lancedb.connect(db_uri)
    return db.table_names()

if __name__ == "__main__":
    init_db()
    print("LLM OS Database Initialized.")
