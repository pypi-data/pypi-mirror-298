from . import get_s3_client

def delete_s3_object(bucket_name, object_key):
    """Delete an object from S3."""
    s3 = get_s3_client()
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"Deleted {object_key} from {bucket_name}")
    except Exception as e:
        print(f"Error deleting {object_key} from {bucket_name}: {e}")