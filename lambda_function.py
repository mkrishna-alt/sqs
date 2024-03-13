import json
import boto3

def lambda_handler(event, context):
    # Set your AWS region
    aws_region = 'us-east-1'  # Update with your desired AWS region

    # Create SQS and DynamoDB clients
    sqs = boto3.client('sqs', region_name=aws_region)
    dynamodb = boto3.resource('dynamodb', region_name=aws_region)
    
    # Specify your DynamoDB table name
    dynamodb_table_name = 'datatable'  # Update with your DynamoDB table name
    
    # Create DynamoDB table resource
    table = dynamodb.Table(dynamodb_table_name)
     
     
    print(event)
    # Process messages from the SQS event
    for record in event['Records']:
        try:
            # Extract the message body from the 'Body' key

            print(record['body'])
            print(record['messageId'])
            # Write the message to DynamoDB using 'MessageId' as the primary key
            table.put_item(Item={
                'id': record['messageId'],  # Assuming 'MessageId' is a unique identifier
                'Content': record['body']  # Assuming 'Content' is another attribute in the message
            })
            
            # Delete the message from SQS
            receipt_handle = record['receiptHandle']
            region, account_id, queue_name = record['eventSourceARN'].split(':')[-3:]
            sqs = boto3.client('sqs', region_name=region)
            sqs_queue_url = f'https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}'
            sqs.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=receipt_handle)
        except Exception as e:
            print(f"Error processing message: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Messages processed successfully.')
    }
