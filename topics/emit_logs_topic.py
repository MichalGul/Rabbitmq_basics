import pika
from pika.frame import Method
import sys

def create_connection():
    # connect to rabbit broker pub sub style
    credentials = pika.PlainCredentials('user', 'user')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    # create exchange type topic -> send message to by topic routing key a.b.c
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    return connection, channel


def publish_string(channel, message, routing_key_topic: str = "info"):
    channel.basic_publish(exchange='topic_logs', # exchange parameter message goes through here, taki filtr tematów wiadomości, ''-> default exchange
                          routing_key=routing_key_topic, # Also can be topic
                          body=f'{message}')
    print(f" [x] Sent '{routing_key_topic} : {message}' to logs topic")


def main():
    connection, channel = create_connection()

    while True:
        resp = input("Enter message [x] to send: ").strip().lower()
        print('-' * 40)

        routing_key = input("Enter routing key: ").strip().lower()
        print('-' * 40)
        if not routing_key:
            routing_key = "anonymous.info"

        match resp:
            case 'x':
                break
            case _:
                publish_string(channel, resp, routing_key)

    connection.close()
    print()
    print("kthx, bye.")


if __name__ == '__main__':
    main()