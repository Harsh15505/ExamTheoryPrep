# BDA PYQ 2025 – Complete Solutions
**Pandit Deendayal Energy University | Re-End Sem Exam (May 2025)**
**Course: Big Data Analytics (B23CP309) | Max Marks: 100 | Time: 3 Hours**

---

## Q1-A: Answer ANY ONE [10 Marks]

### Option 1: Big Data 3Vs in Smart City Infrastructure

**Volume, Velocity, and Variety** are the three core dimensions of Big Data. In a smart city, all three manifest simultaneously:

| V | Smart City Source | Scale |
|---|---|---|
| **Volume** | IoT sensors, CCTV cameras, smart meters, GPS feeds | Petabytes/year per city |
| **Velocity** | Real-time traffic signals, emergency alerts, live energy grid | Milliseconds to seconds |
| **Variety** | Structured (meter readings), Semi-structured (JSON GPS), Unstructured (video, audio) | Hundreds of formats |

**Why Big Data Analytics becomes necessary:**
- Traditional RDBMS cannot horizontally scale to store sensor data from millions of devices.
- SQL batch queries cannot meet real-time traffic rerouting requirements (needs stream processing).
- A single city generates data in CSV, JSON, video, satellite images — no single schema fits all.

**Big Data techniques adopted:**
1. **HDFS / S3** → Distributed storage for volume
2. **Kafka / Spark Streaming** → Real-time ingestion for velocity
3. **NoSQL (MongoDB, Cassandra)** → Flexible schema for variety
4. **GraphX / Neo4j** → Network analysis (roads, power grids)

---

### Option 2: Hadoop Architecture & Big Data Analytics Adoption

Hadoop is a distributed computing framework built on two core components: **HDFS** (storage) and **MapReduce** (processing).

```
┌──────────────────────────────────────────────┐
│               HADOOP CLUSTER                 │
│                                              │
│   ┌────────────┐      ┌──────────────────┐   │
│   │  NameNode  │◄────►│  Secondary       │   │
│   │  (Master)  │      │  NameNode        │   │
│   │            │      │  (Checkpoint)    │   │
│   │ - Metadata │      └──────────────────┘   │
│   │ - FSImage  │                             │
│   │ - EditLog  │                             │
│   └─────┬──────┘                             │
│         │ heartbeat + block reports          │
│    ┌────▼───────────────────────────────┐    │
│    │          DataNodes (Slaves)        │    │
│    │  ┌──────┐  ┌──────┐  ┌──────┐    │    │
│    │  │ DN-1 │  │ DN-2 │  │ DN-3 │    │    │
│    │  │Blk-1 │  │Blk-1 │  │Blk-2 │    │    │
│    │  │Blk-3 │  │Blk-2 │  │Blk-3 │    │    │
│    │  └──────┘  └──────┘  └──────┘    │    │
│    └────────────────────────────────────┘    │
│                                              │
│   ┌──────────────────────────────────────┐   │
│   │   YARN (Resource Manager)            │   │
│   │   + MapReduce / Spark Jobs           │   │
│   └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
```

**Key Components:**
- **NameNode**: Stores metadata (file-to-block mapping). Does NOT store actual data.
- **DataNode**: Stores actual data blocks. Sends heartbeat every 3 seconds to NameNode.
- **Secondary NameNode**: Periodically merges FSImage + EditLog (NOT a hot standby).
- **YARN**: Negotiates resources and schedules jobs on the cluster.

**Adoption for Big Data Analytics:**
- Hadoop enables schema-on-read, so raw unstructured data can be stored first, analyzed later.
- Horizontal scaling: add commodity hardware nodes cheaply.
- Fault tolerance through replication (default 3x).

> **💡 Depth of Understanding:**
> Hadoop is considered the "first wave" of Big Data. Modern stacks replace MapReduce with Spark (10–100x faster in-memory), and HDFS with cloud object stores (S3, GCS). However, the NameNode single-point-of-failure problem led to **HDFS HA** using ZooKeeper + Standby NameNode, and later **HDFS Federation** for massive deployments.

---

## Q1-B: HDFS – 1TB Log File Storage [10 Marks]

### (a) How HDFS Stores Data & Maintains Fault Tolerance

**Data Storage Process:**
1. Client contacts NameNode to start a write.
2. NameNode returns a list of DataNodes to write to (pipeline).
3. File is split into **128 MB blocks**.
4. Each block is written to the first DataNode, which replicates to the second, which replicates to the third (pipeline replication).
5. NameNode updates its metadata once all replicas confirm.

```
CLIENT
  │
  ├──► NameNode: "I want to write file.log"
  │◄── "Write Block-1 to: DN1 → DN2 → DN4"
  │
  ├──► DN1 ──► DN2 ──► DN4  (Block-1 pipeline)
  ├──► DN2 ──► DN3 ──► DN5  (Block-2 pipeline)
  └──► ...
```

