#!/usr/bin/env python
import time
import pika
from random import uniform

rabbit_host = 'host'
rabbit_user = 'monitoring_user'
rabbit_password = 'isis2503'
exchange = 'monitoring_measurements'
topic = 'ML.505.Temperature'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbit_host, credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
channel = connection.channel()

channel.exchange_declare(exchange=exchange, exchange_type='topic')

print('> Sending measurements. To exit press CTRL+C')

while True:
    value = round(uniform(10, 50), 1)
    payload = "{'value':%r,'unit':'C'}" % (value)
    channel.basic_publish(exchange=exchange,
                          routing_key=topic, body=payload)
    print("Monitored temperature: %r" % (value))
    time.sleep(5)

connection.close()
