# BDA PYQ 2024 – Complete Solutions
**Pandit Deendayal Energy University | End Sem Exam (May 2024)**
**Course: Big Data Analytics (B23CP309) | Max Marks: 100 | Time: 3 Hours**

---

## Q1-A: Answer Both [10 Marks]

### 1. Big Data 3Vs in Healthcare

In a healthcare scenario, all three dimensions of Big Data are present simultaneously:

| V | Healthcare Source | Example |
|---|---|---|
| **Volume** | EHR records, medical imaging (MRI/CT scans), genomics, wearable sensor logs | A single MRI = 100MB+; millions of patients = petabytes |
| **Velocity** | Real-time patient vitals (ICU monitors), ambulance GPS, emergency alerts | ECG streams at 500Hz, blood pressure every second |
| **Variety** | Structured (lab results), Semi-structured (HL7/FHIR messages), Unstructured (doctor notes, X-ray images, audio recordings) | No single schema fits all formats |

**Why Big Data Analytics is necessary:**
- Traditional RDBMS cannot store or query petabyte-scale patient records efficiently.
- Real-time ICU monitoring requires stream processing — batch SQL cannot respond fast enough.
- Genomic data (VCF files), imaging (DICOM), and clinical notes require different storage and processing engines.
- Predictive analytics (disease outbreak detection, readmission risk) requires ML on distributed datasets.

---

### 2. Hadoop Architecture

Hadoop is a distributed computing framework built on **HDFS** (storage) and **MapReduce** (processing), managed by **YARN** (resource allocation).

```
┌────────────────────────────────────────────────────────────────┐
│                       HADOOP CLUSTER                           │
│                                                                │
│  ┌─────────────────┐         ┌────────────────────────────┐   │
│  │   NameNode      │◄───────►│  Secondary NameNode        │   │
│  │   (HDFS Master) │         │  (Checkpointing FSImage)   │   │
│  │  - File→Block   │         └────────────────────────────┘   │
│  │    mapping      │                                          │
│  │  - Block        │         ┌────────────────────────────┐   │
│  │    locations    │         │   ResourceManager (YARN)   │   │
│  └────────┬────────┘         │   - Cluster resource mgmt  │   │
│           │ heartbeats       │   - Schedules MapReduce     │   │
│    ┌──────▼────────────────────────────────────────┐     │   │
│    │               DataNodes (Workers)             │     │   │
│    │  ┌─────────┐  ┌─────────┐  ┌─────────┐       │     │   │
│    │  │  DN-1   │  │  DN-2   │  │  DN-3   │       │     │   │
│    │  │ Blk-1   │  │ Blk-1   │  │ Blk-2   │       │     │   │
│    │  │ Blk-2   │  │ Blk-3   │  │ Blk-3   │       │     │   │
│    │  │NodeMgr  │  │NodeMgr  │  │NodeMgr  │       │     │   │
│    │  └─────────┘  └─────────┘  └─────────┘       │     │   │
│    └───────────────────────────────────────────────┘     │   │
└────────────────────────────────────────────────────────────────┘
```

**Key Components:**
| Component | Role |
|---|---|
| **NameNode** | Stores HDFS metadata (file→block mapping). Does NOT store actual data. |
| **DataNode** | Stores actual data blocks. Sends heartbeat every 3s. |
| **Secondary NameNode** | Periodically merges FSImage + EditLog. NOT a hot backup. |
| **ResourceManager** | YARN master — allocates cluster resources to applications. |
| **NodeManager** | YARN worker — manages containers on each DataNode. |

> **💡 Depth of Understanding:**
> Hadoop 1.x had a single JobTracker handling both resource management and job tracking — a bottleneck. Hadoop 2.x introduced **YARN** separating these concerns, allowing Spark, Tez, and other frameworks to run alongside MapReduce on the same cluster. Hadoop 3.x added **Erasure Coding** as an alternative to 3x replication — achieving the same fault tolerance with only ~1.5x storage overhead (vs 3x), crucial for cold storage at petabyte scale.

---

## Q1-B: Answer All [5 Marks Each]

### Q1-B.1: HDFS Fault Tolerance [5 Marks]

HDFS achieves fault tolerance through **replication**, **heartbeat monitoring**, and **automatic recovery**:

```
FILE: patient_data.csv (384 MB)
Block Size = 128 MB → 3 blocks created

Block Distribution (Replication Factor = 3):
┌─────────────────────────────────────────────────┐
│               Rack 1              │   Rack 2    │
│  ┌──────┐  ┌──────┐  ┌──────┐   │  ┌──────┐   │
│  │ DN-1 │  │ DN-2 │  │ DN-3 │   │  │ DN-4 │   │
│  │ B1✓  │  │ B1✓  │  │ B2✓  │   │  │ B1✓  │   │
│  │ B2✓  │  │ B3✓  │  │ B3✓  │   │  │ B2✓  │   │
│  └──────┘  └──────┘  └──────┘   │  └──────┘   │
└─────────────────────────────────────────────────┘

Rack Awareness: 1st replica (local), 2nd replica (diff rack), 3rd (same remote rack)
→ Survives complete rack failure
```

