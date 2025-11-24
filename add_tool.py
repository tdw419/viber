
import lancedb
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from llm_os.db import DB_URI

def main():
    """Adds the run_python_script tool to the tools table."""
    db = lancedb.connect(DB_URI)
    tools_tbl = db.open_table("tools")

    # Clear existing tools to avoid duplicates in this test setup
    tools_tbl.delete("tool_id > 0")

    tools_tbl.add([{
        "tool_id": 1,
        "project_id": 1,
        "name": "run_python_script",
        "type": "python",
        "entrypoint_path": "llm_os/tools/run_python_script.py",
        "args_schema": '{"file_id": "int"}',
        "description": "Executes a Python script from the code_files table.",
        "capabilities_embedding": [0.0] * 768, # Placeholder
    }])
    print("Added run_python_script tool to the tools table.")

if __name__ == "__main__":
    main()
