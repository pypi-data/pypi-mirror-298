from pymongo import MongoClient

def update_document(mongo_client, database_name, collection_name, filter_query, update_data):
    """Update a document in a MongoDB collection."""
    collection = mongo_client.get_collection(database_name, collection_name)
    try:
        result = collection.update_one(filter_query, {'$set': update_data})
        print(f"Updated {result.modified_count} document(s) matching {filter_query}")
    except Exception as e:
        print(f"Error updating document: {e}")