from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

# Set your AWS region
aws_region = 'us-east-1'  # Update with your desired AWS region

# Create an STS client to assume the role
sts_client = boto3.Session(profile_name='personal').client('sts')

# Role ARN to assume
role_to_assume_arn = 'arn:aws:iam::127450734152:role/SRE'  # Update with the ARN of the role to assume
role_session_name = 'flask-app-session'

# Assume the role
response = sts_client.assume_role(
    RoleArn=role_to_assume_arn,
    RoleSessionName='flask-session'
)

# Extract temporary security credentials
credentials = response['Credentials']
aws_access_key_id = credentials['AccessKeyId']
aws_secret_access_key = credentials['SecretAccessKey']
aws_session_token = credentials['SessionToken']

# Create an SQS client with the temporary security credentials
sqs = boto3.client(
    'sqs',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=aws_region
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_message', methods=['POST'])
def send_message():
   # message = request.args.get('message')
    # Extract the message from the request
    message = request.args.get('message', 'No message provided')    
    
    print(message)
    if not message:
        return 'Please provide a valid message.', 400

    # Send a message to the SQS queue
    queue_url = 'https://sqs.us-east-1.amazonaws.com/127450734152/terraform-main-queue'  # Update with your existing queue URL
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)

    return f'Message sent to queue! Message ID: {response["MessageId"]}'


if __name__ == '__main__':
    app.run(debug=True)
