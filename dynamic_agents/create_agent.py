
import lancedb
import sys
import os
import pyarrow as pa
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from projects.llm_os_core.db import DB_URI

def create_agent(db_conn: lancedb.LanceDBConnection, agent_name: str, role: str, prompt_profile: str) -> dict:
    """
    Creates a new agent and returns it as a dictionary.
    """
    agents_tbl = db_conn.open_table("agents")
    
    # Get the next agent ID
    # Check if an agent with this name already exists
    existing_agents = agents_tbl.to_pandas()
    if not existing_agents.empty and agent_name in existing_agents['name'].values:
        print(f"Agent '{agent_name}' already exists. Skipping creation.")
        return existing_agents[existing_agents['name'] == agent_name].to_dict('records')[0]

    if not existing_agents.empty:
        max_id = existing_agents['agent_id'].max()
        next_id = max_id + 1
    else:
        next_id = 1

    agent = {
        "agent_id": next_id,
        "name": agent_name,
        "role": role,
        "prompt_profile": prompt_profile,
        "code_ref": "", # Placeholder
    }
    agents_tbl.add([agent])
    print(f"Created new agent: {agent_name}")
    return agent

if __name__ == "__main__":
    # Simple CLI for creating an agent
    if len(sys.argv) < 4:
        print("Usage: python create_agent.py <name> <role> <prompt_profile>")
        sys.exit(1)
    
    db_conn = lancedb.connect(DB_URI)
    create_agent(db_conn, sys.argv[1], sys.argv[2], sys.argv[3])
