from . import get_s3_client

def list_s3_objects(bucket_name, prefix=None):
    """List objects in an S3 bucket."""
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        objects = [obj['Key'] for obj in response.get('Contents', [])]
        return objects
    except Exception as e:
        print(f"Error listing objects in {bucket_name}: {e}")
        return []