# Unit 3 Assignment – Complete Solutions (Assignment-2)
**Big Data Analytics (BDA) | HDFS & MapReduce Calculations**
**10 MCQ Questions with Detailed Explanations**

---

## 📚 Key Formulas Reference

| Concept | Formula |
|---------|---------|
| **Number of Blocks** | `⌈File Size / Block Size⌉` |
| **Total Blocks (with replication)** | `Number of Blocks × Replication Factor` |
| **Physical Disk Space** | `Logical File Size × Replication Factor` |
| **Unique Logical Blocks** | `Total Physical Blocks / Replication Factor` |
| **NameNode RAM** | `Number of Blocks × Metadata Per Block (≈150 bytes)` |
| **Map Tasks** | `= Number of Input Splits ≈ Number of Blocks` |
| **Shuffle Operations** | `Number of Mappers × Number of Reducers` |
| **Min DataNodes** | `⌈Total Physical Storage / Storage Per Node⌉` |

---

## Q1: HDFS Block Count with Replication

### Question
An HDFS block size is **128 MB**. A file of size **640 MB** is stored with replication factor **3**. How many **total blocks** are stored in HDFS?

**Options:** a. 5 &nbsp;&nbsp; b. 10 &nbsp;&nbsp; c. 15 &nbsp;&nbsp; d. 20

### Solution

```
Step 1: Calculate logical blocks
    Logical Blocks = ⌈File Size / Block Size⌉
                   = ⌈640 MB / 128 MB⌉
                   = ⌈5⌉
                   = 5 blocks

Step 2: Apply replication factor
    Total Blocks = Logical Blocks × Replication Factor
                 = 5 × 3
                 = 15 blocks
```

### ✅ Answer: **(c) 15**

| Metric | Value |
|--------|-------|
| File Size | 640 MB |
| Block Size | 128 MB |
| Logical Blocks | 5 |
| Replication Factor | 3 |
| **Total Physical Blocks** | **15** |

> **💡 Explanation:** Each 128 MB block is replicated 3 times across different DataNodes for fault tolerance. HDFS stores **3 copies** of every block. So 5 unique blocks × 3 replicas = 15 total blocks stored in the cluster.

---

## Q2: Actual Disk Space with Replication

### Question
If HDFS replication factor is **3**, and a file occupies **2 GB** logical space, what is the **actual disk space** used?

**Options:** a. 2 GB &nbsp;&nbsp; b. 4 GB &nbsp;&nbsp; c. 6 GB &nbsp;&nbsp; d. 8 GB

### Solution

```
Actual Disk Space = Logical File Size × Replication Factor
                  = 2 GB × 3
                  = 6 GB
```

### ✅ Answer: **(c) 6 GB**

| Metric | Value |
|--------|-------|
| Logical File Size | 2 GB |
| Replication Factor | 3 |
| **Actual Disk Space** | **6 GB** |

> **💡 Explanation:** Replication is a simple multiplier on storage. The trade-off is **storage efficiency vs. fault tolerance**. With RF=3, you use 3× storage but can tolerate the failure of any 2 copies of each block. This is why real clusters use compression (Snappy, LZ4) and erasure coding (HDFS 3.x) to reduce overhead while maintaining reliability.

---

## Q3: Unique Logical Blocks in a Cluster

### Question
An HDFS cluster has **12 DataNodes**, each storing **100 blocks**. Replication factor is **3**. How many **unique logical blocks** are stored?

**Options:** a. 400 &nbsp;&nbsp; b. 1200 &nbsp;&nbsp; c. 300 &nbsp;&nbsp; d. 3600

### Solution

```
Step 1: Calculate total physical blocks across all DataNodes
    Total Physical Blocks = 12 DataNodes × 100 blocks/node
                          = 1200 blocks

Step 2: Calculate unique logical blocks
    Unique Logical Blocks = Total Physical Blocks / Replication Factor
                          = 1200 / 3
                          = 400 blocks
```

### ✅ Answer: **(a) 400**