**Fault Detection & Recovery Steps:**
1. NameNode expects heartbeat from DataNode every **3 seconds**
2. After **10 missed heartbeats (~30s)**, DataNode marked as dead
3. NameNode checks which blocks are now under-replicated
4. Schedules re-replication of missing blocks on healthy nodes
5. Block report confirms restoration of replication factor

> **💡 Depth of Understanding:**
> HDFS HA (High Availability) mode uses **ZooKeeper** for leader election between Active and Standby NameNodes. The Standby continuously receives edit logs via a **JournalNode quorum** (typically 3 JournalNodes). On Active NameNode failure, ZooKeeper detects it and promotes Standby to Active in seconds — eliminating HDFS's historical single point of failure. This is now standard in production clusters.

---

### Q1-B.2: MapReduce Word Count – All Phases [5 Marks]

**Problem:** Count frequency of each word in a large text corpus stored in HDFS.

```
INPUT (HDFS Split → 2 Mappers):
  Mapper 1 input: "big data is big"
  Mapper 2 input: "data is fast data"
```

**Phase 1 — MAP:**
Each mapper tokenizes its input and emits `(word, 1)` for every token.
```
Mapper 1 output:          Mapper 2 output:
(big,  1)                 (data, 1)
(data, 1)                 (is,   1)
(is,   1)                 (fast, 1)
(big,  1)                 (data, 1)
```

**Phase 2 — COMBINER (Local Mini-Reducer):**
Runs on each mapper node locally. Aggregates same keys before network transfer — reduces shuffle cost.
```
Mapper 1 after combiner:  Mapper 2 after combiner:
(big,  2)                 (data, 2)
(data, 1)                 (is,   1)
(is,   1)                 (fast, 1)
```

**Phase 3 — SHUFFLE & SORT:**
Framework groups all values by key across all mappers and sends to appropriate reducers.
```
After shuffle (sorted by key):
(big,  [2])         → Reducer 1
(data, [1, 2])      → Reducer 1
(fast, [1])         → Reducer 2
(is,   [1, 1])      → Reducer 2
```

**Phase 4 — REDUCE:**
Reducer sums the list of values for each key and writes to HDFS.
```
Reducer 1 output:         Reducer 2 output:
(big,  2)                 (fast, 1)
(data, 3)                 (is,   2)
```

**Full Pipeline Diagram:**
```
HDFS Input
   │
   ├──► [Mapper 1] ──► [Combiner 1] ──┐
   │                                   ├──► [Shuffle & Sort] ──► [Reducer 1] ──► HDFS Output
   └──► [Mapper 2] ──► [Combiner 2] ──┘                    └──► [Reducer 2] ──► HDFS Output
```

**Java MapReduce Skeleton:**
```java
// Mapper
public class WordMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    public void map(LongWritable key, Text value, Context ctx) throws IOException {
        String[] words = value.toString().split("\\s+");
        for (String word : words) {
            ctx.write(new Text(word.toLowerCase()), new IntWritable(1));
        }
    }
}
// Reducer
public class WordReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    public void reduce(Text key, Iterable<IntWritable> values, Context ctx) throws IOException {
        int sum = 0;
        for (IntWritable val : values) sum += val.get();
        ctx.write(key, new IntWritable(sum));
    }
}
```

> **💡 Depth of Understanding:**
> The **Combiner is optional but critical for performance**. Without it, all `(word, 1)` pairs are shuffled over the network — for a 1TB input with "the" appearing 100M times, that's 100M key-value pairs just for "the". With combiner, each mapper sends one `(the, N)` instead. The combiner works only when the reduce function is **commutative and associative** (sum, max, min work; average does NOT work directly). MapReduce is mostly replaced by **Spark** today (10-100x faster due to in-memory DAG), but its conceptual phases (map→shuffle→reduce) still underlie all distributed processing frameworks.

---

### Q1-B.3: Data Visualization Tools for Big Data [5 Marks]

**Core Tools and Their Roles:**

| Tool | Type | Best For | Scale |
|---|---|---|---|
| **Matplotlib / Seaborn** | Static (Python) | EDA, statistical distributions | <100K rows |
| **Plotly / Dash** | Interactive (Python) | Drill-down dashboards, web apps | Up to 1M rows |
| **Tableau** | BI Platform | Executive dashboards, drag-and-drop | Millions (with extract) |
| **Power BI** | BI Platform | Microsoft ecosystem integration | Large aggregated data |
| **Apache Superset** | Open-source BI | SQL-backed dashboards on Spark/Presto | Billions (server-side) |
| **Datashader** | Server-side rendering | Billion-point scatter plots | True big data scale |
| **Grafana** | Real-time monitoring | Time-series, Kafka/Spark streaming metrics | Real-time streams |

