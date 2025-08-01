
# Running PySpark Streaming 

#### Prerequisite

Ensure your Kafka and Spark services up and running by following the [docker setup readme](./../../docker/README.md). 
It is important to create network and volume as described in the document. Therefore please ensure, your volume and network are created correctly

```bash
docker volume ls # should list hadoop-distributed-file-system
docker network ls # should list kafka-spark-network 
```


### Running Producer and Consumer
```bash
# Run producer
python3 producer.py

# Run consumer with default settings
python3 consumer.py
# Run consumer for specific topic
python3 consumer.py --topic <topic-name>
```

### Running Streaming Script

spark-submit script ensures installation of necessary jars before running the streaming.py

```bash
./spark-submit.sh streaming.py 
```

### Additional Resources
- [Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#structured-streaming-programming-guide)
- [Structured Streaming + Kafka Integration](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#structured-streaming-kafka-integration-guide-kafka-broker-versio)


### Kafka Connect (Source + Sink) vs Kafka Producer / Consumer

Kafka connect is typically used to connect external sources to Kafka i.e. to produce/consume to/from external sources from/to Kafka.

Anything that you can do with connector can be done through Producer+Consumer
Readily available Connectors only ease connecting external sources to Kafka without requiring the developer to write the low-level code.

Some points to remember - 

1. If the source and sink are both the same Kafka cluster, Connector doesn't make sense
2. If you are doing changed-data-capture (CDC) from a database and push them to Kafka, you can use a Database source connector.
3. Resource constraints: Kafka connect is a separate process. So double check what you can trade-off between resources and ease of development.
4. If you are writing your own connector, it is well and good, unless someone has not already written it. If you are using third-party connectors, you need to check how well they are maintained and/or if support is available.