
import unittest
import os
import shutil
import lancedb
import pyarrow as pa
import datetime
from . import create_agent
from . import assign_tasks
from . import scale_agents
from . import resource_pool
from . import collect_metrics

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.db_uri = "./.test_lancedb"
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)
        
        # Initialize all necessary tables
        db_conn = lancedb.connect(self.db_uri)
        
        # Agents table
        agents_schema = pa.schema([
            pa.field("agent_id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("role", pa.string()),
            pa.field("prompt_profile", pa.string()),
            pa.field("code_ref", pa.string()),
        ])
        db_conn.create_table("agents", schema=agents_schema)

        # Tasks table
        tasks_schema = pa.schema([
            pa.field("task_id", pa.int64()),
            pa.field("project_id", pa.int64()),
            pa.field("status", pa.string()),
            pa.field("created_by_agent_id", pa.int64()),
            pa.field("tool_id", pa.int64()),
            pa.field("args", pa.string()),
            pa.field("priority", pa.int64()),
        ])
        db_conn.create_table("tasks", schema=tasks_schema)

        # Metrics table
        metrics_schema = pa.schema([
            pa.field("timestamp", pa.timestamp('ns')),
            pa.field("cpu_percent", pa.float64()),
            pa.field("memory_percent", pa.float64()),
        ])
        db_conn.create_table("metrics", schema=metrics_schema)

        # Resource Pool table
        resource_pool_schema = pa.schema([
            pa.field("resource_id", pa.int64()),
            pa.field("name", pa.string()),
            pa.field("type", pa.string()), # e.g., CPU, GPU, Memory
            pa.field("total", pa.float64()),
            pa.field("available", pa.float64()),
        ])
        db_conn.create_table("resource_pool", schema=resource_pool_schema)
        
        # Add two agents for testing
        create_agent.create_agent(db_conn, "Agent 1", "Worker", "Profile 1")
        create_agent.create_agent(db_conn, "Agent 2", "Worker", "Profile 2")
        
        # Set DB_URI for all modules
        create_agent.DB_URI = self.db_uri
        assign_tasks.DB_URI = self.db_uri
        scale_agents.DB_URI = self.db_uri
        resource_pool.DB_URI = self.db_uri
        collect_metrics.DB_URI = self.db_uri

    def tearDown(self):
        if os.path.exists(self.db_uri):
            shutil.rmtree(self.db_uri)

    def test_end_to_end_workflow(self):
        """Test a simplified end-to-end workflow of agent creation, task assignment, and metric collection."""
        db_conn = lancedb.connect(self.db_uri)

        # 1. Add agents directly in setUp

        # 2. Create a task
        tasks_tbl = db_conn.open_table("tasks")
        tasks_tbl.add([{"task_id": 1, "project_id": 1, "status": "PENDING", "created_by_agent_id": 0, "tool_id": 0, "args": "", "priority": 0}])
        print("Task 1 created.")

        # 3. Assign task
        assign_tasks.assign_task(db_conn, 1, 1) # Assign task 1 to agent 1
        updated_task = tasks_tbl.to_pandas()
        updated_task = updated_task[updated_task["task_id"] == 1].to_dict('records')[0]
        self.assertEqual(updated_task['status'], "ASSIGNED")
        self.assertEqual(updated_task['created_by_agent_id'], 1)
        print("Task 1 assigned to Agent 1.")

        # 4. Collect metrics (simulate executor working)
        collect_metrics.collect_metrics()
        metrics_tbl = db_conn.open_table("metrics")
        self.assertGreater(len(metrics_tbl.to_pandas()), 0)
        print("Metrics collected.")

if __name__ == '__main__':
    unittest.main()