**Workflow for Big Data Visualization:**
```
Raw Data (TB scale in HDFS/S3)
         │
         ▼
[Spark SQL Aggregation]  ← Always aggregate first!
         │
         ▼
Summary DataFrame (MB scale)
         │
         ▼
[Plotly / Tableau / Superset]
         │
         ▼
Interactive Dashboard
```

**Healthcare-specific visualization needs:**
- Patient trend analysis → Plotly line charts with time-slider
- Geographic disease spread → Folium/Kepler.gl choropleth maps
- Survival analysis → Kaplan-Meier curves (matplotlib + lifelines)
- Real-time ICU monitoring → Grafana + InfluxDB

> **💡 Depth of Understanding:**
> The fundamental rule: **never send raw big data to the visualization layer**. Always pre-aggregate with Spark/SQL. Tools like Apache Superset connect directly to Spark Thrift Server and execute SQL queries on the cluster — the browser only receives the aggregated result (e.g., 12 data points for a monthly chart), never the raw billions of rows. **D3.js** is the gold standard for custom, pixel-perfect visualizations but requires JavaScript expertise. For ML results visualization, **MLflow UI** tracks experiment metrics, model versions, and hyperparameter comparisons automatically.

---

### Q1-B.4: Distributed Tools and Libraries [5 Marks]

| Tool/Library | Category | Key Features |
|---|---|---|
| **Apache Spark** | Processing Engine | In-memory DAG, 100x faster than MapReduce, Python/Scala/Java/R APIs |
| **Apache Hadoop** | Storage + Processing | HDFS + MapReduce, mature ecosystem, batch workloads |
| **Apache Kafka** | Message Broker | Distributed log, high-throughput streaming, replay capability |
| **Apache Hive** | SQL on Hadoop | HiveQL (SQL-like), schema-on-read, integrates with YARN |
| **Apache Pig** | ETL Framework | Pig Latin (procedural), good for data pipeline scripting |
| **Apache HBase** | NoSQL on Hadoop | Column-family store on HDFS, low-latency random reads |
| **Apache Cassandra** | Distributed DB | Masterless, high-write throughput, eventual consistency |
| **MongoDB** | Document Store | Flexible JSON schema, rich query language, horizontal sharding |
| **GraphX / GraphFrames** | Graph Processing | PageRank, connected components, Pregel-style computation |
| **MLlib** | ML Library | Spark-native ML: classification, clustering, regression, pipelines |

**Comparison — Batch vs Stream:**

| Dimension | Spark (Batch) | Kafka + Spark Streaming |
|---|---|---|
| Latency | Seconds to hours | Milliseconds to seconds |
| Data | Bounded (finite) | Unbounded (infinite) |
| Use Case | Reports, ETL | Real-time alerts, dashboards |
| Fault Tolerance | Lineage recomputation | Checkpointing + offset tracking |

> **💡 Depth of Understanding:**
> The **CAP Theorem** governs distributed database design: a system can only guarantee two of three — Consistency, Availability, Partition Tolerance. HBase: CP (consistent + partition tolerant). Cassandra: AP (available + partition tolerant). MongoDB: CP by default (tunable with `w:0` write concern). Understanding these trade-offs is critical when choosing a distributed tool for a specific use case (e.g., financial transactions need CP; social media likes can tolerate AP).

---

## Q2 (Q3 in paper): Kafka Streaming Architecture for Uber [10 Marks]

### System Requirements

Uber's ride-booking platform must handle:
- **Millions of concurrent ride requests** globally
- **GPS pings** from millions of active drivers (high velocity)
- **Sub-second matching** between riders and drivers
- **Dynamic surge pricing** based on real-time supply/demand
- **Exactly-once** payment processing (no duplicate charges)

### Kafka Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                      UBER KAFKA ECOSYSTEM                            │
│                                                                      │
│  PRODUCERS                    KAFKA CLUSTER                          │
│  ┌────────────┐               ┌──────────────────────────────────┐   │
│  │ Rider App  │──────────────►│ Topic: ride-requests             │   │
│  │ (TripReq)  │               │ Partitioned by city/geo-hash     │   │
│  └────────────┘               └──────────────┬───────────────────┘   │
│                                              │                       │
│  ┌────────────┐               ┌──────────────▼───────────────────┐   │
│  │ Driver App │──────────────►│ Topic: driver-location-stream    │   │
│  │ (GPS ping) │               │ Partitioned by driver_id         │   │
│  └────────────┘               └──────────────┬───────────────────┘   │
│                                              │                       │
│  ┌────────────┐               ┌──────────────▼───────────────────┐   │
│  │ Payment Svc│──────────────►│ Topic: trip-events               │   │
│  └────────────┘               │ (Assigned, Started, Completed)   │   │
│                               └──────────────┬───────────────────┘   │
│                                              │                       │
│  CONSUMERS                                   │                       │
│  ┌───────────────────────────────────────────▼──────────────────┐    │
│  │  Matching Service  ◄── ride-requests + driver-location-stream │    │
│  │  → Assigns nearest driver → Publishes to trip-events          │    │
│  └──────────────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │  Surge Pricing Engine ◄── ride-requests + driver-location     │    │
│  │  → Computes demand/supply ratio → Updates price multiplier    │    │
│  └──────────────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │  Notification Service ◄── trip-events                         │    │
│  │  → Sends push notifications to rider/driver mobile apps       │    │
│  └──────────────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │  Analytics (Spark Streaming) ◄── all topics                   │    │
│  │  → Real-time dashboards, fraud detection, ETA prediction      │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

