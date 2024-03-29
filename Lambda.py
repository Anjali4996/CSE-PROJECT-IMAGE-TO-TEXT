import json
import base64
import boto3
import string
import random

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    textract = boto3.client("textract")

    # Retrieve base64 encoded image data from the request body
    get_file_content = event["body-json"]

    # Decode the base64 content
    decoded_content = base64.b64decode(get_file_content)

    # Generate a unique filename for the image
    pic_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".png"

    # Upload the image to S3
    s3.put_object(Bucket="textimage25", Key=pic_filename, Body=decoded_content)

    # Retrieve the image from S3
    s3_response = s3.get_object(Bucket="textimage25", Key=pic_filename)
    image_bytes = s3_response['Body'].read()

    # Detect text in the image using Amazon Textract
    textract_response = textract.detect_document_text(Document={'Bytes': image_bytes})

    # Extract the detected text
    extracted_text = '\n'.join(block['Text'] for block in textract_response['Blocks'] if block['BlockType'] == 'LINE')

    # Delete the file from S3
    s3.delete_object(Bucket="textimage25", Key=pic_filename)

    return {
        'statusCode': 200,
        'body': json.dumps(extracted_text)
    }
