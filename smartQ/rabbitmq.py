import pika
import pickle


RABBITMQ_SERVER_IP = '203.255.57.129'
RABBITMQ_SERVER_PORT = '5672'

credentials = pika.PlainCredentials('rabbitmq', '1q2w3e4r')
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_SERVER_IP, RABBITMQ_SERVER_PORT, 'vhost', credentials))

channel = connection.channel()

channel.exchange_declare(exchange='input', exchange_type='direct')
channel.exchange_declare(exchange='output', exchange_type='direct')


def publish(message, exchange_name, routing_key_name):
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key_name,
        body=pickle.dumps({'message': message})
    )
    
    return True

def make_exchange(exchange_name):
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    return True