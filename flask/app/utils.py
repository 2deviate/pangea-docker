"""
Copyright: Copyright (C) 2022 2DEVIATE Inc. - All Rights Reserved
Product: Standard
Description: Utility helper functions
Notifyees: craig@2deviate.com
Category: None
"""
# third-party imports
import json
import boto3
import base64
import requests
from botocore.exceptions import ClientError


def get_secret(config):
    # Get Secret Name and Region from App Config
    secret_name = config["AWS_SECRET_NAME"]
    region_name = config["AWS_REGION_NAME"]

    if not (secret_name and region_name):
        raise KeyError("missing secret_name and or region_name keys")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    if secret:
        return json.loads(secret)


def response_json(success, data, message=None):
    """
    Helper method that converts the given data in json format
    :param success: status of the APIs either true or false
    :param data: data returned by the APIs
    :param message: user-friendly message
    :return: json response
    """
    data = {
        "response": data,
        "success": success,
        "message": message,
    }
    return data


def make_request(url):
    """
    Helper method that uses Python Requests library to make calls to
    external APIs
    :param url: url on which request can make
    :return: data returned by requests library in the json format
    """
    req = requests.get(url)
    return req.json()