### Key Topics and Partitioning Strategy

| Kafka Topic | Partition Key | Consumers | Purpose |
|---|---|---|---|
| `ride-requests` | `city_id` or `geo_hash` | Matching Service | Route requests to local matchers |
| `driver-location-stream` | `driver_id` | Matching, ETA, Surge | GPS stream at ~1 ping/4 sec per driver |
| `trip-events` | `trip_id` | Notification, Analytics, Payment | Lifecycle tracking |
| `payment-events` | `user_id` | Payment Service | Exactly-once billing |
| `notifications` | `user_id` | Push Gateway | Mobile push notifications |

### Challenges and Solutions

| Challenge | Kafka Solution |
|---|---|
| **Millions of GPS pings/sec** | Partition `driver-location` by `driver_id`; 100+ partitions across brokers |
| **Driver-Rider matching latency** | Consumer groups with dedicated matching threads per city partition |
| **Duplicate payment charges** | Idempotent producer (`enable.idempotence=true`) + exactly-once transactions |
| **Global multi-region** | Cross-cluster replication (MirrorMaker 2) between regional clusters |
| **Message replay for debugging** | Kafka's durable log retention allows replaying historical events |
| **Varied consumer languages** | Consumer proxy layer standardizes Go, Python, Java consumer SDKs |

### Real-Time Flow
```
1. Rider opens app → TripRequested event → [Kafka: ride-requests]
2. Matching Service consumes → queries driver-location → assigns driver
3. DriverAssigned event → [Kafka: trip-events]
4. Notification Service → "Your driver is 3 min away" push notification
5. Driver GPS pings → [Kafka: driver-location-stream] → Rider map updates
6. TripCompleted → [Kafka: trip-events] → Payment Service charges card
```

> **💡 Depth of Understanding:**
> Uber built **uReplicator** (open-sourced) to handle cross-cluster Kafka replication more reliably than stock MirrorMaker. They also built **Chaperone** for auditing message delivery (ensuring no data loss between producer and consumer). At Uber's scale, Kafka handles **1+ trillion messages per day**. The shift from per-region monoliths to Kafka-backed microservices allowed each team to independently deploy and scale their service without coordination — a key enabler of Uber's engineering velocity.

---

## Q4.1: Pig Latin Script – Log File Processing [10 Marks]

### Problem
Process a large log file containing `user_id`, `timestamp`, and `action` performed. Count number of actions per user and display aggregated result.

### Sample Log File Format (log_data.csv)
```
user_id,timestamp,action
U001,2024-01-15 09:00:01,LOGIN
U002,2024-01-15 09:00:05,SEARCH
U001,2024-01-15 09:01:10,CLICK
U003,2024-01-15 09:01:30,PURCHASE
U002,2024-01-15 09:02:00,CLICK
U001,2024-01-15 09:03:45,LOGOUT
U003,2024-01-15 09:04:00,LOGIN
U002,2024-01-15 09:05:10,PURCHASE
```

### Complete Pig Latin Script

```pig
-- Step 1: Load the raw log file from HDFS
raw_logs = LOAD '/data/logs/log_data.csv'
           USING PigStorage(',')
           AS (user_id:chararray, timestamp:chararray, action:chararray);

-- Step 2: Filter out the header row (if present)
clean_logs = FILTER raw_logs BY user_id != 'user_id';

-- Step 3: Project only the fields we need
user_actions = FOREACH clean_logs GENERATE user_id, action;

-- Step 4: Group records by user_id
-- Creates: (user_id, {(user_id, action), (user_id, action), ...})
grouped = GROUP user_actions BY user_id;

-- Step 5: Count actions per user
action_counts = FOREACH grouped GENERATE
    group       AS user_id,
    COUNT(user_actions)  AS total_actions;

-- Step 6: Order by total_actions descending (most active user first)
sorted_counts = ORDER action_counts BY total_actions DESC;

-- Step 7: Display results (use STORE for HDFS output in production)
DUMP sorted_counts;

-- Production: Save to HDFS
-- STORE sorted_counts INTO '/output/user_action_counts'
--     USING PigStorage(',');
```

### Expected Output
```
(U001, 3)
(U002, 3)
(U003, 2)
```

### Extended Script – Count Actions Per User Per Action Type

