

import pika, sys, os

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


def consume_callback(channel: BlockingChannel, method: Basic.Deliver, properties, body):
    print(f" [x] Received {method.routing_key} : {body.decode()}", flush=True)


def main():
    # connection to rabbint
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    # declare exchange and bind queue to it
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_keys]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    channel.basic_consume(queue=queue_name, on_message_callback=consume_callback, auto_ack=True)#, auto_ack=True) #auto confirm task is done

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Blocking functions
    channel.start_consuming()

    # stop consumer
    # channel.stop_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)