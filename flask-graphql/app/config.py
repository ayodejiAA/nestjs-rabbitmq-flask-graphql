import os
from lib.ClientRPC import ClientRPC

client = ClientRPC(
    url=os.getenv('RMQ_URL'),
    routing_key=os.getenv('SERVICE_QUEUE_NAME')
)
