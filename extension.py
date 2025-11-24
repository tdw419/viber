
import subprocess
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'projects/003-llm-os-gui')))
import pandas as pd
import pyarrow as pa
import general_agent
import lm_studio_agent
from projects.llm_os_core import db
from projects.llm_os_core import config

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
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def mcp_server(port="5000"):
    """
    Placeholder for a server-starting function if needed,
    but the main server is now in server.py.
    """
    print(f"Starting MCP server on port {port}...")
    print("Please run 'gunicorn server:app' to start the server.")

def rag_init_db():
    """
    Initializes the LanceDB database.
    """
    schema = pa.schema(
        [
            pa.field("vector", pa.list_(pa.float32(), 768)),
            pa.field("text", pa.string()),
            pa.field("id", pa.int64()),
        ]
    )
    db.create_table(config.DB_URI, config.TABLE_NAME, schema)
    print(f"Database created at {config.DB_URI}")

def rag_add(file_path):
    """
    Adds a document to the RAG database.
    """
    with open(file_path, "r") as f:
        text = f.read()
    vector = lm_studio_agent.get_embedding_from_lm_studio(text)
    db.add_documents(config.DB_URI, config.TABLE_NAME, [{"vector": vector, "text": text, "id": 0}])
    print(f"Added document to the database.")

def rag_search(query):
    """
    Searches the RAG database.
    """
    vector = lm_studio_agent.get_embedding_from_lm_studio(query)
    results = db.query_table(config.DB_URI, config.TABLE_NAME, vector)
    return results


def start_agent():
    """
    Starts the AI agent.
    """
    print("Starting the AI agent...")
    run_command("venv/bin/python agent.py")


def start_general_agent():
    """
    Starts the general AI agent.
    """
    print("Starting the general AI agent...")
    run_command("venv/bin/python general_agent.py")

def mcp_spec_new(description):
    """
    Creates a new feature specification using spec-kit programmatically.
    """
    general_agent.create_new_feature_programmatic(description)

def mcp_find_gemini_cli():
    """
    Triggers the general agent to find the gemini-cli executable.
    """
    general_agent.find_gemini_cli_executable()

def rag_init_conversations_db():
    """
    Initializes the LanceDB conversations database.
    """
    db_path = "lancedb"
    db = lancedb.connect(db_path)
    schema = [
        {"conversation_id": "", "timestamp": "", "role": "", "content": ""}
    ]
    try:
        tbl = db.create_table("gemini_conversations", schema=schema)
        print(f"Conversations database created at {db_path}")
    except Exception as e:
        print(f"Error creating conversations database: {e}")




def main():
    """
    The main function of the extension.
    """
    mcp_server()


