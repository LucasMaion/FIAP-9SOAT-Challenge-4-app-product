import boto3
from botocore.exceptions import BotoCoreError, ClientError

class SQSClient:
    def __init__(self, region_name: str):
        self.sqs = boto3.client('sqs', region_name=region_name)

    def send_message(self, queue_url: str, message_body: str, delay_seconds: int = 0) -> dict:
        try:
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body,
                DelaySeconds=delay_seconds
            )
            return response
        except (BotoCoreError, ClientError) as error:
            print(f"Error sending message: {error}")
            raise

    def receive_messages(self, queue_url: str, max_number: int = 1, wait_time: int = 0) -> list:
        try:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time
            )
            return response.get('Messages', [])
        except (BotoCoreError, ClientError) as error:
            print(f"Error receiving messages: {error}")
            raise

    def delete_message(self, queue_url: str, receipt_handle: str) -> None:
        try:
            self.sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
        except (BotoCoreError, ClientError) as error:
            print(f"Error deleting message: {error}")
            raise

    def get_queue_url(self, queue_name: str) -> str:
        try:
            response = self.sqs.get_queue_url(QueueName=queue_name)
            return response['QueueUrl']
        except (BotoCoreError, ClientError) as error:
            print(f"Error getting queue URL: {error}")
            raise