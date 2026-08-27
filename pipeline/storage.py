import boto3
import logging 

def upload_to_s3(file, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(Bucket=bucket, Key=object_name, Body=file)
        logging.info(f"File {object_name} uploaded to bucket {bucket}")
    except Exception as e:
        logging.error(e)
        return False
