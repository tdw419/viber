import lancedb
import pandas as pd
from typing import List, Dict, Any
import pyarrow as pa

def create_table(db_uri: str, table_name: str, schema: Any):
    """Creates a new LanceDB table."""
    db = lancedb.connect(db_uri)
    try:
        tbl = db.create_table(table_name, schema=schema)
        return tbl
    except Exception as e:
        print(f"Error creating table: {e}")
        return None

def add_documents(db_uri: str, table_name: str, documents: List[Dict[str, Any]]):
    """Adds a list of documents to the table."""
    db = lancedb.connect(db_uri)
    try:
        tbl = db.open_table(table_name)
    except Exception:
        schema = pa.schema(
            [
                pa.field("vector", pa.list_(pa.float32(), 768)),
                pa.field("text", pa.string()),
                pa.field("id", pa.int64()),
            ]
        )
        tbl = db.create_table(table_name, schema=schema)
    tbl.add(pd.DataFrame(documents))

def query_table(db_uri: str, table_name: str, query_embedding: List[float], limit: int = 5):
    """Performs a vector search on the table."""
    db = lancedb.connect(db_uri)
    tbl = db.open_table(table_name)
    result_df = tbl.search(query_embedding).limit(limit).to_pandas()
    # Convert numpy arrays in 'vector' column to lists of standard floats
    if 'vector' in result_df.columns:
        result_df['vector'] = result_df['vector'].apply(lambda x: [float(i) for i in x])
    return result_df.to_dict('records')