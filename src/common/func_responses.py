import json

def make_success_response(body: dict, status_code: int = 200):
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }
