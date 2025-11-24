
import lancedb
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from projects.llm_os_core.db import DB_URI

def main():
    """
    This agent reviews the results of the "hello world" script,
    proposes a change, and creates a new task.
    """
    db = lancedb.connect(DB_URI)
    task_results_tbl = db.open_table("task_results")
    code_files_tbl = db.open_table("code_files")
    tasks_tbl = db.open_table("tasks")

    # 1. Read the results of the "hello world" script
    task_results_tbl = db.open_table("task_results")
    all_results = task_results_tbl.to_pandas()
    results = all_results[all_results["task_id"] == 1].to_dict('records')
    if not results:
        print("No results found for task 1. Aborting.")
        return
    
    print(f"Results for task 1:\n{results[0]}")

    # 2. Propose a change
    new_script_content = 'print("Hello again from the LLM OS!")'
    
    # 3. Write the new version of the script
    code_files_tbl.add([
        {
            "file_id": 2,
            "project_id": 1,
            "path": "hello_world_v2.py",
            "content": new_script_content,
            "version": 2,
            "embedding": [0.0] * 768, # Placeholder
        },
    ])
    print("Added 'hello_world_v2.py' to the code_files table.")

    # 4. Create a new task to run the modified script
    tasks_tbl.add([
        {
            "task_id": 2,
            "project_id": 1,
            "status": "PENDING",
            "created_by_agent_id": 2, # This agent
            "tool_id": 1, # run_python_script
            "args": '{"file_id": 2}',
            "priority": 1,
        },
    ])
    print("Added task to run 'hello_world_v2.py'.")

if __name__ == "__main__":
    main()