| Metric | Value |
|--------|-------|
| DataNodes | 12 |
| Blocks per Node | 100 |
| Total Physical Blocks | 1,200 |
| Replication Factor | 3 |
| **Unique Logical Blocks** | **400** |

> **💡 Explanation:** Think of it in reverse — each unique file block exists in 3 copies spread across the cluster. So the 1200 physical blocks stored across all nodes actually represent only 400 distinct data blocks. The NameNode's metadata tracks these 400 unique blocks and their 3 replica locations each.

---

## Q4: Rack Failure Probability

### Question
If one rack contains **5 DataNodes** out of **10 total racks**, and data is stored across **2 racks**, what is the probability both racks fail if **5 racks fail**?

**Options:** a. 0.25 &nbsp;&nbsp; b. 0.5 &nbsp;&nbsp; c. 0.1 &nbsp;&nbsp; d. 0.75

### Solution

This is a **combinatorics / hypergeometric probability** problem.

```
Given:
  - Total racks = 10
  - Data is stored on 2 specific racks
  - 5 racks fail randomly
  - Find: P(both data racks are among the 5 failed racks)

Method: Use combinations

P(both fail) = C(2,2) × C(8,3) / C(10,5)

Where:
  C(2,2) = ways to choose both data racks from the 2 data racks = 1
  C(8,3) = ways to choose remaining 3 failed racks from 8 non-data racks
  C(10,5) = total ways to choose 5 failed racks from 10

Calculation:
  C(2,2) = 1
  C(8,3) = 8! / (3! × 5!) = (8 × 7 × 6) / (3 × 2 × 1) = 336 / 6 = 56
  C(10,5) = 10! / (5! × 5!) = 252

  P(both fail) = (1 × 56) / 252
               = 56 / 252
               = 0.2222...
               ≈ 0.22
```

### ✅ Answer: **(a) 0.25** (closest approximation among the options)

> **💡 Explanation:** The exact probability is 2/9 ≈ 0.222, but among the given options, **0.25** is the closest. Another way to think about it: P(1st data rack fails) = 5/10 = 0.5, then P(2nd data rack also fails | 1st already failed) = 4/9 ≈ 0.44. Combined: 0.5 × 0.44 = 0.222. This demonstrates why HDFS uses **rack-awareness** — by placing replicas on different racks, data survives even if an entire rack goes down.

---

## Q5: NameNode RAM Requirement

### Question
NameNode metadata consumes **150 bytes per block**. If HDFS stores **2 million blocks**, how much RAM is required?

**Options:** a. 150 MB &nbsp;&nbsp; b. 300 MB &nbsp;&nbsp; c. 450 MB &nbsp;&nbsp; d. 600 MB

### Solution

```
RAM Required = Number of Blocks × Metadata Per Block
             = 2,000,000 × 150 bytes
             = 300,000,000 bytes

Convert to MB:
             = 300,000,000 / (1000 × 1000)     [using SI/decimal MB]
             = 300 MB

    OR       = 300,000,000 / (1024 × 1024)      [using binary MiB]
             ≈ 286.1 MiB
```

### ✅ Answer: **(b) 300 MB**

| Metric | Value |
|--------|-------|
| Blocks | 2,000,000 |
| Metadata per Block | 150 bytes |
| Total Metadata | 300,000,000 bytes |
| **RAM Required** | **≈ 300 MB** |

> **💡 Explanation:** This is the critical **NameNode memory bottleneck**. ALL metadata lives in RAM for fast lookups. This means:
> - 10 million blocks → 1.5 GB RAM
> - 100 million blocks → 15 GB RAM
> - 1 billion blocks → 150 GB RAM (impractical!)
>
> This is why HDFS has a **small files problem** — millions of tiny files each consume 150 bytes of NameNode RAM regardless of file size. Solutions: HAR files, SequenceFiles, or HDFS Federation (multiple NameNodes, each managing a namespace partition).

---

## Q6: Total Blocks (Non-Exact Division)

### Question
File size **1.2 GB**, block size **128 MB**, replication **2**. Total blocks?

**Options:** a. 10 &nbsp;&nbsp; b. 18 &nbsp;&nbsp; c. 20 &nbsp;&nbsp; d. 24