**Fault Tolerance Mechanism:**
- **Heartbeat**: Each DataNode sends heartbeat every 3 sec. If NameNode misses 10 heartbeats (~30 sec), DataNode is declared dead.
- **Block Report**: DataNode reports all its blocks to NameNode on startup and periodically.
- **Under-replication**: If a DataNode dies and a block drops below replication factor, NameNode schedules re-replication on a healthy node.
- **Rack Awareness**: 1st replica → local node, 2nd → different rack, 3rd → same remote rack. Survives entire rack failure.

### (b) What Happens When a DataNode Fails During Write?

During an active write pipeline (e.g., DN1 → DN2 → DN3):
1. If **DN2 fails mid-write**, the pipeline is broken.
2. The client receives an error acknowledgment.
3. The block written so far is given a new unique ID to avoid stale data conflicts.
4. NameNode is notified and removes DN2 from the pipeline.
5. Writing resumes with a new pipeline using remaining healthy nodes (DN1 → DN3).
6. Once the write completes, NameNode detects the block is under-replicated (only 2 copies) and schedules a 3rd replica copy to another available DataNode.

### (c) Block Calculation

```
File Size         = 1 TB = 1024 GB = 1,048,576 MB
Block Size        = 128 MB
Number of Blocks  = ⌈1,048,576 / 128⌉ = 8,192 blocks
Replication Factor= 3

Total Storage     = 8,192 × 128 MB × 3
                  = 3,145,728 MB
                  = 3,072 GB
                  = 3 TB
```

**Summary:**
| Metric | Value |
|---|---|
| Blocks Created | 8,192 |
| Storage per replica | 1 TB |
| Total Storage (3x replication) | **3 TB** |

> **💡 Depth of Understanding:**
> The "small files problem" in HDFS: if you store millions of 1 KB files, each file still uses one metadata entry in NameNode memory (~150 bytes per block). 1 billion files = ~150 GB of NameNode RAM. Solutions include **HAR (Hadoop Archive)** files, **SequenceFiles**, or using **HBase** for small object storage. Also note: block size of 128 MB is configurable — Spark clusters often use 256 MB blocks to reduce the number of tasks on very large files.

---

## Q2: Apache Kafka – Real-Time Analytics [10 Marks]

### (a) Kafka Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    KAFKA CLUSTER                         │
│                                                          │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │
│  │  Broker 1   │   │  Broker 2   │   │  Broker 3   │   │
│  │             │   │             │   │             │   │
│  │ Topic-A P0  │   │ Topic-A P1  │   │ Topic-A P2  │   │
│  │ (Leader)    │   │ (Leader)    │   │ (Leader)    │   │
│  │ Topic-A P1  │   │ Topic-A P2  │   │ Topic-A P0  │   │
│  │ (Follower)  │   │ (Follower)  │   │ (Follower)  │   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘   │
│         └─────────────────┼─────────────────┘           │
│                           │                             │
│              ZooKeeper / KRaft (Metadata)               │
└───────────────────────────┼──────────────────────────────┘
            ▲               │               ▼
     ┌──────┴──────┐        │      ┌────────────────────┐
     │  Producers  │        │      │   Consumer Group   │
     │             │        │      │  Consumer A → P0   │
     │ App Logs    │        │      │  Consumer B → P1   │
     │ Clickstream │        │      │  Consumer C → P2   │
     └─────────────┘        │      └────────────────────┘
                            │
                     Offset Tracking
```

**Core Components:**
| Component | Role |
|---|---|
| **Producer** | Publishes messages to topics; uses key-based or round-robin partitioning |
| **Broker** | Server in cluster; stores partitions; handles leader/follower replication |
| **Topic** | Logical category for messages; divided into partitions |
| **Partition** | Ordered, immutable log; each message has an offset; unit of parallelism |
| **Consumer** | Reads messages; tracks offset; each partition read by one consumer per group |
| **Consumer Group** | Set of consumers sharing workload; enables horizontal scaling |
| **ZooKeeper/KRaft** | Manages broker metadata, leader election |

### (b) Kafka Producer & High Throughput

The producer achieves high throughput via:
1. **Batching**: Messages are buffered (`batch.size`, `linger.ms`) and sent in bulk, reducing network overhead.
2. **Compression**: Supports `gzip`, `snappy`, `lz4` — compresses batches before sending.
3. **Async Send**: By default, `send()` is asynchronous; producer doesn't wait for broker ACK.
4. **Partitioning**: If key is set, hash(key) % numPartitions routes to a fixed partition for ordering. If no key, round-robin distributes load.
5. **ACK Modes**:
   - `acks=0` → Fire and forget (fastest, no guarantee)
   - `acks=1` → Leader confirms (balanced)
   - `acks=all` → All ISR confirm (safest, slowest)

### (c) Spark Structured Streaming + Kafka Integration

```python
# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "my-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Process
parsed = df.selectExpr("CAST(value AS STRING)")

# Write with checkpointing
query = parsed.writeStream \
    .format("console") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start()
