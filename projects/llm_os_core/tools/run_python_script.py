
import sys
import lancedb
import pandas as pd
from projects.llm_os_core.db import DB_URI

def main():
    """
    This tool takes a file path from the code_files table and executes it.
    The file path is passed as a command-line argument.
    """
    if len(sys.argv) < 2:
        print("Usage: python run_python_script.py <file_id>")
        sys.exit(1)

    file_id = int(sys.argv[1])

    db = lancedb.connect(DB_URI)
    code_files_tbl = db.open_table("code_files")
    code_file = code_files_tbl.search(file_id).to_pandas().to_dict('records')[0]

    exec(code_file['content'])

if __name__ == "__main__":
    main()
