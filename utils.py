
import subprocess
import json
from typing import Dict, Any, Optional

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