```

**Fault Tolerance Mechanism:**
- **Checkpointing**: Spark saves Kafka offsets + state to HDFS/S3 after each micro-batch.
- **Offset Tracking**: On restart, Spark reads last committed offset from checkpoint and replays from there.
- **Idempotent Sinks**: Combined with idempotent writes, guarantees **exactly-once** semantics.
- **WAL (Write-Ahead Log)**: Before processing, offsets are logged — ensures no data loss.

### (d) Partition Assignment: 8 Partitions, 4 Brokers, 3 Consumers

**Setup:** Topic has partitions P0–P7, Consumer Group has C1, C2, C3.

**Assignment (Kafka uses Range or RoundRobin assignor):**
```
C1 → P0, P1, P2  (3 partitions)
C2 → P3, P4, P5  (3 partitions)
C3 → P6, P7      (2 partitions)
```

**Rule:** Each partition is assigned to exactly ONE consumer in a group. Since 8 partitions / 3 consumers ≈ 2.67, consumers get 3, 3, and 2 partitions respectively.

**If C3 fails:**
- Kafka detects missing heartbeat (session.timeout.ms, default 10s).
- **Rebalance** is triggered.
- P6 and P7 are redistributed:
```
C1 → P0, P1, P2, P6
C2 → P3, P4, P5, P7
```
- Processing resumes from last committed offsets for P6 and P7 (no data loss).

> **💡 Depth of Understanding:**
> **Kafka vs Traditional MQ (RabbitMQ):** Kafka is a *log*, not a queue — messages are retained even after consumption (configurable retention period). This allows multiple consumer groups to independently replay the same data. **Kafka KRaft mode** (Kafka 3.3+) eliminates ZooKeeper dependency — brokers self-manage metadata using the Raft consensus algorithm, reducing operational complexity significantly.

---

## Q3: Mixed Questions [5 Marks Each]

### 3.1 Pig Latin vs SQL [5 Marks]

| Feature | Pig Latin | SQL |
|---|---|---|
| **Paradigm** | Procedural (step-by-step data flow) | Declarative (describe what, not how) |
| **Schema** | Optional (schema-on-read) | Mandatory (schema-on-write) |
| **Data Model** | Nested: Bags, Tuples, Maps | Flat relational tables |
| **Execution** | Converted to MapReduce jobs | Query optimizer decides plan |
| **Best Use** | ETL pipelines, raw data cleaning | Reporting, analytics, BI |
| **Optimization** | Manual control over pipeline | Automatic by query planner |
| **Unstructured Data** | Handles well (just load it) | Struggles without predefined schema |
| **Joins** | `JOIN A BY id, B BY id` | `SELECT ... FROM A JOIN B ON A.id=B.id` |

**Example — Find average salary per department:**

```pig
-- Pig Latin
emp = LOAD 'employees' USING PigStorage(',') AS (id, name, dept, salary);
grp = GROUP emp BY dept;
avg = FOREACH grp GENERATE group AS dept, AVG(emp.salary) AS avg_sal;
DUMP avg;
```

```sql
-- SQL
SELECT dept, AVG(salary) AS avg_sal
FROM employees
GROUP BY dept;
```

> **💡 Depth of Understanding:**
> Pig Latin's procedural nature makes debugging easier — you can inspect intermediate relations at each step (`DUMP`, `ILLUSTRATE`). However, Pig is largely obsolete today, replaced by Spark DataFrame/SQL API which provides the same procedural control with 10–100x better performance via in-memory DAG execution. HiveQL (SQL on Hadoop) has also matured significantly with Tez and LLAP.

---

### 3.2 Spark repartition(8) on 4-partition HDFS data [5 Marks]

**Scenario:** Spark reads 4-partition HDFS file → calls `repartition(8)`

**What repartition() does:**
- Triggers a **full shuffle** across the network.
- All data is redistributed evenly into 8 new partitions regardless of original partitioning.
- Uses a hash partitioner by default.

```
BEFORE repartition(8):
HDFS → [Part-0] [Part-1] [Part-2] [Part-3]  (4 tasks, ~250 MB each for 1 GB file)

Full Shuffle (network transfer):
        ↓↓↓↓↓↓↓↓↓

AFTER repartition(8):
[P0][P1][P2][P3][P4][P5][P6][P7]  (8 tasks, ~125 MB each)
```

**Performance Impact:**

| Aspect | Before (4 parts) | After repartition(8) |
|---|---|---|
| Parallelism | 4 tasks | 8 tasks |
| Task Size | ~Larger | ~Smaller (better for joins) |
| Shuffle Cost | None | **Full shuffle — expensive** |
| Use Case | Sequential reads | Parallel joins, aggregations |

**When to use `repartition` vs `coalesce`:**
- `repartition(n)`: Full shuffle, can increase OR decrease partitions, equal distribution.
- `coalesce(n)`: No shuffle (merge partitions locally), only decrease partitions, may be unequal.

> **💡 Depth of Understanding:**
> The golden rule: **repartition before wide transformations** (joins, groupBy), **coalesce before writing** output files. Spark's default parallelism is `spark.default.parallelism` (200 for shuffle ops). For a 1 TB dataset with 128 MB blocks, you get ~8192 input partitions — which is fine. Never set partitions too small (data spills to disk) or too high (too many small tasks, scheduler overhead dominates).

---

### 3.3 Social Network Graph in PySpark [5 Marks]

**Scenario:** User follow relationships (social network graph). Assume edges:
- User A → B, C
- User B → C, D  
- User C → A
- User D → B

```python
from pyspark.sql import SparkSession
from graphframes import GraphFrame