### Solution

```
Step 1: Convert file size to MB
    File Size = 1.2 GB = 1.2 × 1024 MB = 1228.8 MB

Step 2: Calculate logical blocks (ceiling division!)
    Logical Blocks = ⌈1228.8 / 128⌉
                   = ⌈9.6⌉
                   = 10 blocks

    Why 10? The last block is only partially filled:
    - 9 full blocks × 128 MB = 1152 MB
    - 1 partial block = 1228.8 - 1152 = 76.8 MB
    - HDFS still allocates a block for this remainder

Step 3: Apply replication factor
    Total Blocks = 10 × 2 = 20
```

### ✅ Answer: **(c) 20**

| Metric | Value |
|--------|-------|
| File Size | 1.2 GB = 1228.8 MB |
| Block Size | 128 MB |
| Logical Blocks | ⌈9.6⌉ = **10** |
| Replication Factor | 2 |
| **Total Physical Blocks** | **20** |

> **💡 Explanation:** HDFS always uses **ceiling division** — even if the last block is only partially filled (76.8 MB out of 128 MB), it still counts as one block. However, the actual disk space used by the partial block is only 76.8 MB, NOT 128 MB. HDFS doesn't waste the remaining 51.2 MB — the block is stored at its actual data size.

---

## Q7: MapReduce Map Tasks

### Question
**640 MB** file, **128 MB** block → how many **map tasks**?

**Options:** a. 4 &nbsp;&nbsp; b. 5 &nbsp;&nbsp; c. 6 &nbsp;&nbsp; d. 10

### Solution

```
Number of Input Splits ≈ Number of Blocks = ⌈File Size / Block Size⌉

Map Tasks = ⌈640 / 128⌉
          = ⌈5.0⌉
          = 5
```

### ✅ Answer: **(b) 5**

> **💡 Explanation:** In MapReduce, **one map task is created per input split**, and by default each input split corresponds to one HDFS block. So:
> - Block 1 (0–128 MB) → Map Task 1
> - Block 2 (128–256 MB) → Map Task 2
> - Block 3 (256–384 MB) → Map Task 3
> - Block 4 (384–512 MB) → Map Task 4
> - Block 5 (512–640 MB) → Map Task 5
>
> This is the principle of **data locality** — each mapper ideally runs on the same node where its block is stored, avoiding network transfer.

---

## Q8: Reducer Execution Time

### Question
Reducer takes **8 seconds per key**, **200 keys** → total time?

**Options:** a. 800s &nbsp;&nbsp; b. 1200s &nbsp;&nbsp; c. 1600s &nbsp;&nbsp; d. 2000s

### Solution

```
Total Time = Time Per Key × Number of Keys
           = 8 seconds × 200 keys
           = 1600 seconds
```

### ✅ Answer: **(c) 1600s**

| Metric | Value |
|--------|-------|
| Time per Key | 8 seconds |
| Number of Keys | 200 |
| **Total Reducer Time** | **1600 seconds** |

> **💡 Explanation:** This assumes a **single reducer** processing all 200 keys sequentially. In practice, you'd configure multiple reducers to parallelize:
> - With 4 reducers: each handles ~50 keys → ~400s per reducer → total wall-clock ≈ 400s
> - With 10 reducers: each handles ~20 keys → ~160s per reducer → total wall-clock ≈ 160s
>
> The number of reducers is configurable via `mapreduce.job.reduces`. However, the total **CPU time** remains 1600s regardless of parallelism.

---

## Q9: Shuffle Operations Count

### Question
**12 mappers** & **4 reducers** → how many **shuffle operations**?

**Options:** a. 12 &nbsp;&nbsp; b. 16 &nbsp;&nbsp; c. 48 &nbsp;&nbsp; d. 4

### Solution

```
Shuffle Operations = Number of Mappers × Number of Reducers
                   = 12 × 4
                   = 48
```

### ✅ Answer: **(c) 48**

| Metric | Value |
|--------|-------|
| Mappers | 12 |
| Reducers | 4 |
| **Shuffle Operations** | **48** |

