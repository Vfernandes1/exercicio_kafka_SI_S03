from confluent_kafka import Producer
import socket
from kafka import KafkaProducer


conf = {'bootstrap.servers': 'localhost:9092'}

producer = Producer(conf)

# producer = KafkaProducer(bootstrap_servers='localhost:9092')

topic_name = 'exercicio-vini'

for i in range(10):
    message = f'I have a dream! {i}'
    # producer.send(topic_name, message.encode('utf-8'))
    producer.produce('exercicio-vini', value=message)
    producer.flush()
print('Mensagens enviadas com sucesso!')