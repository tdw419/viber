import os
import re
from typing import Dict, Any, Optional
import lm_studio_agent
import utils
import subprocess
import json

def run_command(command: str) -> Optional[str]:
    """Runs a command and returns the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        return None

def get_current_feature_info() -> Optional[Dict[str, Any]]:
    """
    Gets the current feature information by running the setup-plan.sh script.
    """
    script_path = ".specify/scripts/bash/setup-plan.sh"
    command = f"bash {script_path} --json"
    output = run_command(command)
    if output:
        try:
            # The script might output more than just the JSON, so we find the JSON object
            json_output = output[output.find('{'):]
            return json.loads(json_output)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON output from setup-plan.sh: {e}")
            print(f"Script output:\n{output}")
            return None
    return None

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
    This version is more robust to different markdown list styles and indentation,
    and ensures only one main task (with its sub-tasks) is returned at a time.
    """
    print("Searching for the next incomplete task...")
    lines = plan_content.splitlines()
    
    current_main_task = None
    current_sub_tasks = []
    main_task_indent = -1

    for i, line in enumerate(lines):
        stripped_line = line.lstrip()
        indent = len(line) - len(stripped_line)

        # Check for main task pattern: '- [ ] Task Name'
        main_task_match = re.match(r'^[-*]\s*\[ \]\s*(.+)', stripped_line)
        
        if main_task_match:
            # If we've found a main task and it's not indented, or it's a sibling to a previous main task
            if current_main_task is None or indent <= main_task_indent:
                if current_main_task is not None: # If we have a previous main task, return it now
                    return {"task": current_main_task, "sub_tasks": current_sub_tasks}
                
                current_main_task = main_task_match.group(1).strip()
                main_task_indent = indent
                current_sub_tasks = []
                print(f"Found potential main task: {current_main_task} (indent: {indent})")
            elif current_main_task is not None and indent > main_task_indent: # This is a sub-task
                current_sub_tasks.append(main_task_match.group(1).strip())
        elif current_main_task is not None and (not stripped_line or stripped_line.startswith("##")):
            # If we were collecting sub-tasks and hit an empty line or a new phase header, return the current task info
            return {"task": current_main_task, "sub_tasks": current_sub_tasks}

    # After the loop, return any remaining collected task info
    if current_main_task is not None:
        return {"task": current_main_task, "sub_tasks": current_sub_tasks}

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
    Executes a given task by asking the LLM for either shell commands or Python code, 
    and then executing/writing it.
    """
    print(f"Executing task: {task}")

    # Determine if it's a shell command task or a Python file modification task
    shell_command_match = re.search(r'\((`[^`]+`)\)', task)
    python_file_match = re.search(r'`([^`]+\.py)`', task)

    if shell_command_match:
        # It's a shell command task
        command = shell_command_match.group(1).strip('`')
        print(f"Executing shell command:\n---\n{command}\n---")
        utils.run_command(command)
        for sub_task in sub_tasks:
            sub_shell_command_match = re.search(r'\((`[^`]+`)\)', sub_task)
            if sub_shell_command_match:
                sub_command = sub_shell_command_match.group(1).strip('`')
                print(f"Executing sub-task shell command:\n---\n{sub_command}\n---")
                utils.run_command(sub_command)
            else:
                print(f"No shell command found in sub-task: {sub_task}")

    elif python_file_match:
        # It's a Python file modification task
        file_path = python_file_match.group(1)
        print(f"Target file for Python code: {file_path}")

        current_content = ""
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                current_content = f.read()

        prompt = f"Given the task: '{task}'"
        if sub_tasks:
            prompt += "\nWith the following sub-tasks:\n"
            for sub_task in sub_tasks:
                prompt += f"- {sub_task}\n"
        
        if current_content:
            prompt += f"\nHere is the current content of the file `{file_path}`:\n```python\n{current_content}\n```"

        prompt += f"\nPlease provide the complete and final code for the file `{file_path}`. Only output the code in a single Python markdown block. Do not include any other text or explanation."

        llm_response = lm_studio_agent.get_completion_from_lm_studio(prompt)

        if llm_response:
            print(f"LLM Response:\n{llm_response}")
            code_match = re.search(r'```python\n(.*?)\n```', llm_response, re.DOTALL)
            if code_match:
                code = code_match.group(1)
                print(f"Writing code to {file_path}")
                with open(file_path, "w") as f:
                    f.write(code)
            else:
                print("LLM did not provide a valid python code block.")
        else:
            print("LLM did not provide a response. Skipping task execution.")
    else:
        # It's a descriptive task, no direct command to execute
        print(f"No executable command or file modification detected for task: {task}")

    print("Task execution complete.")

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

def get_next_roadmap_idea() -> Optional[str]:
    """
    Gets the next incomplete idea from the roadmap.
    """
    if not os.path.exists("roadmap.md"):
        return None
    
    with open("roadmap.md", "r") as f:
        for line in f:
            if line.strip().startswith("- [ ]"):
                return line.strip().replace("- [ ]", "").strip()
    return None

def main():
    """
    The main loop for the iteration agent.
    """
    print("Iteration Agent: Starting a new development iteration.")

    # For now, we'll hardcode the current project ID for testing purposes.
    # In a real system, this would be determined dynamically.
    current_project_id = "001-import-existing-codebases-into"

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
        print("No incomplete tasks found in the plan. Checking the roadmap for new ideas.")
        next_idea = get_next_roadmap_idea()
        if next_idea:
            print(f"Found new idea in the roadmap: {next_idea}")
            print("Creating a new feature specification for this idea.")
            with open("temp_command.sh", "w") as f:
                f.write(f'venv/bin/python general_agent.py <<< "spec new {next_idea}"')
            utils.run_command("bash temp_command.sh")
            os.remove("temp_command.sh")
            # Mark the idea as in progress
            with open("roadmap.md", "r") as f:
                roadmap_content = f.read()
            updated_roadmap = roadmap_content.replace(f"- [ ] {next_idea}", f"- [x] {next_idea} (In Progress)", 1)
            with open("roadmap.md", "w") as f:
                f.write(updated_roadmap)
        else:
            print("No new ideas found in the roadmap. Nothing to do.")
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