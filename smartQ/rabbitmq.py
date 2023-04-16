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


# not yet
def get_device_name(email):
    exchange_name = email
    queues = []
    print('hi')
    try:
        for queue in channel.get_bindings(exchange=exchange_name):
            queues.append(queue['queue'])
    except:
        print('false')
        return False
            
    print(queues)
    return queues


class Result_Saver():
    def __init__(self):
        self.queue_name = 'MongoDB'
        channel.queue_declare(self.queue_name)
        channel.queue_bind(exchange='output', queue=self.queue_name, routing_key='toMongoDB')


    def callback(self, ch, method, properties, body):
        message = pickle.loads(body, encoding='bytes')
        database.insert_result(message)
        print('[MongoDB] Result Saved')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        

    def consume(self):
        channel.basic_consume(on_message_callback=self.callback, queue=self.queue_name)
        print('[MongoDB] Start Consuming')
        channel.start_consuming()