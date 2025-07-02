# 📘 Introduction to Stream Processing

## What is Stream Processing?

We will explore what stream processing means and how it differs from traditional data exchange methods.

### Real-World Analogy: Postal Service

Think of a traditional postal service. You write a message (data) on a letter and send it via the postal system. Eventually, it reaches the intended receiver. This is a simple form of **batch data exchange**—it's not immediate, and there's a delay.

### In Software: APIs

In modern software systems, data is exchanged through technologies like:

- REST APIs  
- GraphQL  
- Webhooks  

These enable one system (producer) to send information to another (consumer).

### Analogy: The Public Notice Board

A **notice board** is a helpful metaphor to understand data flow:

- A **producer** posts flyers (data) on the board.
- **Consumers** walk by and read these flyers, if they’re interested.

You can extend this analogy:

- Consumers might only be interested in certain **topics** (e.g., `Kafka`, `Spark`, `Big Data`).
- Producers post flyers under these topics.
- Consumers subscribed to those topics receive only relevant information.

This mimics a **pub-sub model** (publish-subscribe), common in streaming systems like **Kafka**.

![sp1](images/sp1.jpeg)

---

## What is Stream Processing?

Now that we understand data exchange, let’s talk about **stream processing** specifically.

### Batch vs Stream

| Batch Processing              | Stream Processing               |
|------------------------------|----------------------------------|
| Data is collected and sent in chunks (e.g., hourly, daily) | Data is sent and received in near real-time |
| Example: Email notifications | Example: Kafka topics, Spark streaming |
| Often delayed                | Much faster and continuous       |

In **stream processing**, the goal is to move from periodic/batch data to **continuous** data flow.

### What is Real-Time, Really?

> Real-time does NOT mean "instantaneous".

Instead, real-time generally means a few seconds of delay, as opposed to hours or days. This latency is small enough to support applications like:

- Fraud detection  
- Real-time analytics  
- Monitoring systems


## Kafka

Kafka has various terms like producer, consumer and topics. Let us look into each one of them in the following sections 

### 1. What is a Topic?

A **topic** is essentially a *named stream of events*.  
You can think of it as a category or feed to which records (events) are published.

- Every topic represents a continuous flow of data.
- Producers write events to a topic.
- Consumers read events from a topic.
- Topics are partitioned internally, allowing Kafka to scale horizontally and handle very large volumes of data.

In simple terms, if your application generates data over time, that data flows into a topic.

---

### 2. What is an Event?

An **event** (sometimes called a **record** or **message**) is the individual piece of data that gets written to a topic.

Let’s look at a concrete example:

Imagine you’re building an application that records the temperature in a room every 30 seconds.

- **Each event** answers the question:  
  *What was the temperature in the room at a specific point in time?*
- For instance:  
  *32°C recorded at 2:00 PM.*
- Thirty seconds later, a new reading is taken, creating another event.
- Over time, these events form a time-ordered sequence of measurements.

These individual data points—each with a value and a timestamp—are collected into the topic.

Once events are published, they stay in the topic for a configurable retention period (by default, 7 days), during which consumers can read and process them independently.

---

#### Additional Insights

- **Producers**: Applications or services that create and send events to Kafka topics.
- **Consumers**: Applications or services that subscribe to topics to read and process events.
- **Partitions**: Each topic is split into partitions to distribute load and provide parallelism.
- **Offsets**: Every event in a partition has a unique offset, which acts as its position in the log. Consumers track offsets to know what they’ve already processed.

Kafka is designed to **decouple producers and consumers**, so producers don’t need to know who will consume their data, and consumers can read the data at their own pace.


### 3. Event Structure

At a minimum, an event contains:

- **Key** (optional): Used to determine the partition within the topic.
- **Value**: The actual data payload of the event.
- **Timestamp**: The time when the event was produced or logged.
- **Metadata**: Additional information such as headers or the offset in the partition.

Let’s break down each part:

#### Key

The key is optional.
- When present, Kafka uses it to decide which partition an event should go to.
- Common use cases:
  - Grouping related events (e.g., all events for the same user or order).
  - Ensuring ordering guarantees within a partition.

**Example:**  
If you have a topic recording temperature readings by sensor ID, the sensor ID could be the key.

---

#### Value

- The value holds the main content of the event.
- It can be anything: a string, JSON, Avro, Protobuf, or any binary data.
- Most of the time, this is what consumers are interested in processing.

**Example Value:**  
```json
{
  "sensorId": "sensor-123",
  "temperature": 32,
  "unit": "C",
  "recordedAt": "2025-06-26T14:00:00Z"
}
```

#### Timestamp

- Every event has a timestamp assigned when it is produced
- This timestamp can be set by the producer or by the Kafka broker when the event is received
- Timestamps help consumers understand when the event occurred

#### Putting it all together

| Field         | Example Value             |
| ------------- | ------------------------- |
| **Key**       | `sensor-123`              |
| **Value**     | `{ "temperature": 32 }`   |
| **Timestamp** | `2025-06-26T14:00:00Z`    |
| **Headers**   | `{"trace-id": "abc-123"}` |
| **Offset**    | `42`                      |


### 4. Reliability

Kafka provides a unique combination of obustness, scalability, and flexibility that makes it stand out:

- **Robustness and Reliability**
  - Even if servers or nodes go down, you will still receive your data.
  - This is achieved through **replication**: Kafka automatically replicates data across multiple nodes so it remains durable and available.

- **Flexibility**
  - Topics can be small or huge—Kafka handles both gracefully.
  - You can have a single consumer or hundreds of consumers reading from the same topic independently.
  - With integrations like **Kafka Connect** (for connecting to databases and other systems) and **ksqlDB** (for stream processing using SQL), you get powerful tools to build end-to-end data pipelines.

- **Tiered Storage**
  - Kafka offers **tiered storage**, letting you keep all your event history cost-effectively.
  - You can replay or reprocess old data later for offline analytics or audits.

- **Scalability**
  - Kafka scales horizontally.
  - If your workload grows from 10 events per second to 1,000 or 100,000 events per second, Kafka can handle the increase seamlessly by adding more brokers and partitions.
 