import threading
import time
import boto3
from botocore.exceptions import BotoCoreError, ClientError


class UserSync:
    def __init__(self, queue_url, db_handler, interval=10):
        """
        Initializes the SQSQueueMonitor.

        :param queue_url: The URL of the SQS FIFO queue.
        :param db_handler: A callable that processes messages and inserts them into the database.
        :param interval: The interval (in seconds) to poll the queue.
        """
        self.queue_url = queue_url
        self.db_handler = db_handler
        self.interval = interval
        self.sqs_client = boto3.client("sqs")
        self.stop_event = threading.Event()

    def _process_messages(self):
        """
        Polls the SQS queue, retrieves messages, and processes them.
        """
        while not self.stop_event.is_set():
            try:
                response = self.sqs_client.receive_message(
                    QueueUrl=self.queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5
                )
                messages = response.get("Messages", [])
                for message in messages:
                    try:
                        self.db_handler(message["Body"])
                        self.sqs_client.delete_message(
                            QueueUrl=self.queue_url,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                    except Exception as e:
                        print(f"Error processing message: {e}")
            except (BotoCoreError, ClientError) as e:
                print(f"Error interacting with SQS: {e}")
            time.sleep(self.interval)

    def start(self):
        """
        Starts the daemon thread to monitor the SQS queue.
        """
        self.thread = threading.Thread(target=self._process_messages, daemon=True)
        self.thread.start()

    def stop(self):
        """
        Stops the daemon thread.
        """
        self.stop_event.set()
        self.thread.join()
