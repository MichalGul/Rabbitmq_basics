import pika, sys, os
import time

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic


def consume_callback(channel: BlockingChannel, method: Basic.Deliver, properties, body):
    print(f" [x] Received {body.decode()}")
    # simulate intense work
    time.sleep(body.count(b'.'))
    print(f" [x] Done: {body.decode().replace('.', '')}")
    print(f"[x] Sending acknowledgement to rabbit!")

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # connection to rabbint
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_consume(queue='hello', on_message_callback=consume_callback)#, auto_ack=True) #auto confirm task is done

    channel.queue_declare(queue="task_queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=consume_callback)#, auto_ack=True) #auto confirm task is done

    print(' [*] Waiting for messages. To exit press CTRL+C')
    # Blocking functions
    channel.start_consuming()

    # stop consumer
    #channel.stop_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)