```pig
-- Load
logs = LOAD '/data/logs/log_data.csv' USING PigStorage(',')
       AS (user_id:chararray, ts:chararray, action:chararray);

-- Group by user + action type
grp = GROUP logs BY (user_id, action);

-- Count each (user, action) combination
action_type_counts = FOREACH grp GENERATE
    FLATTEN(group)       AS (user_id, action),
    COUNT(logs)          AS count;

-- Filter: show only PURCHASE actions
purchases = FILTER action_type_counts BY action == 'PURCHASE';

-- Sort by user
sorted = ORDER purchases BY user_id ASC;
DUMP sorted;
-- Output: (U002, PURCHASE, 1)  (U003, PURCHASE, 1)
```

### Pig Latin Operators Used

| Operator | Purpose |
|---|---|
| `LOAD` | Read data from HDFS with schema |
| `FILTER` | Remove unwanted rows (WHERE equivalent) |
| `FOREACH ... GENERATE` | Project/transform fields (SELECT equivalent) |
| `GROUP BY` | Aggregate records by key |
| `COUNT()` | Built-in function to count tuples in a bag |
| `ORDER BY` | Sort results |
| `DUMP` | Print to console (triggers execution) |
| `STORE` | Save to HDFS (production use) |

> **💡 Depth of Understanding:**
> Pig translates each Latin script into a series of MapReduce (or Tez/Spark) jobs automatically. A `GROUP BY` becomes a MapReduce shuffle; `FOREACH` becomes a map-side transformation. Pig's **lazy evaluation** means nothing executes until `DUMP` or `STORE` is called — Pig builds the full execution plan first, then optimizes it (e.g., combining multiple `FOREACH` into a single map phase). Like Spark, Pig is largely superseded by **Spark SQL** in modern clusters, but it remains on exam syllabi for its conceptual value in understanding data flow programming.

---

## Q4.2: Spark SQL – Affairs Dataset [10 Marks]

### Schema (df.printSchema() output)
```
root
 |-- affairs: integer (nullable = true)
 |-- gender: string (nullable = true)
 |-- age: double (nullable = true)
 |-- ym: double (nullable = true)          ← years married
 |-- children: string (nullable = true)    ← "yes" or "no"
 |-- religiousness: integer (nullable = true)
 |-- education: integer (nullable = true)
 |-- occupation: integer (nullable = true)
 |-- rate: integer (nullable = true)       ← marriage rating 1-5
 |-- nbaffairs: integer (nullable = true)  ← number of affairs
```

**Register as Temp View:**
```python
df.createOrReplaceTempView("affairs")
```

---

**i. Average age of individuals involved in marital affairs**

```python
# Spark SQL
result_i = spark.sql(
    "SELECT ROUND(AVG(age), 2) AS avg_age_with_affairs "
    "FROM affairs "
    "WHERE nbaffairs > 0"
)
result_i.show()

# DataFrame API
from pyspark.sql.functions import avg, round as spark_round, col
df.filter(col("nbaffairs") > 0) \
  .agg(spark_round(avg("age"), 2).alias("avg_age_with_affairs")) \
  .show()
```

---

**ii. Maximum years married among individuals with at least one child**

```python
# Spark SQL
result_ii = spark.sql(
    "SELECT MAX(ym) AS max_years_married "
    "FROM affairs "
    "WHERE children = 'yes'"
)
result_ii.show()

# DataFrame API
from pyspark.sql.functions import max as spark_max
df.filter(col("children") == "yes") \
  .agg(spark_max("ym").alias("max_years_married")) \
  .show()
```

---

**iii. Percentage of marriages rated above 4 among individuals who had affairs**

```python
# Spark SQL (rate > 4 means rate = 5, the maximum)
result_iii = spark.sql(
    "SELECT ROUND( "
    "  SUM(CASE WHEN rate > 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), "
    "  2) AS pct_high_rated_with_affairs "
    "FROM affairs "
    "WHERE nbaffairs > 0"
)
result_iii.show()

# DataFrame API
from pyspark.sql.functions import sum as spark_sum, when
affairs_df = df.filter(col("nbaffairs") > 0)
total = affairs_df.count()
affairs_df.agg(
    spark_round(
        spark_sum(when(col("rate") > 4, 1).otherwise(0)) * 100.0 / total,
        2
    ).alias("pct_high_rated_with_affairs")
).show()
```

---

**iv. Average age of individuals involved in affairs, grouped by number of children**

```python
# Spark SQL
result_iv = spark.sql(
    "SELECT children, "
    "       ROUND(AVG(age), 2) AS avg_age "
    "FROM affairs "
    "WHERE nbaffairs > 0 "
    "GROUP BY children "
    "ORDER BY children"
)
result_iv.show()

# DataFrame API
df.filter(col("nbaffairs") > 0) \
  .groupBy("children") \
  .agg(spark_round(avg("age"), 2).alias("avg_age")) \
  .orderBy("children") \
  .show()
```

**Expected Output:**
```
+--------+--------+
|children| avg_age|
+--------+--------+
|      no|   28.54|
|     yes|   32.17|
+--------+--------+
```

