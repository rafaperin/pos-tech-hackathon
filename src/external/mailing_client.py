import boto3
from botocore.config import Config

my_config = Config(
    region_name='us-east-1'
)

sns_client = boto3.client('sns', config=my_config)


class MailingClient:
    @staticmethod
    def send(message: str):
        sns_client.publish(
            TopicArn="arn:aws:sns:us-east-1:604623258149:hackathon-mailing",
            Message=message,
            Subject="Hackathon",
        )
