import os
import re

def slugify(text: str) -> str:
    """
    Converts a string to a slug.
    """
    text = text.lower()
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^a-z0-9-]', '', text)
    return text

def get_next_project_id() -> int:
    """
    Gets the next project ID by looking at the existing project directories.
    """
    if not os.path.exists("projects"):
        return 1
    
    project_dirs = [d for d in os.listdir("projects") if os.path.isdir(os.path.join("projects", d))]
    if not project_dirs:
        return 1
    
    max_id = 0
    for dir_name in project_dirs:
        match = re.match(r'(\d+)-', dir_name)
        if match:
            max_id = max(max_id, int(match.group(1)))
            
    return max_id + 1

def create_project(project_name: str):
    """
    Creates a new project.
    """
    project_slug = slugify(project_name)
    project_id = get_next_project_id()
    project_dir = f"projects/{project_id:03d}-{project_slug}"

    os.makedirs(os.path.join(project_dir, "checklists"))
    
    with open(os.path.join(project_dir, "spec.md"), "w") as f:
        f.write(f"# Feature Specification: {project_name}\n")

    with open(os.path.join(project_dir, "plan.md"), "w") as f:
        f.write(f"# Implementation Plan: {project_name}\n")
        
    print(f"Created new project at {project_dir}")
