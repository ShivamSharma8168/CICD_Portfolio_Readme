import boto3
import os

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

instance_id = 'enter ec2 instance id' # Enter your instance id here 
sns_topic_arn = 'paste your arn'      # Paste your ARN generated in lambda function

def lambda_handler(event, context):
    try:
        # Notify before stopping EC2
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=f"Stopping instance {instance_id} to avoid extra charges.",
            Subject="EC2 Stop Warning. Free-tier Alert!"
        )

        # Stop the instance
        ec2.stop_instances(InstanceIds=[instance_id])

        return {
            'statusCode': 200,
            'body': f"Notification sent and instance {instance_id} stopped to avoid extra charges."
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error stopping instance {instance_id}: {str(e)}"
        }

