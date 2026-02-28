# Домашнее задание к занятию «Очереди RabbitMQ» — Пак Владислав

---

## Задание 1. Установка RabbitMQ

RabbitMQ 3.12.14 установлен через Docker с management plugin.

**Docker Compose** запускает контейнер с образом `rabbitmq:3.12-management`, который уже включает management plugin.

```bash
docker compose up -d
```

Management UI доступен на порту 15672 (http://localhost:15672).

**Скриншот веб-интерфейса RabbitMQ:**

![RabbitMQ Overview](img/task1_rabbitmq_overview.png)

---

## Задание 2. Отправка и получение сообщений

### Отправка сообщений (producer.py)

```bash
python3 producer.py
```

![Producer](img/task2_producer.png)

### Очередь hello в веб-интерфейсе (3 сообщения Ready)

![Queue hello](img/task2_queue_hello.png)

### Получение сообщений (consumer.py)

```bash
python3 consumer.py
```

![Consumer](img/task2_consumer.png)

---

## Задание 3. Подготовка HA кластера

### Настройка кластера

Две ноды RabbitMQ запущены через Docker Compose (`rmq01` и `rmq02`) в одной Docker-сети.

Объединение в кластер:

```bash
docker exec rmq02 rabbitmqctl stop_app
docker exec rmq02 rabbitmqctl reset
docker exec rmq02 rabbitmqctl join_cluster rabbit@rmq01
docker exec rmq02 rabbitmqctl start_app
```

Создание политики ha-all:

```bash
docker exec rmq01 rabbitmqctl set_policy ha-all ".*" '{"ha-mode":"all"}'
```

### Скриншот: доступные ноды в кластере

![Cluster nodes](img/task3_cluster_nodes.png)

### Скриншот: политика ha-all

![HA policy](img/task3_ha_policy.png)

### Вывод `rabbitmqctl cluster_status`

**Нода rmq01:**

```
Cluster status of node rabbit@rmq01 ...
Basics

Cluster name: rabbit@rmq01

Disk Nodes

rabbit@rmq01
rabbit@rmq02

Running Nodes

rabbit@rmq01
rabbit@rmq02

Versions

rabbit@rmq01: RabbitMQ 3.12.14 on Erlang 25.3.2.15
rabbit@rmq02: RabbitMQ 3.12.14 on Erlang 25.3.2.15
```

**Нода rmq02:**

```
Cluster status of node rabbit@rmq02 ...
Basics

Cluster name: rabbit@rmq02

Disk Nodes

rabbit@rmq01
rabbit@rmq02

Running Nodes

rabbit@rmq01
rabbit@rmq02

Versions

rabbit@rmq01: RabbitMQ 3.12.14 on Erlang 25.3.2.15
rabbit@rmq02: RabbitMQ 3.12.14 on Erlang 25.3.2.15
```

### Скриншот: `rabbitmqadmin get queue='hello'` на обеих нодах

![rabbitmqadmin both nodes](img/task3_rabbitmqadmin_both.png)

### Тест HA failover

Остановлена нода rmq01 (к которой подключался producer), запущен consumer_rmq02.py на второй ноде:

```bash
docker stop rmq01
python3 consumer_rmq02.py
```

**Скриншот: consumer получает сообщения с rmq02 после отключения rmq01:**

![Consumer rmq02 failover](img/task3_consumer_rmq02_failover.png)

Все сообщения успешно получены через вторую ноду — HA кластер работает корректно.

---

## Файлы проекта

| Файл | Описание |
|------|----------|
| `docker-compose.yml` | Docker Compose для 2 нод RabbitMQ с management |
| `producer.py` | Скрипт отправки сообщений в очередь hello |
| `consumer.py` | Скрипт получения сообщений (rmq01, порт 5672) |
| `consumer_rmq02.py` | Скрипт получения сообщений (rmq02, порт 5673) |
