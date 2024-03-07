import pika
from pika.frame import Method

def create_connection():
    # connect to rabbit broker pub sub style
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    # create exchange type fanout -> all messages to all avaliabie queues
    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    # create random queue for logs exchange
    result: Method = channel.queue_declare(queue='', exclusive=True)

    # bind queue to exchange
    channel.queue_bind(exchange='logs', queue=result.method.queue)

    return connection, channel


def publish_string(channel, message, queue_name: str = "hello"):
    channel.basic_publish(exchange='logs', # exchange parameter message goes through here, taki filtr tematów wiadomości, ''-> default exchange
                          routing_key='', # queue name
                          body=f'{message}')
    print(f" [x] Sent '{message}' to logs exchange")


def main():
    connection, channel = create_connection()

    while True:
        resp = input("Enter message [x] to finish: ").strip().lower()
        print('-' * 40)

        match resp:
            case 'x':
                break
            case _:
                # queue_name = input("Enter queue name ").strip().lower() or 'task_queue'
                # print('-' * 40)
                #
                # if queue_name not in ['hello', 'task_queue']:
                #     print("bad queue name. Message dissmised!")
                #     continue

                publish_string(channel, resp)

    connection.close()
    print()
    print("kthx, bye.")


if __name__ == '__main__':
    main()