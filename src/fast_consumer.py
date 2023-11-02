from confluent_kafka import Consumer
from kafka import KafkaConsumer

# conf = {'bootstrap.servers': '127.0.0.1:9092',
#         'group.id': 'foo',
#         'auto.offset.reset': 'smallest'}

# consumer = Consumer(conf)

topic_name = 'exercicio-vini'

# # consumer = KafkaConsumer(topic_name, bootstrap_servers='localhost:9092')

# for message in consumer:
#     print(f'Mensagem recebida: {message.value.decode("utf-8")}')

# consumer.subscribe([topic_name])

def logica_consumer():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'exercicio_ponderada',
        'auto.offset.reset': 'earliest',
    }

    consumer = Consumer(conf)
    consumer.subscribe([topic_name])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Mensagem não consumida: {msg.error()}")
            else:
                print(f"A mensagem foi recebida: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    logica_consumer()