import pika
import pickle

from smartQ import database

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
        body=pickle.dumps(message)
    )
    
    return True
    

# when user create -> user's exchange also create
def make_exchange(exchange_name):
    channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
    return True


class Result_Saver():
    def __init__(self):
        channel.queue_declare('MongoDB')
        channel.queue_bind(exchange='output', queue='MongoDB', routing_key='toMongoDB')


    def callback(self, ch, method, properties, body):
        message = pickle.loads(body, encoding='bytes')
        database.insert_result(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        

    def consume(self, queue_name):
        channel.basic_consume(on_message_callback=self.callback, queue=queue_name)
        print('[MongoDB] Start Consuming')
        channel.start_consuming()