> **💡 Depth of Understanding:**
> The **Affairs dataset** (Fair's dataset from R's `Ecdat` package) is a classic dataset for studying discrete dependent variables. The `rate` field is an ordinal Likert scale (1=very unhappy, 5=very happy). Using `rate > 4` correctly captures only the top category. In real-world analyses, you'd use **Spark MLlib LogisticRegression** to predict probability of having an affair based on age, ym, religiousness, and rate — a classic classification problem demonstrating imbalanced class handling, feature engineering, and model evaluation on distributed data.

---

## Q5.1: PageRank – Find Rank of All Web Pages [5 Marks]

### Graph Definition

Assume the following web graph (N = 4 pages):
- **A** → M, H
- **M** → A
- **H** → A, M
- **P** → H *(P has no incoming links)*

```
P ──► H ◄─────┐
      │        │
      ▼        │
      A ──────►M
      ▲        │
      └────────┘
Incoming: A←{M,H}  M←{A,H}  H←{P}  P←{nobody}
```

**Formula:** PR(p) = (1−d)/N + d × Σ[PR(q)/OutDeg(q)], d=0.85, N=4, (1−d)/N = 0.0375

**Init:** PR₀(A)=PR₀(M)=PR₀(H)=PR₀(P) = 0.25

**Iteration 1:**

```
PR₁(A) = 0.0375 + 0.85×[PR₀(M)/1 + PR₀(H)/2]
        = 0.0375 + 0.85×[0.25 + 0.125]
        = 0.0375 + 0.31875 = 0.35625

PR₁(M) = 0.0375 + 0.85×[PR₀(A)/2 + PR₀(H)/2]
        = 0.0375 + 0.85×[0.125 + 0.125]
        = 0.0375 + 0.2125 = 0.25

PR₁(H) = 0.0375 + 0.85×[PR₀(P)/1]
        = 0.0375 + 0.85×0.25
        = 0.0375 + 0.2125 = 0.25

PR₁(P) = 0.0375 + 0.85×0
        = 0.0375
```

**Results:**

| Page | PR₀ | PR₁ | Rank |
|---|---|---|---|
| A | 0.25 | **0.3563** | 🥇 1st |
| M | 0.25 | 0.2500 | 🥈 2nd |
| H | 0.25 | 0.2500 | 🥈 2nd |
| P | 0.25 | **0.0375** | 4th |
| **Sum** | **1.0** | **1.0** | ✅ |

**PySpark GraphX Implementation:**
```python
from graphframes import GraphFrame

vertices = spark.createDataFrame([
    ("A","PageA"),("M","PageM"),("H","PageH"),("P","PageP")
], ["id","name"])

edges = spark.createDataFrame([
    ("A","M","link"),("A","H","link"),
    ("M","A","link"),
    ("H","A","link"),("H","M","link"),
    ("P","H","link")
], ["src","dst","rel"])

g = GraphFrame(vertices, edges)
ranks = g.pageRank(resetProbability=0.15, maxIter=10)
ranks.vertices.select("id","pagerank").orderBy("pagerank", ascending=False).show()
```

> **💡 Depth of Understanding:**
> Page A ranks highest because two pages (M and H) both link to it, concentrating PageRank. Page P ranks lowest — it has no incoming links; it only receives the random teleportation baseline 0.0375. In Spark GraphX, `pageRank(tol=0.0001)` runs until convergence (values change < tolerance); `staticPageRank(numIter=10)` runs exactly 10 iterations. **Personalized PageRank** biases the random surfer toward a set of seed nodes — used in Pinterest's Pixie recommendation system to find items similar to what a user just pinned.

---

## Q5.2: MongoDB Schema Design from RDBMS [10 Marks]

### Given RDBMS Schema (Relational)

```sql
-- Products table
CREATE TABLE Products (
    product_id   INT PRIMARY KEY,
    name         VARCHAR(100),
    brand        VARCHAR(50),
    base_price   DECIMAL(10,2),
    category_id  INT
);

-- Categories table
CREATE TABLE Categories (
    category_id  INT PRIMARY KEY,
    name         VARCHAR(50)
);

-- Variants table (sizes, colors)
CREATE TABLE Variants (
    variant_id   INT PRIMARY KEY,
    product_id   INT,
    color        VARCHAR(30),
    size         VARCHAR(10),
    stock        INT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Reviews table
CREATE TABLE Reviews (
    review_id    INT PRIMARY KEY,
    product_id   INT,
    user_id      INT,
    rating       INT,
    comment      TEXT,
    review_date  DATE
);
```

### MongoDB Schema Design (Document Model)

**Design Principle:** Embed frequently-read data together; reference large/unbounded arrays.

**Products Collection** (embeds category + variants; references reviews):