spark = SparkSession.builder.appName("SocialGraph").getOrCreate()

# Define vertices (users)
vertices = spark.createDataFrame([
    ("A", "UserA"), ("B", "UserB"),
    ("C", "UserC"), ("D", "UserD")
], ["id", "name"])

# Define edges (follows)
edges = spark.createDataFrame([
    ("A", "B", "follows"), ("A", "C", "follows"),
    ("B", "C", "follows"), ("B", "D", "follows"),
    ("C", "A", "follows"), ("D", "B", "follows")
], ["src", "dst", "relationship"])

# Create graph
g = GraphFrame(vertices, edges)

# i. In-degree (who is followed by how many)
in_deg = g.inDegrees
in_deg.show()
# Expected: A=1, B=2, C=2, D=1

# ii. Out-degree (how many does each follow)
out_deg = g.outDegrees
out_deg.show()
# Expected: A=2, B=2, C=1, D=1

# iii. Most followed user (max in-degree)
from pyspark.sql.functions import desc
most_followed = g.inDegrees.orderBy(desc("inDegree")).limit(1)
most_followed.show()
# Result: B or C (both have in-degree 2)
```

**Graph Visualization:**
```
    A ──► B ──► D
    │     │
    ▼     ▼
    C ◄───┘
    │
    └──► A  (cycle)
```

> **💡 Depth of Understanding:**
> GraphFrames is built on Spark DataFrames and uses **Pregel-style** message passing for graph algorithms. For PageRank, use `g.pageRank(resetProbability=0.15, maxIter=10)`. GraphX (RDD-based) is the older API with more low-level control. For massive graphs (billions of edges), tools like **GraphX with checkpointing** or **Presto + graph extensions** are used. In-degree is the key metric for "influence" in social networks (Twitter followers, citation counts).

---

### 3.4 Visualization Libraries for Large Dataset (e.g., Yelp Reviews) [5 Marks]

**Chosen Libraries and Justification:**

| Library | Type | Best For | Scalability |
|---|---|---|---|
| **Matplotlib / Seaborn** | Static | Quick EDA, distributions, heatmaps | Small–Medium (<100K rows) |
| **Plotly** | Interactive | Drill-down charts, dashboards | Medium (up to ~1M rows) |
| **Bokeh** | Interactive | Large streaming datasets, web apps | Medium-Large |
| **Datashader** | Server-side rendering | Billion-point scatter plots | Very Large (billions of rows) |
| **Tableau / Power BI** | BI Tool | Business dashboards, non-technical users | Large with aggregated data |

**For Yelp Reviews Dataset:**
1. **Text Data** → Word Cloud (`wordcloud` library), Topic distribution (Plotly bar charts)
2. **Rating Distribution** → Seaborn `histplot` or Plotly histogram
3. **Geographic Data** → Folium (Leaflet.js maps), Plotly `scatter_mapbox`
4. **Time Series (reviews over time)** → Plotly line chart with range slider
5. **Category Comparison** → Plotly grouped bar chart

**Scale Decision:**
- If dataset > 10M rows: aggregate with Spark first, then visualize aggregated output with Plotly.
- For raw point plotting at scale: use **Datashader** (renders server-side, sends image to browser).

> **💡 Depth of Understanding:**
> The key insight is: **never plot raw big data**. Always aggregate first using Spark/SQL, then visualize the summary. Tools like **Apache Superset** and **Grafana** connect directly to Spark SQL / Presto and run queries on the backend, making the visualization layer always lightweight regardless of underlying data size.

---

## Q4: Spark SQL & DataFrames [10+5+5 Marks]

### Q4.1 Spark SQL Queries on Customer DataFrame [10 Marks]

**Schema given:**
```
customer_id: string (nullable = true)
gender: string (nullable = true)
age: double (nullable = true)
annual_income: double (nullable = true)
spending_score: double (nullable = true)
membership_years: integer (nullable = true)
```

**Setup – Register DataFrame as temp view:**
```python
df.createOrReplaceTempView("customers")
```

---

**i. Average spending score of customers aged between 25 and 40 (inclusive)**

```python
# Spark SQL approach
result_i = spark.sql(
    "SELECT ROUND(AVG(spending_score), 2) AS avg_spending_score "
    "FROM customers "
    "WHERE age BETWEEN 25 AND 40"
)
result_i.show()

# DataFrame API equivalent
from pyspark.sql.functions import avg, round as spark_round
df.filter((df.age >= 25) & (df.age <= 40)) \
  .agg(spark_round(avg("spending_score"), 2).alias("avg_spending_score")) \
  .show()
```

---

**ii. Maximum annual income among customers with membership > 5 years**

```python
# Spark SQL approach
result_ii = spark.sql(
    "SELECT MAX(annual_income) AS max_annual_income "
    "FROM customers "
    "WHERE membership_years > 5"
)
result_ii.show()

