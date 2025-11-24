# Implementation Plan: RAG System for Gemini CLI

## Phase 1: Core RAG System (Python)

- [x] **Task 1.1: Setup Project Structure**
    - [x] Create a new directory `rag_system` in the project root. (`mkdir -p rag_system`)
    - [x] Inside `rag_system`, create the following files: (`touch rag_system/__init__.py rag_system/db.py rag_system/embed.py rag_system/query.py rag_system/main.py`)

- [x] **Task 1.2: Implement Database Interaction (`db.py`)**
    - [x] Define a function `create_table(table_name, schema)` to create a new LanceDB table.
    - [x] Define a function `add_documents(table_name, documents)` to add a list of documents to the table.
    - [x] Define a function `query_table(table_name, query_embedding, limit=5)` to perform a vector search.

- [x] **Task 1.3: Implement Text Embedding (`embed.py`)**
    - [x] Use a pre-trained sentence transformer model (e.g., from Hugging Face) to generate embeddings.
    - [x] Define a function `get_embedding(text)` that takes a string and returns its vector embedding.

- [x] **Task 1.4: Implement Query Logic (`query.py`)**
    - [x] Define a function `search_documents(query)` that:
        1. Takes a natural language query as input.
        2. Generates an embedding for the query using `embed.get_embedding`.
        3. Queries the LanceDB table using `db.query_table`.
        4. Returns the retrieved documents.

- [x] **Task 1.5: Create CLI Interface (`main.py`)**
    - [x] Use `argparse` to create a simple command-line interface.
    - [x] Implement two subcommands:
        - [x] `add`: Takes a file path as input, reads the text, and adds it to the database.
        - [x] `query`: Takes a query string as input and prints the search results.

## Phase 2: Gemini CLI Extension Integration

- [x] **Task 2.1: Create a New Extension Command**
    - [x] In `extension.py`, add a new command `rag`.
    - [x] This command will have two subcommands: `add` and `query`.

- [x] **Task 2.2: Implement the `rag add` Command**
    - [x] The `rag add` command will take a file path as an argument.
    - [x] It will call the `rag_system.main.py add` command as a subprocess.
    - [x] It will print the output from the subprocess to the Gemini CLI.

- [x] **Task 2.3: Implement the `rag query` Command**
    - [x] The `rag query` command will take a query string as an argument.
    - [x] It will call the `rag_system.main.py query` command as a subprocess.
    - [x] It will print the output from the subprocess to the Gemini CLI.

## Phase 3: Testing and Refinement

- [x] **Task 3.1: Unit Tests for RAG System**
    - [x] Write unit tests for the functions in `db.py`, `embed.py`, and `query.py`.
    - [x] Use a small, sample dataset for testing.

- [x] **Task 3.2: Integration Tests for Extension**
    - [x] Write integration tests for the `rag` extension command.
    - [x] Test both the `add` and `query` subcommands.

- [x] **Task 3.3: Performance and Accuracy Testing**
    - [x] Test the system with a larger dataset.
    - [x] Measure the response time for queries.
    - [x] Evaluate the accuracy of the search results.
    - [x] Refine the embedding model and query logic as needed.