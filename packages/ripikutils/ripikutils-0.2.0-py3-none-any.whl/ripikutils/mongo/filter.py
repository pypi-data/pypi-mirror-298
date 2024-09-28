from pymongo import MongoClient

def apply_filter(mongo_client, database_name, collection_name, filter_query):
    """Filter documents in a MongoDB collection."""
    collection = mongo_client.get_collection(database_name, collection_name)
    try:
        results = collection.find(filter_query)
        return list(results)
    except Exception as e:
        print(f"Error applying filter: {e}")
        return []