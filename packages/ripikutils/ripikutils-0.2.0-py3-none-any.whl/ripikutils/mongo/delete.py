from . import get_mongo_client

def delete_document(database_name, collection_name, filter_query):
    """Delete a document from MongoDB collection."""
    try:
        client = get_mongo_client("default")
        db = client[database_name]
        collection = db[collection_name]
        result = collection.delete_one(filter_query)
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting document: {e}")
        return 0