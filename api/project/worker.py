#!/usr/bin/env python
import pika
import json
import config
import requests

credentials = pika.PlainCredentials(config.rabbit_user, config.rabbit_pass)

parameters = pika.ConnectionParameters(config.rabbit_host, 5672, "/", credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.queue_declare(queue='alquiler', durable=True)
print(" [*] Waiting for tasks to do. To exit press CTRL+C")

def rent_patin(msg):
    endpoint = "http://" + config.api_host + "/api/patines/rent"
    data = json.loads(msg)
    body = {
		"user": data["user"],
		"slot": data["slot"],
		"patin": data["patin"]
	}
    
    r = requests.post(url = endpoint, json = body)
    print(r.text)

def callback(ch, method, properties, body):

    print(" [x] Task received, we will rent the patin %r" % body)

    rent_patin(body)

    ch.basic_ack(delivery_tag=method.delivery_tag)

    print(" [x] Done")
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='alquiler')

channel.start_consuming()
