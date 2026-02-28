#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RabbitMQ Producer — отправка сообщений в очередь hello."""

import pika

# Подключение к RabbitMQ (rmq01)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)
channel = connection.channel()

# Объявляем очередь hello
channel.queue_declare(queue='hello')

# Отправляем сообщение
message = 'Hello Netology!'
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=message
)

print(f" [x] Sent '{message}'")

connection.close()
