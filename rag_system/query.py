from . import db
from . import embed
from . import config

def search_documents(query: str):
    """
    Searches for documents in the database that are relevant to the query.
    """
    query_embedding = embed.get_embedding(query)
    results = db.query_table(config.DB_URI, config.TABLE_NAME, query_embedding)
    return results