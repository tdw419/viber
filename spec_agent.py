
import os
import re
import lm_studio_agent
from typing import Dict, Any
import utils

def fill_spec_placeholder(spec_content: str, placeholder: str) -> str:
    """
    Fills a placeholder in the spec with LLM-generated content.
    """
    prompt = f"""Given the following specification content:
---
{spec_content}
---
Please provide the content for the section: '{placeholder}'.
Only output the content for that section, nothing else."""

    llm_response = lm_studio_agent.get_completion_from_lm_studio(prompt)
    return llm_response

def main():
    """
    The main loop for the spec agent.
    """
    print("Spec Agent: Starting to fill in the specification.")

    feature_info = utils.get_current_feature_info()
    if not feature_info:
        print("Could not determine the current feature. Aborting.")
        return

    spec_path = feature_info.get("FEATURE_SPEC")

    if not spec_path or not os.path.exists(spec_path):
        print(f"Spec file not found at {spec_path}. Aborting.")
        return

    with open(spec_path, "r") as f:
        spec_content = f.read()

    placeholders = re.findall(r'(\[NEEDS LLM INPUT\])', spec_content)

    for placeholder in placeholders:
        print(f"Filling placeholder: {placeholder}")
        llm_content = fill_spec_placeholder(spec_content, placeholder)
        spec_content = spec_content.replace(placeholder, llm_content, 1)

    with open(spec_path, "w") as f:
        f.write(spec_content)

    print("Specification filled.")

if __name__ == "__main__":

    main()
