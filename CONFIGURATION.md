# Kafka Cluster and Topics Configuration

This document details the configuration of each Kafka broker and the topics used in the project.

---

## Kafka Brokers Configuration

We are running a **multi-node Kafka cluster** with three brokers.

| Broker ID | Port  | Log Directory      | Configuration File      |
|:---------:|:-----:|:------------------:|:-----------------------:|
| 1         | 9092  | /tmp/kafka-logs     | config/server-1.properties |
| 2         | 9093  | /tmp/kafka-logs-1   | config/server-2.properties |
| 3         | 9094  | /tmp/kafka-logs-2   | config/server-3.properties |

### Broker 1 Configuration (`server-1.properties`)

```properties
broker.id=1
listeners=PLAINTEXT://localhost:9092
log.dirs=/tmp/kafka-logs
zookeeper.connect=localhost:2181

### Broker 2 Configuration (`server-2.properties`)

```properties
broker.id=2
listeners=PLAINTEXT://localhost:9093
log.dirs=/tmp/kafka-logs-1
zookeeper.connect=localhost:2181

### Broker 3 Configuration (`server-3.properties`)

```properties
broker.id=3
listeners=PLAINTEXT://localhost:9094
log.dirs=/tmp/kafka-logs-2
zookeeper.connect=localhost:2181

# kafka topics

| Topic Name          | Partitions | Replication Factor | Purpose                          |
|:--------------------|:----------:|:------------------:|:--------------------------------:|
| server-metrics       | 3          | 3                  | Server resource metrics          |
| loadbalancer-logs    | 3          | 3                  | Load balancer monitor logs   |