```json
{
  "_id": 5001,
  "name": "Classic Running Shoe",
  "brand": "ActiveGear",
  "base_price": 89.99,
  "category": {
    "category_id": 10,
    "name": "Footwear"
  },
  "variants": [
    { "color": "Red",  "size": "9",  "stock": 50 },
    { "color": "Blue", "size": "10", "stock": 25 },
    { "color": "Red",  "size": "10", "stock": 10 }
  ],
  "avg_rating": 4.3,
  "total_reviews": 128
}
```

**Reviews Collection** (separate — unbounded, grows over time):
```json
{
  "_id": ObjectId("..."),
  "product_id": 5001,
  "user_id": 901,
  "rating": 5,
  "comment": "Great shoes, very comfortable!",
  "review_date": ISODate("2024-03-15")
}
```

### MongoDB CRUD Operations

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
products = db["products"]
reviews  = db["reviews"]

# ── i. Find product collection with price < 5000 ──────────────────
affordable = products.find(
    {"base_price": {"$lt": 5000}},
    {"name": 1, "brand": 1, "base_price": 1, "_id": 0}
)
for p in affordable:
    print(p)

# ── ii. Find all products in "Footwear" category ─────────────────
footwear = products.find(
    {"category.name": "Footwear"},
    {"name": 1, "base_price": 1}
)

# ── iii. Find products with avg_rating >= 4 ──────────────────────
top_rated = products.find(
    {"avg_rating": {"$gte": 4}},
    {"name": 1, "avg_rating": 1, "brand": 1}
).sort("avg_rating", -1)

# ── iv. Update stock for a specific variant ──────────────────────
products.update_one(
    {"_id": 5001, "variants.color": "Red", "variants.size": "9"},
    {"$set": {"variants.$.stock": 45}}
)

# ── v. Insert a new product ──────────────────────────────────────
new_product = {
    "_id": 5002,
    "name": "Trail Running Jacket",
    "brand": "ActiveGear",
    "base_price": 120.00,
    "category": {"category_id": 11, "name": "Apparel"},
    "variants": [
        {"color": "Black", "size": "M", "stock": 30},
        {"color": "Grey",  "size": "L", "stock": 20}
    ],
    "avg_rating": 0,
    "total_reviews": 0
}
products.insert_one(new_product)

# ── vi. Aggregation: Average price per category ──────────────────
pipeline = [
    {"$group": {
        "_id": "$category.name",
        "avg_price": {"$avg": "$base_price"},
        "count":     {"$sum": 1}
    }},
    {"$sort": {"avg_price": -1}}
]
result = list(products.aggregate(pipeline))
for r in result:
    print(r)
```

### RDBMS vs MongoDB Comparison

| Aspect | RDBMS | MongoDB |
|---|---|---|
| **Schema** | Fixed, predefined | Flexible, schema-on-read |
| **Joins** | Explicit JOINs at query time | Embed related data in document |
| **Scaling** | Vertical (bigger server) | Horizontal (sharding) |
| **Transactions** | ACID by default | ACID from v4.0 (multi-document) |
| **Best For** | Structured, relational data | Hierarchical, variable-structure data |
| **Query Language** | SQL (declarative) | MQL — MongoDB Query Language |

> **💡 Depth of Understanding:**
> The MongoDB **Aggregation Pipeline** is the equivalent of SQL GROUP BY + JOIN + HAVING. Stages flow sequentially: `$match` → `$group` → `$sort` → `$project`. For the RDBMS-to-MongoDB migration decision, use the **Embedding vs Referencing** rule: embed when data is "owned" by the parent and rarely changes (variants of a product); reference when data is shared across many documents or is unbounded in size (reviews). MongoDB 5.0+ introduced **time-series collections** with native time-series compression — ideal for IoT sensor data or financial tick data, competing with InfluxDB.

---

## Q5.3: MLlib Pipeline for Text Processing [5 Marks]

### What is an MLlib Pipeline?

A **Pipeline** chains multiple data transformation and ML stages into a single, reproducible workflow. Each stage is either a **Transformer** (transforms data) or an **Estimator** (fits a model from data).

```
Raw Text DataFrame
      │
      ▼
[Stage 1: Tokenizer]          → splits "big data rocks" → ["big","data","rocks"]
      │
      ▼
[Stage 2: StopWordsRemover]   → removes "the","a","is" etc.
      │
      ▼
[Stage 3: HashingTF]          → converts words to sparse TF vector (hashing trick)
      │
      ▼
[Stage 4: IDF]                → down-weights common words across corpus
      │
      ▼
[Stage 5: LogisticRegression] → classifies text (spam/ham, sentiment, category)
      │
      ▼
Predictions DataFrame
```

### Complete PySpark MLlib Pipeline

```python
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
)
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession.builder.appName("TextClassificationPipeline").getOrCreate()

# Sample dataset: news articles with categories
data = spark.createDataFrame([
    ("Breaking news about the economy and finance", "business"),
    ("Sports team wins the championship game",      "sports"),
    ("New machine learning model beats benchmarks", "tech"),
    ("Stock market crashes amid economic crisis",   "business"),
    ("Football player scores winning goal",         "sports"),
    ("AI model generates realistic images",         "tech"),
], ["text", "label"])

