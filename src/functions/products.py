import json
import logging
import botocore
from src.common.func_responses import make_success_response
from src.common.s3_client import S3Client
from src.setttings import S3_BUCKET
from src.common.enum import Routes, HTTPMethods


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Product:
    def __init__(self):
        self.file_name = "products.json"
        self.s3_client = S3Client(S3_BUCKET)

    def init_file(self):
        logger.info("Init file in S3 for Products ...")
        files_in_s3 = self.s3_client.list_object_names()
        if self.file_name not in files_in_s3:
            logger.info(f"{self.file_name} not found. Creating new file ...")
            init_data = {
                "table_name": "product",
                "data": {}
            }
            self.s3_client.upload_file_from_data(init_data, self.file_name)
        else:
            logger.info(f"{self.file_name} file already exist. Do nothings.")
        logger.info("Done")
        return "Done"


    def get_all(self) -> dict:
        """
        Get all products list

        """
        try:
            logger.info("Get list products ...")
            path = self.s3_client.download_file_obj(self.file_name)
            with open(path, "r") as f:
                data = f.read()
            data = json.loads(data)
            data = data["data"]
            return data
        except botocore.exceptions.ClientError as e:
            logger.warning("Not found files in S3. Automatically creating files ...")
            self.init_file()
            return {}


    def create(self):
        """
        We expect a file already exist.
        - Download the file to check data
        - Edit file
        - Upload file
        :return:
        """
        new_data = {
            "id": "1",
            "name": "products 2"
        }
        product_dict = self.get_all()
        if not product_dict.get(new_data["id"]):
            product_dict[new_data["id"]] = new_data
        else:
            raise Exception(f"id {new_data['id']} already exist")
        upload_data = {
                "table_name": "product",
                "data": product_dict
            }

        self.s3_client.upload_file_from_data(upload_data, self.file_name)

def lambda_handler(event, context):
    verb = event.get("method", "GET")
    resource = event.get("resource")
    logger.info(resource)

    product_service = Product()
    get_routes = {
        Routes.Products.REF_PRODUCTS: product_service.get_all
    }
    post_routes = {
        Routes.Products.REF_PRODUCTS: product_service.create,
    }

    verb_paths = {
        HTTPMethods.GET: get_routes,
        HTTPMethods.POST: post_routes
    }

    paths = verb_paths.get(verb)

    func = paths.get(resource)
    data = func()

    return make_success_response({"data": data})


if __name__ == "__main__":
    # event = {
    #     "resource": "/products/init",
    #     "method": "POST"
    # }
    event  = {
        "resource": Routes.Products.REF_PRODUCTS,
        "method": HTTPMethods.POST
    }
    rs = lambda_handler(event, None)
    body = json.loads(rs["body"])
    print(json.dumps(body, indent=4))
