
import os
import re
from typing import Dict, Any, Optional
import lm_studio_agent
import utils

def read_feature_files(feature_info: Dict[str, Any]) -> Dict[str, str]:
    """
    Reads the content of the spec and plan files.
    """
    files = {}
    spec_path = feature_info.get("FEATURE_SPEC")
    plan_path = feature_info.get("IMPL_PLAN")

    if spec_path and os.path.exists(spec_path):
        with open(spec_path, "r") as f:
            files["spec"] = f.read()
    
    if plan_path and os.path.exists(plan_path):
        with open(plan_path, "r") as f:
            files["plan"] = f.read()

    return files

def determine_next_task(plan_content: str) -> Optional[Dict[str, Any]]:
    """
    Determines the next incomplete main task and its sub-tasks from the plan.
    """
    print("Searching for the next incomplete task...")
    lines = plan_content.splitlines()
    
    for i, line in enumerate(lines):
        # Find the first line that is a main task and is not checked
        if re.search(r'^- \[ \]\s*', line) and not (line.startswith("  ") or line.startswith("\t")):
            task_match = re.search(r'^- \[ \]\s*(.*)', line)
            if task_match:
                task = task_match.group(1).strip()
                print(f"Found potential main task: {task}")

                # Now, collect its sub-tasks
                sub_tasks = []
                for j in range(i + 1, len(lines)):
                    sub_line = lines[j]
                    # Sub-tasks are indented and start with '- [ ]'
                    if sub_line.strip().startswith("- [ ]") and (sub_line.startswith("  ") or sub_line.startswith("\t")):
                        sub_task_match = re.search(r'^- \[ \]\s*(.*)', sub_line.strip())
                        if sub_task_match:
                            sub_tasks.append(sub_task_match.group(1).strip())
                    # If we hit another main task or a new phase, stop.
                    elif (sub_line.strip().startswith("- [ ]") and not (sub_line.startswith("  ") or sub_line.startswith("\t"))) or sub_line.strip().startswith("##"):
                        break
                
                return {"task": task, "sub_tasks": sub_tasks}

    print("No incomplete main tasks found.")
    return None

def execute_command_from_task(task: str):
    """
    Parses a shell command from a task description and executes it.
    """
    match = re.search(r'\(`([^`]+)`\)', task)
    if match:
        command = match.group(1)
        print(f"Executing command: {command}")
        run_command(command)
    else:
        print(f"No command found in task: {task}")

def execute_task(task: str, sub_tasks: list[str]):
    """
    This function is a placeholder. The user will manually implement each task.
    """
    print(f"The next task is: {task}")
    if sub_tasks:
        print("Sub-tasks:")
        for sub_task in sub_tasks:
            print(f"- {sub_task}")
    print("Please implement this task manually.")

def update_plan(plan_path: str, task: str, sub_tasks: list[str]):
    """
    Updates the plan to mark a task and its sub-tasks as complete.
    """
    with open(plan_path, "r") as f:
        plan_content = f.read()

    # Mark the main task as complete
    updated_plan = plan_content.replace(f"- [ ] {task}", f"- [x] {task}", 1)

    # Mark all sub-tasks as complete
    for sub_task in sub_tasks:
        updated_plan = updated_plan.replace(f"- [ ] {sub_task}", f"- [x] {sub_task}", 1)

    with open(plan_path, "w") as f:
        f.write(updated_plan)
    print(f"Updated plan: Marked '{task}' and its sub-tasks as complete.")

def main():
    """
    The main loop for the iteration agent.
    """
    print("Iteration Agent: Starting a new development iteration.")

    feature_info = utils.get_current_feature_info()
    if not feature_info:
        print("Could not determine the current feature. Aborting.")
        return

    files = read_feature_files(feature_info)
    plan_content = files.get("plan")

    if not plan_content:
        print("Could not read the plan file. Aborting.")
        return

    next_task_info = determine_next_task(plan_content)

    if not next_task_info:
        print("No incomplete tasks found in the plan. Nothing to do.")
        return

    next_task = next_task_info["task"]
    sub_tasks = next_task_info["sub_tasks"]

    print(f"Next task: {next_task}")
    if sub_tasks:
        print("Sub-tasks:")
        for sub_task in sub_tasks:
            print(f"- {sub_task}")

    execute_task(next_task, sub_tasks)
    # For now, since execute_task is a placeholder, we'll manually mark the task as complete.
    update_plan(feature_info["IMPL_PLAN"], next_task, sub_tasks)


if __name__ == "__main__":
    main()
