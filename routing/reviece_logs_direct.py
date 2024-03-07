

import pika, sys, os

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


def consume_callback(channel: BlockingChannel, method: Basic.Deliver, properties, body):
    print(f" [x] Received {body.decode()}", flush=True)


def main():
    # connection to rabbint
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    # declare exchange and bind queue to it
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)

    for severity in severities:
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

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