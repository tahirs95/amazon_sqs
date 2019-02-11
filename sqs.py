import boto3
import json
queue_url = 'ENTER YOUR QUEUE URL'
queue_name = 'ENTER YOUR QUEUE Name'

################# SEND
sender = boto3.client('sqs', aws_access_key_id='',aws_secret_access_key='',region_name='')
receiver = boto3.resource('sqs', aws_access_key_id='', aws_secret_access_key='', region_name='')

response = sender.send_message(
    QueueUrl=queue_url,
    MessageBody= json.dumps({"course_id": "5fb6ba42b99f4e8787cb7d0490ae0cb6 ",
"action": "update"
,"storeId": 2})
)
print(response['MessageId'])

################# LENGTH OF MESSAGES

available_messages = sender.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=['ApproximateNumberOfMessages']
)
available_messages_count = available_messages['Attributes']['ApproximateNumberOfMessages']
print("Available messages in the queue:"+str(available_messages_count))

################# RECIEVE

queue = receiver.get_queue_by_name(QueueName=queue_name)
total_processed = 0
while True:
    messages = queue.receive_messages(MaxNumberOfMessages=10)
    if messages:
        print("Items picked from the queue: " + str(len(messages)))
        print('')
        for message in messages:
            print("Message Body is:"+str(json.loads(message.body)))
            total_processed += 1
            message.delete()
            print("Message is deleted successfully.")
    else:
        print("No more messages in the queue.")
        break

print("Total processed messages: " + str(total_processed))