# DataFrame API equivalent
from pyspark.sql.functions import max as spark_max
df.filter(df.membership_years > 5) \
  .agg(spark_max("annual_income").alias("max_annual_income")) \
  .show()
```

---

**iii. Percentage of female customers whose spending score is above 70**

```python
# Spark SQL approach
result_iii = spark.sql(
    "SELECT ROUND( "
    "  SUM(CASE WHEN gender = 'Female' AND spending_score > 70 THEN 1 ELSE 0 END) "
    "  * 100.0 / COUNT(*), 2) AS female_high_spender_pct "
    "FROM customers"
)
result_iii.show()

# DataFrame API equivalent
from pyspark.sql.functions import col, when, sum as spark_sum
total = df.count()
df.agg(
    spark_round(
        spark_sum(
            when((col("gender") == "Female") & (col("spending_score") > 70), 1).otherwise(0)
        ) * 100.0 / total,
        2
    ).alias("female_high_spender_pct")
).show()
```

> **💡 Depth of Understanding:**
> `BETWEEN` in Spark SQL is **inclusive** on both ends (25 <= age <= 40). The `SUM(CASE WHEN...)` pattern for filtered percentages is more efficient than nested subqueries — it scans the table only once (single pass). In PySpark, `when(condition, value).otherwise(0)` is the CASE WHEN equivalent. Use `createOrReplaceTempView` (session-scoped, auto-cleaned) over `createOrReplaceGlobalTempView` (app-scoped) for clean isolation in multi-user environments.

---

### Q4.2 Spark Aggregate & Window Functions [5 Marks]

**Standard GroupBy Aggregations:**

```python
from pyspark.sql.functions import avg, max, min, count, round as spark_round

df.groupBy("gender").agg(
    spark_round(avg("spending_score"), 2).alias("avg_score"),
    spark_round(avg("annual_income"), 2).alias("avg_income"),
    count("*").alias("total_customers"),
    max("age").alias("max_age"),
    min("membership_years").alias("min_membership")
).show()
```

**Window Functions – LAG, LEAD, ROW_NUMBER:**

```python
from pyspark.sql.functions import lag, lead, row_number, avg as w_avg
from pyspark.sql.window import Window

# Partition by gender, order by spending_score ascending
w = Window.partitionBy("gender").orderBy("spending_score")

df_windowed = df \
    .withColumn("prev_score",     lag("spending_score", 1).over(w)) \
    .withColumn("next_score",     lead("spending_score", 1).over(w)) \
    .withColumn("rank_in_gender", row_number().over(w)) \
    .withColumn("running_avg",    spark_round(w_avg("spending_score").over(w), 2))

df_windowed.select(
    "customer_id", "gender", "spending_score",
    "prev_score", "next_score", "rank_in_gender", "running_avg"
).show()
```

**Summary of Key Functions:**

| Function | Type | Description |
|---|---|---|
| `groupBy().agg()` | Aggregation | Collapses N rows → 1 row per group |
| `lag(col, n)` | Window | Value from n rows BEFORE in window |
| `lead(col, n)` | Window | Value from n rows AFTER in window |
| `row_number()` | Window | Sequential rank within partition, no ties |
| `rank()` | Window | Rank with gaps on ties |
| `dense_rank()` | Window | Rank without gaps on ties |
| `avg().over(w)` | Window | Running/rolling average |
| `round(col, n)` | Scalar | Round to n decimal places |

> **💡 Depth of Understanding:**
> The critical distinction: `groupBy()` **collapses** N rows → 1 aggregate row per group (destroys original rows). Window functions **ADD a new column** to each existing row without reducing row count. This is essential for ranking within groups, moving averages, and comparing each row to its predecessor — very common in time-series and financial analytics. `Window.rowsBetween(-6, 0)` defines a 7-row rolling frame; `Window.rangeBetween` works on actual column values (e.g., date ranges) rather than row counts.

---

### Q4.3 Spark Persistence Strategies [5 Marks]

Persistence avoids recomputing expensive operations when a DataFrame or RDD is accessed multiple times.

```python
from pyspark import StorageLevel

# Option 1: cache() — shorthand for MEMORY_AND_DISK
df.cache()

# Option 2: persist() with explicit storage level
df.persist(StorageLevel.MEMORY_ONLY)           # Fastest; evicts partitions if OOM
df.persist(StorageLevel.MEMORY_AND_DISK)       # Default; spills to disk if OOM
df.persist(StorageLevel.DISK_ONLY)             # All on disk; slowest access
df.persist(StorageLevel.MEMORY_ONLY_SER)       # Serialized in memory (smaller, slower)
df.persist(StorageLevel.MEMORY_AND_DISK_SER)   # Serialized + disk spill
df.persist(StorageLevel.OFF_HEAP)              # Avoids JVM GC pressure

# IMPORTANT: Persistence is LAZY — triggered on first action
df.persist()
df.count()   # <-- This triggers actual caching

