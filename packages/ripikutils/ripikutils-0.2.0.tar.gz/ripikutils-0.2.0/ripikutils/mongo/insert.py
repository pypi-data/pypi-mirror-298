from pymongo import MongoClient

def insert_document(mongo_client, database_name, collection_name, document):
    """Insert a document into a MongoDB collection."""
    collection = mongo_client.get_collection(database_name, collection_name)
    try:
        result = collection.insert_one(document)
        print(f"Inserted document with _id: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting document: {e}")