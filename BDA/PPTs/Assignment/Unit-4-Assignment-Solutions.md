# Unit 4 Assignment – Complete Solutions (Assignment-3)
**Big Data Analytics (BDA) | Apache Spark Calculations**
**7 Detailed Calculation Questions**

---

## 📚 Key Formulas Reference

| Concept | Formula |
|---------|---------|
| **Spark Partitions** | `⌈Data Size / HDFS Block Size⌉` |
| **Parallel Tasks** | `min(Partitions, Total Executor Cores)` |
| **Total Executors** | `⌊(Total Cores - Driver Cores) / Cores Per Executor⌋` |
| **Usable Memory** | `Executor Memory × spark.memory.fraction` |
| **Storage Memory** | `Usable Memory × spark.memory.storageFraction` |
| **Execution Memory** | `Usable Memory − Storage Memory` |
| **Job Time** | `⌈Total Tasks / Parallel Cores⌉ × Time Per Task` |

---

## Q1: Spark Partitions & Parallel Tasks

### Question
An RDD has a data size of **1.2 GB** stored in HDFS with a block size of **128 MB**. Calculate the **number of partitions** created by Spark. If an executor has **4 cores**, how many **tasks can run in parallel**?

### Solution

#### Part A: Number of Partitions

```
Step 1: Convert data size to MB
    Data Size = 1.2 GB = 1.2 × 1024 = 1228.8 MB

Step 2: Calculate partitions (= number of HDFS blocks)
    Partitions = ⌈Data Size / Block Size⌉
               = ⌈1228.8 / 128⌉
               = ⌈9.6⌉
               = 10 partitions
```

> **Why?** Spark creates **one partition per HDFS block** by default when reading from HDFS. Since the 1.2 GB file is split into 10 blocks (9 full + 1 partial), Spark creates 10 partitions.

#### Part B: Parallel Tasks

```
Parallel Tasks = Number of Executor Cores = 4
```

> **Why?** Each core processes one partition at a time. With 4 cores and 10 partitions:
> - **Wave 1**: Core 1→P1, Core 2→P2, Core 3→P3, Core 4→P4
> - **Wave 2**: Core 1→P5, Core 2→P6, Core 3→P7, Core 4→P8
> - **Wave 3**: Core 1→P9, Core 2→P10 (2 cores idle)
> - Total waves: ⌈10/4⌉ = 3

### ✅ Answers

| Metric | Value |
|--------|-------|
| Data Size | 1.2 GB = 1228.8 MB |
| Block Size | 128 MB |
| **Number of Partitions** | **10** |
| Executor Cores | 4 |
| **Parallel Tasks** | **4** (at any given time) |

```
Timeline of task execution:

    Core 1: ████ P1 ████ P5 ████ P9
    Core 2: ████ P2 ████ P6 ████ P10
    Core 3: ████ P3 ████ P7 ░░░░ idle
    Core 4: ████ P4 ████ P8 ░░░░ idle
            ─────────────────────────►
            Wave 1   Wave 2   Wave 3
```

> **💡 Key Insight:** If you had 10+ cores, all 10 partitions would execute simultaneously in a single wave. The optimal setup is `cores ≥ partitions` for maximum parallelism. Use `repartition()` to increase partitions if you have more cores than partitions.

---

## Q2: Total Executors & Parallel Tasks in a Cluster

### Question
A Spark cluster has **5 worker nodes** with **16 cores per node**. If the driver uses **2 cores** and each executor is configured with **4 cores**, calculate the **total number of executors** and the **number of parallel tasks**.

### Solution

#### Step 1: Total Available Cores

```
Total Cluster Cores = 5 nodes × 16 cores/node = 80 cores

Cores Available for Executors = Total Cores − Driver Cores
                              = 80 − 2
                              = 78 cores
```

#### Step 2: Number of Executors

