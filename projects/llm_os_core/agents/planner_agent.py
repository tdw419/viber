
import lancedb
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from projects.llm_os_core.db import DB_URI

def main():
    """
    This agent creates a simple "hello world" script and a task to run it.
    """
    db = lancedb.connect(DB_URI)
    code_files_tbl = db.open_table("code_files")
    tasks_tbl = db.open_table("tasks")

    # 1. Create the "hello world" script
    hello_world_script = 'print("Hello from the LLM OS!")'
    code_files_tbl.add([{
        "file_id": 1,
        "project_id": 1,
        "path": "hello_world.py",
        "content": hello_world_script,
        "version": 1,
        "embedding": [0.0] * 768, # Placeholder
    }])
    print("Added 'hello_world.py' to the code_files table.")

    # 2. Create the task to run the script
    tasks_tbl.add([{
        "task_id": 1,
        "project_id": 1,
        "status": "PENDING",
        "created_by_agent_id": 1, # This agent
        "tool_id": 1, # run_python_script
        "args": '{"file_id": 1}',
        "priority": 1,
    }])
    print("Added task to run 'hello_world.py'.")

if __name__ == "__main__":
    main()
