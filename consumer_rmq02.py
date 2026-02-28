#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RabbitMQ Consumer — подключение к rmq02 (вторая нода кластера)."""

import pika

# Подключение к RabbitMQ rmq02 (порт 5673 маппится на 5672 контейнера)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5673)
)
channel = connection.channel()

# Объявляем очередь hello
channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(f" [x] Received from rmq02: '{body.decode()}'")


# Подписываемся на очередь
channel.basic_consume(
    queue='hello',
    on_message_callback=callback,
    auto_ack=True
)

print(' [*] Waiting for messages on rmq02. To exit press CTRL+C')
channel.start_consuming()