```
Total Executors = ⌊Available Cores / Cores Per Executor⌋
                = ⌊78 / 4⌋
                = 19 executors

(Remaining 78 - 19×4 = 78 - 76 = 2 cores are unused)
```

#### Step 3: Parallel Tasks

```
Parallel Tasks = Total Executors × Cores Per Executor
               = 19 × 4
               = 76 tasks
```

### ✅ Answers

| Metric | Value |
|--------|-------|
| Worker Nodes | 5 |
| Cores per Node | 16 |
| Total Cluster Cores | 80 |
| Driver Cores | 2 |
| Available Cores | 78 |
| Cores per Executor | 4 |
| **Total Executors** | **19** |
| **Parallel Tasks** | **76** |

```
Cluster Layout:

    Node 1 (16 cores): [Exec1: 4c] [Exec2: 4c] [Exec3: 4c] [Exec4: 4c]
    Node 2 (16 cores): [Exec5: 4c] [Exec6: 4c] [Exec7: 4c] [Exec8: 4c]
    Node 3 (16 cores): [Exec9: 4c] [Exec10:4c] [Exec11:4c] [Exec12:4c]
    Node 4 (16 cores): [Exec13:4c] [Exec14:4c] [Exec15:4c] [Exec16:4c]
    Node 5 (16 cores): [Driver:2c] [Exec17:4c] [Exec18:4c] [Exec19:4c] [2c unused]

    Total: 19 executors × 4 cores = 76 parallel tasks
```

> **💡 Key Insight:** The driver is typically placed on one of the worker nodes (in cluster mode) or on the submitting machine (in client mode). In practice, you'd also leave 1 core per node for OS/YARN overhead, giving `5×15 - 2 = 73 cores → 18 executors = 72 parallel tasks`. But this question asks for the direct calculation.

---

## Q3: Spark Memory Architecture

### Question
An executor is allocated **10 GB** of memory. If `spark.memory.fraction` is **0.6** and `spark.memory.storageFraction` is **0.5**, calculate the **usable memory**, **storage memory**, and **execution memory**.

### Solution

#### Spark Memory Model

