
import os
import subprocess
import re
import json
import datetime

GEMINI_CLI_PATH = None # Global variable to store the path to gemini-cli

def run_command(command):
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

def list_files():
    """Lists the files in the current directory."""
    print("Project files:")
    for f in sorted(os.listdir(".")):
        print(f"- {f}")

def run_tests():
    """A placeholder for running tests."""
    print("General Agent: No tests defined yet.")

def show_status():
    """Shows the project status."""
    print("General Agent: Project status:")
    list_files()

def find_gemini_cli_executable():
    """
    Searches for the gemini-cli executable using various methods.
    Stores the found path in the global GEMINI_CLI_PATH variable.
    """
    global GEMINI_CLI_PATH

    print("Searching for gemini-cli executable...")

    # 1. Try 'command -v gemini'
    path_from_command_v = run_command("command -v gemini")
    if path_from_command_v and "not found" not in path_from_command_v.lower():
        if os.path.isfile(path_from_command_v) and os.access(path_from_command_v, os.X_OK):
            GEMINI_CLI_PATH = path_from_command_v
            print(f"Found gemini-cli using 'command -v': {GEMINI_CLI_PATH}")
            return GEMINI_CLI_PATH

    # 2. Try 'which gemini'
    path_from_which = run_command("which gemini")
    if path_from_which and "not found" not in path_from_which.lower():
        if os.path.isfile(path_from_which) and os.access(path_from_which, os.X_OK):
            GEMINI_CLI_PATH = path_from_which
            print(f"Found gemini-cli using 'which': {GEMINI_CLI_PATH}")
            return GEMINI_CLI_PATH

    # 3. Try 'whereis gemini' (less precise, might return multiple paths)
    path_from_whereis = run_command("whereis gemini")
    if path_from_whereis and "gemini:" in path_from_whereis:
        # whereis returns "gemini: /path1 /path2"
        potential_paths = path_from_whereis.split(":")[1].strip().split(" ")
        for p in potential_paths:
            if p and os.path.isfile(p) and os.access(p, os.X_OK):
                GEMINI_CLI_PATH = p
                print(f"Found gemini-cli using 'whereis': {GEMINI_CLI_PATH}")
                return GEMINI_CLI_PATH

    # Fallback to searching PATH (from previous implementation)
    path_env = os.environ.get("PATH", "").split(os.pathsep)
    for path in path_env:
        cli_path = os.path.join(path, "gemini-cli")
        if os.path.isfile(cli_path) and os.access(cli_path, os.X_OK):
            GEMINI_CLI_PATH = cli_path
            print(f"Found gemini-cli in PATH: {GEMINI_CLI_PATH}")
            return GEMINI_CLI_PATH
            
    print("gemini-cli executable not found using standard shell commands or system PATH.")
    print("Please ensure gemini-cli is installed and in your system's PATH, or provide its full path manually.")
    GEMINI_CLI_PATH = None
    return None

def handle_spec_command(spec_command):
    """
    Handles the spec commands.
    """
    parts = spec_command.split(" ", 1)
    command = parts[0].lower()

    if command == "new":
        if len(parts) > 1:
            _create_new_feature_interactive(parts[1])
        else:
            print("General Agent: Please provide a feature description.")
    else:
        print("General Agent: Unknown spec command. Available commands: new <description>")


