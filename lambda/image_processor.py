import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')
sns = boto3.client('sns')

PROCESSED_BUCKET = "processedimagessiddu"
SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:<YOUR-ACCOUNT-ID>:ImageProcessingNotifications"

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            source_bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            # Get object from S3
            response = s3.get_object(Bucket=source_bucket, Key=key)
            image_data = response['Body'].read()

            # Load and resize image
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((800, 800))

            # Save processed image to buffer
            buffer = io.BytesIO()
            image.save(buffer, format=image.format, optimize=True, quality=70)
            buffer.seek(0)

            # Upload transformed image
            s3.put_object(
                Bucket=PROCESSED_BUCKET,
                Key=key,
                Body=buffer,
                ContentType=response["ContentType"]
            )

            # Send SNS notification
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Image Processed Successfully",
                Message=f"Image '{key}' has been processed and saved to {PROCESSED_BUCKET}."
            )

        return {"status": "success"}

    except Exception as e:
        print("Error:", str(e))
        return {"status": "error", "message": str(e)}
    