# Release memory when done
df.unpersist()
```

**Storage Level Comparison:**

| Level | Memory | Disk | Serialized | Best For |
|---|---|---|---|---|
| `MEMORY_ONLY` | ✅ | ❌ | ❌ | Small datasets, max speed |
| `MEMORY_AND_DISK` | ✅ | ✅ (spill) | ❌ | General purpose (recommended) |
| `DISK_ONLY` | ❌ | ✅ | ✅ | Very large, rarely reaccessed |
| `MEMORY_ONLY_SER` | ✅ | ❌ | ✅ | Memory-constrained, CPU available |
| `OFF_HEAP` | ✅ (native) | ❌ | ✅ | Long-running jobs, GC problems |

**When to Persist:**
1. DataFrame used in **multiple actions** (count, write, show in sequence)
2. **Iterative ML algorithms** — each pass re-reads same training data
3. After **expensive joins/aggregations** used as inputs to further transforms
4. **Streaming stateful ops** that reference historical accumulated data

> **💡 Depth of Understanding:**
> **Persistence ≠ Checkpointing.** `cache()` stores data but preserves full lineage (DAG) — if a cached partition is lost (node failure), Spark recomputes it using lineage. `checkpoint()` **truncates the lineage** and saves to HDFS — essential for long-running streaming jobs where the DAG grows unboundedly and recomputation from origin would be prohibitively expensive. Rule of thumb: use `cache()` for batch, `checkpoint()` for streaming state, and `OFF_HEAP` when GC pauses are causing performance issues in ML workloads.

---

## Q5-A: PageRank Algorithm – One Iteration [10 Marks]

### Graph Definition

**Pages:** A, B, C, D (N = 4 total pages), **Damping factor d = 0.85**

**Directed links:**
- A → B, C &nbsp; (out-degree = 2)
- B → C &nbsp;&nbsp;&nbsp; (out-degree = 1)
- C → A &nbsp;&nbsp;&nbsp; (out-degree = 1)
- D → A &nbsp;&nbsp;&nbsp; (out-degree = 1)

```
              ┌─────────────────┐
              │                 ▼
    D ───────►A ──────► B ────► C
              ▲                 │
              └─────────────────┘

  Incoming links: A←{C,D}  B←{A}  C←{A,B}  D←{none}
```

---

### PageRank Formula

```
PR(p) = (1 - d) / N  +  d × Σ [ PR(q) / OutDegree(q) ]
                              q→p

Constants:  d = 0.85,  N = 4
            (1-d)/N = 0.15 / 4 = 0.0375
```

---

### Initialization — Iteration 0

All pages start with equal rank:
```
PR₀(A) = PR₀(B) = PR₀(C) = PR₀(D) = 1/4 = 0.25
```

---

### Iteration 1 — Step-by-Step Calculations

**PR₁(A)** — receives from C (out=1) and D (out=1):
```
PR₁(A) = 0.0375 + 0.85 × [ 0.25/1 + 0.25/1 ]
        = 0.0375 + 0.85 × 0.50
        = 0.0375 + 0.4250
        = 0.4625
```

**PR₁(B)** — receives from A (out=2):
```
PR₁(B) = 0.0375 + 0.85 × [ 0.25/2 ]
        = 0.0375 + 0.85 × 0.125
        = 0.0375 + 0.10625
        = 0.14375
```

**PR₁(C)** — receives from A (out=2) and B (out=1):
```
PR₁(C) = 0.0375 + 0.85 × [ 0.25/2 + 0.25/1 ]
        = 0.0375 + 0.85 × [ 0.125 + 0.25 ]
        = 0.0375 + 0.85 × 0.375
        = 0.0375 + 0.31875
        = 0.35625
```

**PR₁(D)** — no incoming links:
```
PR₁(D) = 0.0375 + 0.85 × 0
        = 0.0375
```

---

### Results After Iteration 1

| Page | PR₀ (Initial) | PR₁ (After iter 1) | Δ Change | Rank |
|---|---|---|---|---|
| A | 0.2500 | **0.4625** | +0.2125 | 🥇 1st |
| C | 0.2500 | **0.3563** | +0.1063 | 🥈 2nd |
| B | 0.2500 | 0.1438 | −0.1063 | 🥉 3rd |
| D | 0.2500 | **0.0375** | −0.2125 | 4th |
| **Sum** | **1.0000** | **1.0000** | — | ✅ |

**Verification:** 0.4625 + 0.14375 + 0.35625 + 0.0375 = **1.0** ✓

---

### Convergence

Further iterations continue until all changes are negligible:
```
Convergence condition: max |PR_n(p) - PR_{n-1}(p)| < ε   (e.g., ε = 0.0001)
```
Small graphs typically converge in **10–50 iterations**.

**Intuition:** A ranks highest because two pages (C and D) each dedicate their FULL outgoing rank to A — concentrated endorsement. D ranks lowest because no page links to it; it only receives the random teleportation baseline (0.0375).

> **💡 Depth of Understanding:**
> The **damping factor (0.85)** models a random surfer who follows links 85% of the time and teleports to a random page 15% of the time — preventing rank drain into dead-ends or cycles. The **dangling node problem** (pages with no outgoing links) creates rank sinks; solutions include redistributing their rank uniformly to all pages or removing them pre-computation. In Spark GraphX: `graph.pageRank(tol=0.0001, resetProbability=0.15)`. Real-world PageRank runs on graphs with billions of nodes using Google's Pregel system. The algorithm also underlies citation analysis (academic papers), biological protein-interaction networks, and financial fraud detection (finding central nodes in transaction graphs).

---

## Q5-B Option 1: Distributed Real-Time Streaming with Spark [10 Marks]

### Message Passing in Distributed Streaming Systems

Components communicate via **message passing** through a broker — producers publish events; consumers subscribe and process asynchronously. This decouples sources from processors, enabling independent scaling.

```
PIPELINE ARCHITECTURE:

[Data Sources]       [Broker Layer]         [Processing]        [Sinks]
                                                                
Web Clicks   ──►                           ┌──────────────┐
App Events   ──►  [Kafka Cluster]    ──►   │ Spark SS DAG │ ──► Database
IoT Sensors  ──►  Partitioned &            │ Micro-batching│ ──► Dashboard
Social Feed  ──►  Replicated               └──────────────┘ ──► Alerts
```

### Real-World Example: Spam Detection Pipeline

**Scenario:** Emails stream in → classify spam/ham → quarantine spam in real-time.

```
DAG Flow:
[Kafka: email-stream]
        │
        ▼
[Parse & Decode JSON]  ──► extract subject, body, sender, timestamp
        │
        ▼
[Feature Extraction]   ──► TF-IDF vectors, sender reputation score
        │
        ▼
[ML Classifier: Naive Bayes / Random Forest]
        │
   ┌────┴───────────┐
   ▼                ▼
[SPAM]          [HAM]
   │                │
   ▼                ▼
[Quarantine]   [Inbox Delivery]
[Kafka: spam-log]
```

**PySpark Structured Streaming sketch:**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count, udf
from pyspark.sql.types import StructType, StringType, TimestampType

spark = SparkSession.builder.appName("SpamDetector").getOrCreate()

schema = StructType() \
    .add("email_id", StringType()) \
    .add("sender",   StringType()) \
    .add("subject",  StringType()) \
    .add("body",     TimestampType())

# Ingest from Kafka
raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "email-stream") \
    .load()

emails = raw.select(
    from_json(col("value").cast("string"), schema).alias("d")
).select("d.*")

# Simple spam classifier UDF (replace with real ML model)
spam_detect = udf(
    lambda s, b: "SPAM" if any(w in (s+b).lower()
                 for w in ["free", "win", "click", "prize"]) else "HAM",
    StringType()
)
classified = emails.withColumn("label", spam_detect(col("subject"), col("body")))

# Windowed aggregation — count spam vs ham per 5-minute window
windowed = classified.groupBy(
    window(col("timestamp"), "5 minutes"),
    col("label")
).agg(count("*").alias("count"))

windowed.writeStream \
    .format("console") \
    .option("checkpointLocation", "/checkpoint/spam") \
    .outputMode("update") \
    .start() \
    .awaitTermination()
```

### How Scalability is Achieved

| Mechanism | How It Scales |
|---|---|
| **Kafka Partitions** | More partitions = more parallel Spark tasks |
| **Spark Executors** | Add worker nodes → near-linear throughput increase |
| **Micro-batch Tuning** | Adjust trigger interval (100ms–10s) for latency/throughput trade-off |
| **Dynamic Allocation** | Spark auto-scales executors based on input backlog |
| **RocksDB State Store** | Handles TB-scale stateful windowed operations |
| **Checkpointing** | Fault-tolerant recovery without full reprocessing |

> **💡 Depth of Understanding:**
> Spark Structured Streaming uses **micro-batching** — it buffers incoming data for a short interval then processes as a batch. Apache **Flink** uses true event-by-event streaming (sub-millisecond latency) — better for trading systems or real-time fraud detection. The **Lambda Architecture** runs parallel batch + speed layers (complex, two codebases); the **Kappa Architecture** uses only streaming (simpler, single codebase). Modern teams prefer Kappa with Spark Structured Streaming or Flink. The **Kafka → Spark → Delta Lake** pattern ("Medallion Architecture": Bronze → Silver → Gold layers) is the current industry standard for building scalable, reliable data pipelines.

---

## Q5-B Option 2: MongoDB CRUD – Hospital Management [10 Marks]

### Collection Document Structure

```json
{
  "_id": "P567",
  "name": "Ravi Sharma",
  "age": 45,
  "diagnosis": ["IHD"],
  "status": "active",
  "last_visit": "2024-03-20"
}
```

### Complete CRUD Operations

