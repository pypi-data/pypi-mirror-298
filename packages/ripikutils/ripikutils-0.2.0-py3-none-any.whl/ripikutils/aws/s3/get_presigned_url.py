from . import get_s3_client

def get_presigned_url(bucket_name, object_key, expiration=3600):
    """Generate a presigned URL to share an S3 object."""
    s3 = get_s3_client()
    try:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': bucket_name, 'Key': object_key},
                                        ExpiresIn=expiration)
        return url
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None