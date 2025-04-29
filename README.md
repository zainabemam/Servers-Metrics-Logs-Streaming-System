# Servers Metrics & Logs Streaming System

## Project Overview

This project builds a real-time data streaming system for monitoring a cloud storage website hosted on 10 servers behind a load balancer.

Each server runs an agent that sends resource metrics to Kafka, and the load balancer sends access logs. These streams are processed and stored for further analysis.

The project components:
- **Multi-node Kafka cluster** with two topics:
  - `server-metrics`: server resource consumption metrics.
  - `loadbalancer-logs`: load balancer monitor logs.
- **Kafka consumers**:
  - Metrics consumer inserts data into a relational database.
  - Spark Structured Streaming application processes logs, computes statistics over moving windows, and stores the results into Hadoop HDFS.

---

## Requirements

- Create two Kafka topics.
- Write a consumer for server metrics.
- Write a Spark application for load balancer logs.

---

## How It Works

1. The Java program simulates agent data and sends it to Kafka topics.
2. The metrics consumer reads server metrics and writes them into a database.
3. The Spark streaming application reads load balancer logs, computes 5-minute window aggregates (success/fail counts of GET and POST requests), and writes the output to Hadoop HDFS in Parquet format.

---

## Technologies Used

- **Apache Kafka**
- **Apache Spark**
- **Apache Hadoop (HDFS)**
- **Python** (Kafka consumer & Spark application)
- **Java** (Agents simulator)
- **SQLite** (Database for metrics)

---

## Prerequisites

- Apache Kafka
- Apache Spark
- Apache Hadoop
- Python 3.x
- Java 8+
- Maven
- MySQL (or any relational DB)


## How to Run

1. Start Zookeeper and all Kafka brokers.
2. Start Hadoop HDFS (namenode + datanode).
3. Create Kafka topics (`server-metrics` and `loadbalancer-logs`).
4. Run the Java program to send simulated data.
5. Start the metrics consumer.
6. Start the Spark structured streaming application.


## Author

- [zainab emam]


