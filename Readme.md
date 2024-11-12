# Velib Station Monitoring

This project monitors real-time fluctuations of available bike stands at Vélib stations. It retrieves data using the JCDecaux API and processes it with Kafka to display station activity. This is an academic project.

## Prerequisites

1. Install [Kafka](https://kafka.apache.org/quickstart) and [ZooKeeper](https://zookeeper.apache.org/).
2. Obtain an API key from [JCDecaux Developer Portal](https://developer.jcdecaux.com/#/signup).

## Setup and Execution

```bash
# 1. Start ZooKeeper
./bin/zookeeper-server-start.sh ./config/zookeeper.properties

# 2. Start Kafka Server
./bin/kafka-server-start.sh ./config/server.properties

# 3. Create Kafka Topic
./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic velib-stations

# 4. Run Data Producer
# Use the JCDecaux API to retrieve station data.
python3 ./velib-get-stations.py

# 5. Monitor Station Data
# Run the script to visualize bike stand fluctuations.
python3 ./velib-monitor-stations.py
```
