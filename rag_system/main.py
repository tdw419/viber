import argparse
import sys
from . import db
from . import embed
from . import query
from pydantic import BaseModel, Field
from typing import List
import pyarrow as pa

class DocSchema(BaseModel):
    text: str
    vector: List[float]

def main():
    """The main entry point for the RAG system CLI."""
    parser = argparse.ArgumentParser(description="A simple RAG system for your project.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a document to the database.")
    add_parser.add_argument("file", help="The path to the file to add.")

    # Query command
    query_parser = subparsers.add_parser("query", help="Query the database.")
    query_parser.add_argument("query", help="The query to search for.")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the database.")


    args = parser.parse_args()

    if args.command == "init":
        schema = pa.schema(
            [
                pa.field("vector", pa.list_(pa.float32(), 384)),
                pa.field("text", pa.string()),
            ]
        )
        db.create_table(query.DB_URI, query.TABLE_NAME, schema)
        print("Database initialized.")


    elif args.command == "add":
        try:
            with open(args.file, "r") as f:
                text = f.read()
            embedding = embed.get_embedding(text)
            db.add_documents(query.DB_URI, query.TABLE_NAME, [{"text": text, "vector": embedding}])
            print(f"Added document: {args.file}")
        except FileNotFoundError:
            print(f"Error: File not found at {args.file}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "query":
        results = query.search_documents(args.query)
        for result in results:
            print(result["text"])
            print("-" * 20)

if __name__ == "__main__":
    main()