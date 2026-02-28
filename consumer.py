#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RabbitMQ Consumer — получение сообщений из очереди hello."""

import pika

# Подключение к RabbitMQ (rmq01)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

# Объявляем очередь hello (на случай если consumer запущен первым)
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")


# Подписываемся на очередь
channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=True
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