# Stage 1: Convert label string to numeric index
indexer = StringIndexer(inputCol="label", outputCol="label_idx")

# Stage 2: Tokenize text into words
tokenizer = Tokenizer(inputCol="text", outputCol="words")

# Stage 3: Remove stop words
remover = StopWordsRemover(inputCol="words", outputCol="filtered")

# Stage 4: Term Frequency — hash words into feature vector
hashingTF = HashingTF(inputCol="filtered", outputCol="raw_features", numFeatures=1000)

# Stage 5: Inverse Document Frequency — penalize common words
idf = IDF(inputCol="raw_features", outputCol="features")

# Stage 6: Logistic Regression classifier
lr = LogisticRegression(featuresCol="features", labelCol="label_idx", maxIter=20)

# Build the Pipeline
pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashingTF, idf, lr])

# Split data into train/test
train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)

# Fit (train) the full pipeline
model = pipeline.fit(train_data)

# Transform (predict) on test data
predictions = model.transform(test_data)
predictions.select("text", "label", "prediction").show(truncate=False)

# Evaluate
evaluator = MulticlassClassificationEvaluator(
    labelCol="label_idx", predictionCol="prediction", metricName="accuracy"
)
accuracy = evaluator.evaluate(predictions)
print(f"Test Accuracy: {accuracy:.2%}")
```

### Why Pipeline is Powerful for Large Datasets

| Benefit | Explanation |
|---|---|
| **Single fit/transform** | Entire workflow trains and predicts in one call |
| **No data leakage** | IDF statistics computed only on training data, applied to test |
| **Reproducibility** | Save & reload entire pipeline with `model.save(path)` |
| **Cross-validation** | `CrossValidator` can tune all stages' parameters jointly |
| **Distributed** | All stages run on Spark executors — scales to billions of documents |

### TF-IDF Concept

```
TF(word, doc)  = count of word in doc / total words in doc
IDF(word)      = log(total docs / docs containing word)
TF-IDF         = TF × IDF

Example:
  "data" appears 5x in 100-word doc → TF = 0.05
  "data" appears in 1000 of 10000 docs → IDF = log(10) = 2.303
  TF-IDF("data") = 0.05 × 2.303 = 0.115

  "the" appears 10x → TF = 0.10
  "the" appears in 9999 of 10000 docs → IDF = log(1.0001) ≈ 0.0001
  TF-IDF("the") ≈ 0.00001  ← near zero, effectively filtered out
```

> **💡 Depth of Understanding:**
> `HashingTF` uses the **hashing trick** — maps each word to a bucket using a hash function, avoiding the need to build a global vocabulary dictionary. This makes it stateless and memory-efficient for massive corpora (billions of documents). The trade-off is **hash collisions** (two different words map to same bucket), which can be reduced by increasing `numFeatures`. For tasks requiring exact vocabulary, use `CountVectorizer` instead (builds vocabulary in a first pass, then vectorizes). **Word2Vec** (also in MLlib) produces dense semantic embeddings — "king" − "man" + "woman" ≈ "queen" — capturing meaning, not just frequency, making it superior for semantic similarity tasks.

---

## 📋 Quick Revision Table – PYQ 2024

| Q | Key Points |
|---|---|
| **Q1-A.1** | Healthcare 3Vs: EHR=Volume, ICU streams=Velocity, DICOM+notes=Variety |
| **Q1-A.2** | Hadoop = NameNode + DataNode + YARN (ResourceManager + NodeManager) |
| **Q1-B.1** | Heartbeat=3s, 10 missed=dead, rack awareness: local→diff rack→same remote rack |
| **Q1-B.2** | Map→Combiner(local)→Shuffle&Sort(group by key)→Reduce; combiner = mini-reducer |
| **Q1-B.3** | Never plot raw big data; aggregate first with Spark; Superset/Grafana for scale |
| **Q1-B.4** | CAP: HBase=CP, Cassandra=AP, MongoDB=CP; Spark 100x faster than MapReduce |
| **Q2/Q3** | Kafka topics: ride-requests, driver-location, trip-events; exactly-once for payments |
| **Q4.1** | Pig: LOAD→FILTER→GROUP→FOREACH GENERATE COUNT→DUMP |
| **Q4.2** | `WHERE nbaffairs>0`; `WHERE children='yes'`; `SUM(CASE WHEN rate>4)` |
| **Q5.1** | PR(A)=0.3563 (highest), PR(P)=0.0375 (lowest, no incoming links) |
| **Q5.2** | Embed variants in product doc; reference reviews (unbounded); `$group` for aggregation |
| **Q5.3** | Pipeline: StringIndexer→Tokenizer→StopWordsRemover→HashingTF→IDF→LR |

---
*BDA PYQ May 2024 – Complete Solutions | Pandit Deendayal Energy University*