```
┌──────────────────────────────────────────────┐
│           Executor Memory: 10 GB             │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Reserved Memory: 300 MB (fixed)       │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  User Memory (1 - fraction):           │  │
│  │  = (10 GB - 300 MB) × 0.4 = 3.88 GB   │  │
│  │  (UDFs, data structures, metadata)     │  │
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │  Usable (Unified) Memory:              │  │
│  │  = (10 GB - 300 MB) × 0.6 = 5.82 GB   │  │
│  │                                        │  │
│  │  ┌──────────────┬─────────────────┐    │  │
│  │  │  Storage     │   Execution     │    │  │
│  │  │  Memory      │   Memory        │    │  │
│  │  │  50%         │   50%           │    │  │
│  │  │  = 2.91 GB   │   = 2.91 GB     │    │  │
│  │  └──────────────┴─────────────────┘    │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

#### Detailed Calculation

```
Step 1: Usable Memory (for Spark's unified memory pool)
    Usable Memory = (Executor Memory − Reserved) × spark.memory.fraction
                  = (10 GB − 300 MB) × 0.6
                  = 9.7 GB × 0.6
                  ≈ 5.82 GB

    Simplified (ignoring 300 MB reserved — as per exam convention):
    Usable Memory = 10 GB × 0.6 = 6 GB

Step 2: Storage Memory
    Storage Memory = Usable Memory × spark.memory.storageFraction
                   = 6 GB × 0.5
                   = 3 GB

Step 3: Execution Memory
    Execution Memory = Usable Memory − Storage Memory
                     = 6 GB − 3 GB
                     = 3 GB
```

### ✅ Answers

| Memory Region | Formula | Value (Simplified) | Value (Exact) |
|---------------|---------|-------------------|---------------|
| Executor Total | Given | 10 GB | 10 GB |
| Reserved | Fixed | — | 300 MB |
| **Usable Memory** | `Total × 0.6` | **6 GB** | **5.82 GB** |
| **Storage Memory** | `Usable × 0.5` | **3 GB** | **2.91 GB** |
| **Execution Memory** | `Usable − Storage` | **3 GB** | **2.91 GB** |

> **💡 Key Insight — Unified Memory Management (Spark 1.6+):**
> - Storage and Execution memory share a **unified pool**. The boundary is **soft** — either side can borrow from the other!
> - If execution needs more memory and storage has free space → execution borrows from storage.
> - If storage needs more and execution has free space → storage borrows from execution.
> - However, execution can **evict** storage (cached data), but storage **cannot evict** execution (active computation).
> - `spark.memory.storageFraction = 0.5` is the **initial split**, not a hard boundary.

---

## Q4: Data Per Mapper & Reducer

### Question
A Spark job processes **600 GB** of input data using **300 mappers** and **100 reducers**. Calculate the **amount of data processed by each mapper** and **each reducer**.

### Solution

```
Step 1: Data per Mapper
    Data per Mapper = Total Input Data / Number of Mappers
                    = 600 GB / 300
                    = 2 GB per mapper

Step 2: Data per Reducer
    Data per Reducer = Total Input Data / Number of Reducers
                     = 600 GB / 100
                     = 6 GB per reducer
```

### ✅ Answers

| Metric | Value |
|--------|-------|
| Total Input Data | 600 GB |
| Number of Mappers | 300 |
| Number of Reducers | 100 |
| **Data per Mapper** | **600 / 300 = 2 GB** |
| **Data per Reducer** | **600 / 100 = 6 GB** |

```
Data Flow Visualization:

    INPUT (600 GB)
        │
        ▼
    ┌─── 300 Mappers ───┐
    │ M1: 2 GB → process │
    │ M2: 2 GB → process │   Each mapper handles
    │ M3: 2 GB → process │   an equal 2 GB slice
    │ ...                │
    │ M300: 2 GB         │
    └────────┬───────────┘
             │ SHUFFLE
             ▼
    ┌─── 100 Reducers ──┐
    │ R1: 6 GB → reduce  │
    │ R2: 6 GB → reduce  │   Each reducer aggregates
    │ R3: 6 GB → reduce  │   data from all mappers
    │ ...                │   for its key range
    │ R100: 6 GB         │
    └────────────────────┘
```

> **💡 Key Insight:** The reducer data is **not simply a division** of input data in real scenarios. During shuffle:
> - Each mapper partitions its output by key (using hash partitioner).
> - Data volume at reducers depends on key distribution — skewed keys cause **data skew** where one reducer gets far more data than others.
> - The question assumes **uniform distribution** for simplicity.
> - In practice, 6 GB per reducer is quite large — you might want more reducers to reduce per-task memory pressure.

---

## Q5: Job Execution Time Estimation

### Question
A Spark job consists of **200 tasks**. Each task takes **5 seconds** to execute, and the cluster has **10 executor cores**. Estimate the **total job execution time**.

### Solution

```
Step 1: Calculate number of waves
    Waves = ⌈Total Tasks / Parallel Cores⌉
          = ⌈200 / 10⌉
          = 20 waves

Step 2: Calculate total execution time
    Total Time = Waves × Time Per Task
               = 20 × 5 seconds
               = 100 seconds
```

### ✅ Answer

| Metric | Value |
|--------|-------|
| Total Tasks | 200 |
| Time per Task | 5 seconds |
| Executor Cores | 10 |
| Number of Waves | ⌈200/10⌉ = 20 |
| **Total Execution Time** | **20 × 5 = 100 seconds** |

```
Execution Timeline:

    Core 1:  [T1 5s][T11 5s][T21 5s]...[T191 5s]   ← 20 tasks
    Core 2:  [T2 5s][T12 5s][T22 5s]...[T192 5s]   ← 20 tasks
    Core 3:  [T3 5s][T13 5s][T23 5s]...[T193 5s]   ← 20 tasks
    ...
    Core 10: [T10 5s][T20 5s][T30 5s]...[T200 5s]  ← 20 tasks
             ─────────────────────────────────────►
                         100 seconds total
                    (20 waves × 5 sec/wave)
```

> **💡 Key Insight:** This is an **ideal estimate** assuming:
> - All tasks take exactly 5 seconds (no stragglers).
> - No scheduling overhead between waves.
> - No shuffle/network delays.
>
> In reality, **speculative execution** (`spark.speculation=true`) handles straggler tasks by launching duplicate copies. Also, task scheduling adds ~10-50ms overhead per task. For 200 tasks with 10 cores, the real time might be ~105-110 seconds accounting for overhead.

---

## Q6: Data Copies & Fault Tolerance

### Question
A dataset is divided into **8 partitions** with a replication factor of **2**. Calculate the **total number of data copies** and explain whether the job can continue if **one copy of a partition fails**.

### Solution

#### Part A: Total Data Copies

```
Total Data Copies = Number of Partitions × Replication Factor
                  = 8 × 2
                  = 16 copies
```

#### Part B: Fault Tolerance Analysis

**Yes, the job CAN continue if one copy of a partition fails.**

```
Example: Partition P3 has 2 copies

    Before failure:
        P3-Copy1 (Node A) ← PRIMARY
        P3-Copy2 (Node B) ← REPLICA

    After P3-Copy1 fails (Node A crashes):
        P3-Copy1 (Node A) ← ❌ DEAD
        P3-Copy2 (Node B) ← ✅ USED FOR COMPUTATION

    Spark reads P3 from Node B and continues processing.
```

### ✅ Answers

| Metric | Value |
|--------|-------|
| Partitions | 8 |
| Replication Factor | 2 |
| **Total Data Copies** | **16** |
| **Survives 1 copy failure?** | **Yes ✅** |

> **💡 Detailed Explanation — Spark's Fault Tolerance:**
>
> Spark has **two layers** of fault tolerance:
>
> 1. **HDFS Replication**: With RF=2, each block exists on 2 nodes. If one node fails, Spark reads from the surviving replica. This is what this question refers to.
>
> 2. **RDD Lineage**: Even if ALL copies of a partition are lost, Spark can **recompute** it from the original data using the DAG lineage graph. This is Spark's fundamental fault-tolerance mechanism — it doesn't need replication at the RDD level because it remembers HOW to recreate any lost partition.
>
> ```
> Lineage Graph:
>     textFile("data.txt")     ← Source: HDFS blocks
>         │
>         ▼
>     .filter(line.contains("error"))
>         │
>         ▼
>     .map(line → (word, 1))   ← If this partition is lost,
>         │                       Spark re-reads the HDFS block
>         ▼                       and re-applies filter + map
>     .reduceByKey(_ + _)
> ```
>
> So even with RF=1, Spark can recover — it just needs to re-read and recompute, which is slower than reading a replica.

---

## Q7: Data Locality & Execution Time

### Question
Out of **120 tasks**, **90 are data-local tasks** taking **3 seconds each** and **30 are non-local tasks** taking **6 seconds each**. Calculate the **total execution time** and the **approximate execution time if the cluster has 8 cores**.

### Solution

#### Part A: Total CPU Execution Time (Sequential)

```
Total Time = (Data-Local Tasks × Time per Local Task) + (Non-Local Tasks × Time per Non-Local Task)
           = (90 × 3 seconds) + (30 × 6 seconds)
           = 270 seconds + 180 seconds
           = 450 seconds
```

#### Part B: Approximate Wall-Clock Time with 8 Cores

```
Step 1: Total number of tasks = 120

Step 2: Number of waves
    Waves = ⌈120 / 8⌉ = 15 waves

Step 3: Average time per task
    Average Task Time = Total CPU Time / Total Tasks
                      = 450 / 120
                      = 3.75 seconds per task

Step 4: Approximate wall-clock time
    Wall-Clock Time ≈ Waves × Average Task Time
                    = 15 × 3.75
                    = 56.25 seconds
```

### ✅ Answers

| Metric | Value |
|--------|-------|
| Data-Local Tasks | 90 × 3s = **270s** |
| Non-Local Tasks | 30 × 6s = **180s** |
| **Total CPU Time** | **450 seconds** |
| Cluster Cores | 8 |
| Waves | ⌈120/8⌉ = 15 |
| Average Task Time | 450/120 = 3.75s |
| **Approx Wall-Clock Time** | **≈ 56.25 seconds** |

```
Task Distribution (simplified):

    Local tasks (90):     ████ 3s each ████████████████████████
    Non-local tasks (30): ████████ 6s each ████████████████████

    With 8 cores:
    Core 1: [L 3s][L 3s][L 3s]...[NL 6s]...
    Core 2: [L 3s][L 3s][L 3s]...[NL 6s]...
    ...
    Core 8: [L 3s][L 3s][L 3s]...[NL 6s]...
            ──────────────────────────────►
                   ~56.25 seconds
```

> **💡 Key Insight — Data Locality Levels in Spark:**
>
> | Level | Name | Latency | Description |
> |-------|------|---------|-------------|
> | 1 | `PROCESS_LOCAL` | Fastest | Data in same JVM (cached) |
> | 2 | `NODE_LOCAL` | Fast | Data on same node, different process |
> | 3 | `RACK_LOCAL` | Medium | Data on same rack, different node |
> | 4 | `ANY` | Slowest | Data on remote rack (network transfer) |
>
> Spark waits `spark.locality.wait` (default 3s) for a data-local slot before falling back to non-local. The 2× slowdown for non-local tasks (6s vs 3s) is realistic — network transfer adds significant overhead.
>
> **Optimization:** If you see many non-local tasks, either:
> 1. Increase `spark.locality.wait` to give Spark more time to find local slots
> 2. Add more nodes to improve data distribution
> 3. Use `repartition()` to redistribute data closer to computation

---

## 📊 Quick Answer Sheet

| Q# | Topic | Key Answers |
|----|-------|-------------|
| 1 | Partitions & Parallel Tasks | **10 partitions**, **4 parallel tasks** |
| 2 | Executors & Tasks | **19 executors**, **76 parallel tasks** |
| 3 | Memory Architecture | **Usable: 6 GB**, **Storage: 3 GB**, **Execution: 3 GB** |
| 4 | Data per Mapper/Reducer | **Mapper: 2 GB**, **Reducer: 6 GB** |
| 5 | Job Execution Time | **100 seconds** (20 waves × 5s) |
| 6 | Replication & Fault Tolerance | **16 copies**, **Yes — job continues** |
| 7 | Data Locality Execution | **Total: 450s**, **With 8 cores: ~56.25s** |

---

## 🎯 Exam Quick-Reference: Spark Calculation Patterns

```
1. PARTITIONS:    ⌈DataSize / BlockSize⌉
2. EXECUTORS:     ⌊AvailableCores / CoresPerExecutor⌋
3. PARALLEL:      Executors × CoresPerExecutor (or just total cores)
4. WAVES:         ⌈Tasks / ParallelCores⌉
5. TIME:          Waves × TimePerTask
6. MEMORY:        Total × fraction → split by storageFraction
7. REPLICATION:   Partitions × RF = total copies
```

> **💡 Common Exam Traps:**
> - Always use **ceiling** (⌈⌉) for partitions/blocks/waves — partial blocks still count!
> - Always use **floor** (⌊⌋) for executors — you can't have a fractional executor.
> - Don't forget to subtract driver cores from total cluster cores.
> - Memory calculations may or may not include the 300 MB reserved — check the question context.
> - Replication is at the **HDFS level**, not the Spark RDD level. Spark relies on lineage for RDD fault tolerance.