```python
from pymongo import MongoClient
from datetime import datetime, timedelta

client   = MongoClient("mongodb://localhost:27017/")
db       = client["hospital_db"]
patients = db["patients"]

# ── i. INSERT – New patient record ──────────────────────────────────
new_patient = {
    "_id"      : "P568",
    "name"     : "Priya Patel",
    "age"      : 32,
    "diagnosis": ["Diabetes", "Hypertension"],
    "status"   : "active",
    "last_visit": "2025-04-15"
}
result = patients.insert_one(new_patient)
print(f"Inserted: {result.inserted_id}")

# ── ii. UPDATE – Mark inactive if not visited in > 1 year ───────────
one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

update_result = patients.update_many(
    filter={"last_visit": {"$lt": one_year_ago}},
    update={"$set": {"status": "Inactive"}}
)
print(f"Marked {update_result.modified_count} patients as Inactive")

# ── iii. DELETE – Remove records with last_visit before 2023 ─────────
delete_result = patients.delete_many(
    {"last_visit": {"$lt": "2023-01-01"}}
)
print(f"Deleted {delete_result.deleted_count} old records")

# ── iv. FIND – Active patients who visited in last 6 months ──────────
six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

active_recent = patients.find(
    filter={"status": "active", "last_visit": {"$gte": six_months_ago}},
    projection={"_id": 1, "name": 1, "age": 1, "last_visit": 1}
)

print("Active patients (last 6 months):")
for p in active_recent:
    print(p)
```

### MongoDB Query Operators Reference

| Operator | Meaning | Example |
|---|---|---|
| `$lt` | Less than | `{"last_visit": {"$lt": "2023-01-01"}}` |
| `$lte` | Less than or equal | `{"age": {"$lte": 60}}` |
| `$gt` | Greater than | `{"age": {"$gt": 18}}` |
| `$gte` | Greater than or equal | `{"last_visit": {"$gte": date}}` |
| `$in` | In list | `{"diagnosis": {"$in": ["IHD"]}}` |
| `$set` | Set field value | `{"$set": {"status": "Inactive"}}` |
| `$push` | Add item to array | `{"$push": {"diagnosis": "Fever"}}` |
| `$pull` | Remove from array | `{"$pull": {"diagnosis": "Fever"}}` |

### Performance Indexes

```python
# Create indexes for fields used in filters
patients.create_index("last_visit")
patients.create_index("status")
patients.create_index([("status", 1), ("last_visit", -1)])  # compound index
```

### Why MongoDB for Hospital Records?

| Feature | MongoDB Advantage |
|---|---|
| **Flexible Schema** | Each patient can have different diagnosis arrays |
| **Embedded Documents** | Medical history inside patient doc — no JOINs needed |
| **Horizontal Scaling** | Sharding distributes records across nodes |
| **Schema Evolution** | Add new field without altering existing documents |
| **Change Streams** | Real-time triggers when patient status changes |

> **💡 Depth of Understanding:**
> MongoDB stores data as **BSON** (Binary JSON) — a superset of JSON adding types like Date, ObjectId, Binary. The `_id` field is auto-indexed and serves as primary key. In production hospital systems, compliance with **HIPAA (USA)** or **DPDP Act (India)** requires field-level encryption for PII — MongoDB offers **Client-Side Field Level Encryption (CSFLE)** for this. **Change Streams** enable real-time triggers: when a patient status changes to "critical", an alert fires automatically. **TTL indexes** auto-expire old records: `create_index("last_visit", expireAfterSeconds=94608000)` enforces a 3-year retention policy automatically. For analytics on MongoDB data at scale, use the **MongoDB Spark Connector** to pull collections directly into Spark DataFrames.

---

## 📋 Quick Revision Table

| Q | Key Answer / Formula |
|---|---|
| **Q1-A** | 3Vs: Volume (IoT scale), Velocity (real-time traffic), Variety (CSV+JSON+video) |
| **Q1-B** | 8,192 blocks × 3 replicas = **3 TB total**; Pipeline replication; Heartbeat=3s |
| **Q2a** | Kafka = Producer → Broker(Topic/Partitions) → Consumer Group |
| **Q2d** | 8 parts / 3 consumers = 3,3,2; Rebalance on consumer failure |
| **Q3.1** | Pig = procedural ETL (step-by-step); SQL = declarative analytics |
| **Q3.2** | `repartition` = full shuffle; `coalesce` = no shuffle, reduce only |
| **Q3.3** | `g.inDegrees` = followers; `g.outDegrees` = following; most followed = max inDegree |
| **Q4.1** | BETWEEN inclusive; `SUM(CASE WHEN)` for single-pass filtered percentage |
| **Q4.2** | `lag`=prev row; `lead`=next row; window functions ADD column, don't collapse |
| **Q4.3** | `cache()` is lazy; `MEMORY_AND_DISK` is default; `checkpoint()` truncates lineage |
| **Q5-A** | PR(A)=**0.4625**, PR(C)=0.3563, PR(B)=0.1438, PR(D)=0.0375; Sum=1.0 ✓ |
| **Q5-B1** | Kafka→Spark Streaming DAG→Sinks; scalable via partitions+executors |
| **Q5-B2** | `insert_one`, `update_many($set)`, `delete_many($lt)`, `find(projection)` |

---
*BDA PYQ May 2025 – Complete Solutions | Pandit Deendayal Energy University*
