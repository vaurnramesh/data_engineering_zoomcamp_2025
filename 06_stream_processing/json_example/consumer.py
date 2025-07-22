from typing import Dict, List
from json import loads
from kafka import KafkaConsumer

from rides_schema import Ride
from settings import BOOTSTRAP_SERVERS, KAFKA_TOPIC


def deserialize_key(key_bytes: bytes) -> int:
    return int(key_bytes.decode('utf-8')) if key_bytes else None


def deserialize_value(value_bytes: bytes) -> Ride:
    return loads(value_bytes.decode('utf-8'), object_hook=Ride.from_dict) if value_bytes else None

class JsonConsumer(KafkaConsumer):
    def __init__(self, props):
        super().__init__(**props)

    def consume_from_kafka(self, topics: List[str]):
        self.subscribe(topics)
        print('Consuming from Kafka started')    
        print('Available topics to consume: ', self.subscription())

        while True:
            try:
                message = self.poll(1.0)
                if not message:
                    continue
                for _, message_value in message.items():
                    for msg_val in message_value:
                        print(msg_val.key, msg_val.value)
            except KeyboardInterrupt:
                break

        self.close()
    

if __name__ == '__main__':
    config = {
        'bootstrap_servers': BOOTSTRAP_SERVERS,
        'auto_offset_reset': 'earliest',
        'enable_auto_commit': True,
        'key_deserializer': deserialize_key,
        'value_deserializer': deserialize_value,
        'group_id': 'consumer.group.id.json-example.1',
    }


    json_consumer = JsonConsumer(props=config)
    json_consumer.consume_from_kafka(topics=[KAFKA_TOPIC])        