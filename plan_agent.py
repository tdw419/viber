
import os
import re
import lm_studio_agent
from typing import Dict, Any
import utils

def get_spec_content(spec_path: str) -> str:
    """Reads the content of the spec file."""
    if os.path.exists(spec_path):
        with open(spec_path, "r") as f:
            return f.read()
    return ""

def generate_plan(spec_content: str) -> str:
    """
    Generates an implementation plan based on the spec content.
    """
    prompt = f"""Given the following specification:
---
{spec_content}
---
Please create a detailed implementation plan. The plan should be a markdown file with a list of tasks and sub-tasks.
Each task and sub-task should be in the format '- [ ]'.
For tasks that involve creating files or running commands, include the command in backticks within parentheses, like this: '- [ ] Create a new file (`touch new_file.py`)'
The plan should be broken down into logical phases.
Only output the markdown for the plan, nothing else."""

    llm_response = lm_studio_agent.get_completion_from_lm_studio(prompt)
    return llm_response

def main():
    """
    The main loop for the plan agent.
    """
    print("Plan Agent: Starting to generate the implementation plan.")

    feature_info = utils.get_current_feature_info()
    if not feature_info:
        print("Could not determine the current feature. Aborting.")
        return

    spec_path = feature_info.get("FEATURE_SPEC")
    plan_path = feature_info.get("IMPL_PLAN")

    if not spec_path or not os.path.exists(spec_path):
        print(f"Spec file not found at {spec_path}. Aborting.")
        return

    spec_content = get_spec_content(spec_path)
    plan_content = generate_plan(spec_content)

    with open(plan_path, "w") as f:
        f.write(plan_content)

    print("Implementation plan generated.")

if __name__ == "__main__":
    main()