def create_new_feature_programmatic(description):
    """
    Creates a new feature using spec-kit programmatically.
    """
    print(f"Creating a new feature with description: {description}")

    # 1. Feature Name and Short Name
    feature_name = description.capitalize()
    short_name = "-".join(re.findall(r'\b\w+\b', description.lower())[:4])
    print(f"Generated short name: {short_name}")

    # 2. Check for existing branches and determine the next feature number
    run_command("git fetch --all --prune")

    highest_number = 0

    # Remote branches
    remote_branches_raw = run_command(f"git ls-remote --heads origin '*/[0-9]*-{short_name}' || true")
    if remote_branches_raw:
        for line in remote_branches_raw.split('\n'):
            match = re.search(r'refs/heads/(\d+)-', line)
            if match:
                highest_number = max(highest_number, int(match.group(1)))

    # Local branches
    local_branches_raw = run_command(f"git branch | grep -E '^[* ]*[0-9]+-{short_name}$' || true")
    if local_branches_raw:
        for line in local_branches_raw.split('\n'):
            match = re.search(r'(\d+)-', line)
            if match:
                highest_number = max(highest_number, int(match.group(1)))

    # Specs directories
    spec_dirs_raw = run_command(f"ls -d specs/[0-9]*-{short_name} 2>/dev/null")
    if spec_dirs_raw:
        for line in spec_dirs_raw.split('\n'):
            match = re.search(r'specs/(\d+)-', line)
            if match:
                highest_number = max(highest_number, int(match.group(1)))

    next_feature_number = highest_number + 1
    print(f"Next feature number: {next_feature_number}")

    # d. Run the script `.specify/scripts/bash/create-new-feature.sh`
    script_path = ".specify/scripts/bash/create-new-feature.sh"
    command = f"{script_path} --json --number {next_feature_number} --short-name '{short_name}' '{description}'"
    script_output = run_command(command)

    if not script_output:
        print("Error running create-new-feature.sh")
        return

    try:
        feature_data = json.loads(script_output)
        branch_name = feature_data.get("BRANCH_NAME")
        spec_file = feature_data.get("SPEC_FILE")
        print(f"Branch name: {branch_name}")
        print(f"Spec file: {spec_file}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output from create-new-feature.sh: {e}")
        print(f"Script output:\n{script_output}")
        return

    # 3. Load .specify/templates/spec-template.md
    with open(".specify/templates/spec-template.md", "r") as f:
        spec_template = f.read()

    spec_content = generate_spec_content(description, spec_template)

    # 5. Write the specification to the SPEC_FILE
    with open(spec_file, "w") as f:
        f.write(spec_content)

    print(f"Successfully created new feature specification at {spec_file}")

    # 6. Perform specification quality validation
    # a. Create Spec Quality Checklist
    feature_dir = os.path.dirname(spec_file)
    checklists_dir = os.path.join(feature_dir, "checklists")
    os.makedirs(checklists_dir, exist_ok=True)

    requirements_checklist_content = f"""
# Specification Quality Checklist: {feature_name}

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Feature**: [Link to spec.md]

## Content Quality

- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

## Requirement Completeness

- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Success criteria are technology-agnostic (no implementation details)
- [ ] All acceptance scenarios are defined
- [ ] Edge cases are identified
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

## Feature Readiness

- [ ] All functional requirements have clear acceptance criteria
- [ ] User scenarios cover primary flows
- [ ] Feature meets measurable outcomes defined in Success Criteria
- [ ] No implementation details leak into specification

## Notes

- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
"""
    requirements_checklist_path = os.path.join(checklists_dir, "requirements.md")
    with open(requirements_checklist_path, "w") as f:
        f.write(requirements_checklist_content)

    print(f"Created quality checklist at {requirements_checklist_path}")


def _create_new_feature_interactive(description):
    """
    Creates a new feature using spec-kit (interactive version).
    """
    create_new_feature_programmatic(description)


def generate_spec_content(description, spec_template):
    """
    Generates the content for the specification document based on the description.
    """
    # 1. Feature Name
    feature_name = description.capitalize()

    # 2. User Story (generic)
    user_story = f"As a developer, I want to {description.lower()} to improve the quality of the project."

    # For this more advanced agent, we will let the LLM fill in the details.
    # We will mark the sections that need to be filled with [NEEDS LLM INPUT]
    functional_requirements = "[NEEDS LLM INPUT]"
    success_criteria = "[NEEDS LLM INPUT]"
    key_entities = "[NEEDS LLM INPUT]"
    assumptions = "[NEEDS LLM INPUT]"
    clarifications = "[NEEDS LLM INPUT]"

    # Fill the template
    filled_spec = spec_template.replace("{{feature_description}}", description)
    filled_spec = filled_spec.replace("## Feature Name", f"## Feature Name\n\n{feature_name}")
    filled_spec = filled_spec.replace("## User Story", f"## User Story\n\n{user_story}")
    filled_spec = filled_spec.replace("## Functional Requirements", f"## Functional Requirements\n{functional_requirements}")
    filled_spec = filled_spec.replace("## Success Criteria", f"## Success Criteria\n{success_criteria}")
    filled_spec = filled_spec.replace("## Key Entities", f"## Key Entities\n{key_entities}")
    filled_spec = filled_spec.replace("## Assumptions", f"## Assumptions\n{assumptions}")
    filled_spec = filled_spec.replace("## Clarifications", f"## Clarifications\n{clarifications}")

    return filled_spec


def main():
    """
    The main loop for the general AI agent.
    """
    print("General Agent: Hello! I'm ready to manage the project.")
    print("Available commands: list_files, run_tests, status, spec, find_gemini_cli, help, exit")

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            parts = user_input.split(" ", 1)
            command = parts[0].lower()

            if command == "exit":
                print("General Agent: Goodbye!")
                break
            elif command == "help":
                print("Available commands: list_files, run_tests, status, spec, find_gemini_cli, help, exit")
            elif command == "list_files":
                list_files()
            elif command == "run_tests":
                run_tests()
            elif command == "status":
                show_status()
            elif command == "find_gemini_cli":
                find_gemini_cli_executable()
            elif command == "spec":
                if len(parts) > 1:
                    handle_spec_command(parts[1])
                else:
                    print("General Agent: Please provide a spec command. Available commands: new <description>")
            else:
                print("General Agent: Unknown command. Type 'help' for a list of commands.")
        except (EOFError, KeyboardInterrupt):
            print("\nGeneral Agent: Goodbye!")
            break

if __name__ == "__main__":
    main()
