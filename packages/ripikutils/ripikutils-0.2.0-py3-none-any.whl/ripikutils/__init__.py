from .mongo import initialize_mongo
from .mongo import delete as delete_mongo
from .mongo import filter as filter_mongo
from .mongo import insert as insert_mongo
from .mongo import update as update_mongo
from .mongo import check as check
from .aws.s3 import upload as upload_s3
from .aws.s3 import download as download_s3
from .aws.s3 import delete as delete_s3
from .aws.s3 import get_presigned_url as get_presigned_url_s3
from .aws.s3 import list as list_s3
from .aws.s3 import list as list_s3

__all__ = [
    'aws',
    'mongo',
    'secrets'
]

__version__ = "0.2.0"

# AWS submodule
class aws:
    upload_s3_object = upload_s3.upload_s3_object
    download_s3_object = download_s3.download_s3_object
    delete_s3_object = delete_s3.delete_s3_object
    get_presigned_url = get_presigned_url_s3.get_presigned_url
    list_s3_objects = list_s3.list_s3_objects

# Mongo submodule
class mongo:
    initialize = initialize_mongo
    delete = delete_mongo.delete_document
    filter = filter_mongo.apply_filter
    insert = insert_mongo.insert_document
    update = update_mongo.update_document
    check = check.hello_world