
import lancedb
import pandas as pd
import time
import subprocess
import os
import tempfile
from .db import DB_URI

def poll_pending_tasks(db):
    """Polls the tasks table for pending tasks."""
    tasks_tbl = db.open_table("tasks")
    all_tasks = tasks_tbl.to_pandas()
    pending_tasks = all_tasks[all_tasks["status"] == "PENDING"]
    return pending_tasks.to_dict('records')

def run_task(db, task):
    """Runs a single task."""
    print(f"Running task: {task['task_id']}")

    # Update task status to RUNNING
    tasks_tbl = db.open_table("tasks")
    tasks_tbl.update(where=f"task_id = {task['task_id']}", values={"status": "RUNNING"})

    # Get tool
    tools_tbl = db.open_table("tools")
    all_tools = tools_tbl.to_pandas()
    tool = all_tools[all_tools["tool_id"] == task['tool_id']].to_dict('records')[0]

    # Get code file from entrypoint_path
    code_files_tbl = db.open_table("code_files")
    all_code_files = code_files_tbl.to_pandas()
    # The entrypoint_path is the `path` in code_files
    code_file = all_code_files[all_code_files["path"] == tool['entrypoint_path']].to_dict('records')[0]


    # Create a temporary directory to run the code
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, os.path.basename(code_file['path']))
        with open(file_path, "w") as f:
            f.write(code_file['content'])

        # Execute the code
        try:
            result = subprocess.run(
                ["python", file_path],
                capture_output=True,
                text=True,
                check=True
            )
            stdout = result.stdout
            stderr = result.stderr
            exit_code = 0
            status = "DONE"
        except subprocess.CalledProcessError as e:
            stdout = e.stdout
            stderr = e.stderr
            exit_code = e.returncode
            status = "ERROR"

    # Store results
    task_results_tbl = db.open_table("task_results")
    task_results_tbl.add([{
        "task_id": task['task_id'],
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "artifacts_ref": "",
        "summary": "",
    }])

    # Update task status
    tasks_tbl.update(where=f"task_id = {task['task_id']}", values={"status": status})
    print(f"Task {task['task_id']} finished with status: {status}")

def main():
    """The main loop for the executor daemon."""
    print("Executor Daemon: Starting...")
    db = lancedb.connect(DB_URI)
    while True:
        pending_tasks = poll_pending_tasks(db)
        for task in pending_tasks:
            run_task(db, task)
        time.sleep(5)

if __name__ == "__main__":
    main()
