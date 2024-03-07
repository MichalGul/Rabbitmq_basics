import pika




def create_connection():
    # connect to rabbit broker
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    # create queue to send message to and recieve from
    channel.queue_declare(queue="hello")

    return connection, channel


def publish_string(channel, message):
    channel.basic_publish(exchange='', # exchange parameter message goes through here, taki filtr tematów wiadomości
                          routing_key='hello', # queue name
                          body=f'{message}')
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
                publish_string(channel, resp)

    connection.close()
    print()
    print("kthx, bye.")


if __name__ == '__main__':
    main()