> **💡 Explanation:** During the **shuffle phase**, each mapper's output must be partitioned and sent to the correct reducer. With 12 mappers and 4 reducers:
> - Mapper 1 sends data to Reducer 1, 2, 3, 4 → 4 connections
> - Mapper 2 sends data to Reducer 1, 2, 3, 4 → 4 connections
> - ... (repeat for all 12 mappers)
> - Total: 12 × 4 = **48 shuffle connections**
>
> This is why the shuffle phase is the **most expensive** part of MapReduce — it involves network I/O, disk I/O (sorting), and memory. Minimizing shuffle data (using combiners, map-side aggregation) is the #1 performance optimization technique.

```
         Mappers                    Reducers
    ┌─────────────┐           ┌──────────────┐
    │  M1  ───────┼──── × ───►│   R1         │
    │  M2  ───────┼──── × ───►│   R2         │
    │  M3  ───────┼──── × ───►│   R3         │
    │  ...        │           │   R4         │
    │  M12 ───────┼──── × ───►│              │
    └─────────────┘           └──────────────┘
     Each mapper connects       = 12 × 4
     to ALL reducers            = 48 shuffles
```

---

## Q10: Minimum DataNodes for Large Dataset

### Question
An HDFS cluster uses a **256 MB** block size with replication factor **3**. A dataset of **10 TB** is stored. Each DataNode has **8 TB** usable space. How many **minimum DataNodes** are required to store the dataset safely?

**Options:** a. 4 &nbsp;&nbsp; b. 6 &nbsp;&nbsp; c. 8 &nbsp;&nbsp; d. 10

### Solution

```
Step 1: Calculate total physical storage needed
    Physical Storage = Dataset Size × Replication Factor
                     = 10 TB × 3
                     = 30 TB

Step 2: Calculate minimum DataNodes
    Minimum DataNodes = ⌈Physical Storage / Storage Per Node⌉
                      = ⌈30 TB / 8 TB⌉
                      = ⌈3.75⌉
                      = 4 DataNodes
```

### ✅ Answer: **(a) 4**

| Metric | Value |
|--------|-------|
| Dataset Size | 10 TB |
| Block Size | 256 MB |
| Replication Factor | 3 |
| Total Physical Storage | 30 TB |
| Storage per DataNode | 8 TB |
| **Minimum DataNodes** | **⌈30/8⌉ = 4** |

> **⚠️ Important Caveat:** While mathematically 4 nodes suffice (4 × 8 TB = 32 TB > 30 TB), in practice you'd need **more nodes** because:
> 1. **Replication constraint**: With RF=3, you need **at least 3 DataNodes** (each replica on a different node). 4 satisfies this.
> 2. **Rack awareness**: Ideally spread across 2+ racks for rack-failure tolerance.
> 3. **Headroom**: Production clusters keep 20–30% free space for rebalancing, intermediate shuffle data, and new data ingestion.
> 4. **Performance**: More nodes = more parallel I/O = faster reads/writes.

---

## 📊 Quick Answer Sheet

| Q# | Topic | Answer | Key Formula |
|----|-------|--------|-------------|
| 1 | Block count + replication | **(c) 15** | 5 blocks × 3 = 15 |
| 2 | Disk space with replication | **(c) 6 GB** | 2 GB × 3 = 6 GB |
| 3 | Unique logical blocks | **(a) 400** | 1200 / 3 = 400 |
| 4 | Rack failure probability | **(a) 0.25** | C(2,2)×C(8,3)/C(10,5) ≈ 0.22 |
| 5 | NameNode RAM | **(b) 300 MB** | 2M × 150 bytes = 300 MB |
| 6 | Blocks (non-exact division) | **(c) 20** | ⌈9.6⌉ × 2 = 20 |
| 7 | Map tasks | **(b) 5** | ⌈640/128⌉ = 5 |
| 8 | Reducer time | **(c) 1600s** | 8s × 200 = 1600s |
| 9 | Shuffle operations | **(c) 48** | 12 × 4 = 48 |
| 10 | Minimum DataNodes | **(a) 4** | ⌈30/8⌉ = 4 |
