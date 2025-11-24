import sys

def assign_task(task_id: int, agent_id: int):
    """
    Assigns a task to an agent (simplified).
    """
    print(f"[Simplified] Assigning task {task_id} to agent {agent_id}")

if __name__ == "__main__":
    # Simple CLI for assigning a task
    if len(sys.argv) < 3:
        print("Usage: python assign_tasks.py <task_id> <agent_id>")
        sys.exit(1)
    
    assign_task(int(sys.argv[1]), int(sys.argv[2]))