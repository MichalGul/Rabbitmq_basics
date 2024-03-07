import pika

def create_connection():
    # connect to rabbit broker
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    # create queue to send message to and recieve from, make queue durable -> prevents when rabbit restarts
    channel.queue_declare(queue="hello")

    # make new queue durable -> prevents messages in it when rabbit restarts
    channel.queue_declare(queue="task_queue", durable=True)

    return connection, channel


def publish_string(channel, message, queue_name:str = "hello"):
    channel.basic_publish(exchange='', # exchange parameter message goes through here, taki filtr tematów wiadomości
                          routing_key=queue_name, # queue name
                          body=f'{message}',
                          properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)) # mark messages as persistent
    print(f" [x] Sent '{message}'")


def main():
    connection, channel = create_connection()

    while True:
        resp = input("Enter message [x] to finish: ").strip().lower()
        print('-' * 40)

        match resp:
            case 'x':
                break
            case _:
                queue_name = input("Enter queue name ").strip().lower() or 'task_queue'
                print('-' * 40)

                if queue_name not in ['hello', 'task_queue']:
                    print("bad queue name. Message dissmised!")
                    continue

                publish_string(channel, resp, queue_name)

    connection.close()
    print()
    print("kthx, bye.")


if __name__ == '__main__':
    main()