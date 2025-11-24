
import argparse
import sys
import os
import lancedb
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from projects.llm_os_core.db import DB_URI
from . import create_agent
from . import monitor_agents
from . import scale_agents
from . import assign_tasks

def main():
    """
    A simple command-line interface for managing agents and tasks.
    """
    parser = argparse.ArgumentParser(description="LLM OS CLI for managing agents and tasks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Agent creation command
    create_agent_parser = subparsers.add_parser("create_agent", help="Create a new agent.")
    create_agent_parser.add_argument("name", help="The name of the agent.")
    create_agent_parser.add_argument("role", help="The role of the agent.")
    create_agent_parser.add_argument("prompt", help="The prompt profile for the agent.")

    # Monitor agents command
    monitor_agents_parser = subparsers.add_parser("monitor_agents", help="Monitor the status of agents.")

    # Scale agents command
    scale_agents_parser = subparsers.add_parser("scale_agents", help="Scale the number of agents.")
    scale_agents_parser.add_argument("count", type=int, help="The desired number of agents.")

    # Assign task command
    assign_task_parser = subparsers.add_parser("assign_task", help="Assign a task to an agent.")
    assign_task_parser.add_argument("task_id", type=int, help="The ID of the task.")
    assign_task_parser.add_argument("agent_id", type=int, help="The ID of the agent.")

    args = parser.parse_args()

    db_conn = lancedb.connect(DB_URI)

    if args.command == "create_agent":
        create_agent.create_agent(db_conn, args.name, args.role, args.prompt)
    elif args.command == "monitor_agents":
        monitor_agents.monitor_agents(db_conn)
    elif args.command == "scale_agents":
        scale_agents.scale_agents(db_conn, args.count)
    elif args.command == "assign_task":
        assign_tasks.assign_task(db_conn, args.task_id, args.agent_id)

if __name__ == "__main__":
    main()
