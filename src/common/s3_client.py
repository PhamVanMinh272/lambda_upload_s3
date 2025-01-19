import json
import boto3

class S3Client:
    def __init__(self, bucket_name: str = None):
        self.region = 1
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def list_bucket_names(self):
        # Retrieve the list of existing buckets
        response = self.s3.list_buckets()
        bucket_names = []
        for bucket in response['Buckets']:
            bucket_names.append(bucket["Name"])
        return bucket_names

    def list_object_names(self):
        response = self.s3.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix='')
        file_names = []
        for content in response.get('Contents', []):
            file_names.append(content['Key'])
        return file_names

    def upload_file_obj(self, file_object, object_name):
        # Upload the file
        response = self.s3.upload_fileobj(file_object, self.bucket_name, object_name)

    def upload_file_from_data(self, data: dict, object_name: str):
        with open(object_name, "wb") as f:
            """
            Upload file required binary mode then we use 'rb'
            """
            json_data = json.dumps(data)
            f.write(json_data.encode("utf-8"))

        with open(object_name, "rb") as f:
            """
            Upload file required binary mode then we use 'rb'
            """
            self.upload_file_obj(f, object_name)

    def download_file_obj(self, object_name):
        print(f"Download file '{object_name}' ...")
        data = []
        with open(object_name, 'wb') as f:
            self.s3.download_fileobj(self.bucket_name, object_name, f)
            # data = f.read()
        return object_name

