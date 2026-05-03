# PageRank Assignment – Complete Solutions
**Big Data Analytics (BDA) | Assignment — PageRank Algorithm**
**Source: 101computing.net — Page Rank Algorithm Quiz**

---

## 📚 Theory: The PageRank Formula (Simplified)

PageRank was developed by **Larry Page and Sergey Brin** (Google founders) to rank web pages by importance.

### Core Idea
> A page is important if many important pages link to it.

### Simplified Formula (Used in This Assignment)

```
PR(page) = Σ [ PR(inlink) / OutDegree(inlink) ]
            for each page linking TO this page
```

**In plain English:**
- Look at every page that links **to** your page.
- Each linking page "donates" a fraction of its own PageRank.
- The fraction = `PR(linker) / number of outgoing links from that linker`.
- Sum all such donations = your PageRank.

### Full Google Formula (For Exam Reference)

```
PR(p) = (1 - d) / N  +  d × Σ [ PR(q) / OutDegree(q) ]
                             q→p

Where:
  d = damping factor (typically 0.85)
  N = total number of pages
  (1-d)/N = baseline "random teleportation" score
```

> **💡 Note:** The quiz problems below use the **simplified formula** (no damping factor). Exam problems may use the full formula with `d = 0.85`.

---

## Quiz #1: Find PageRank of Page B

### Question
Given the following directed web graph, find the **PageRank score of web page B**.

### Graph Structure

```
     A ─────────────────► B
     │ (PR: 12)           ▲  (PR: ??)
     │                    │
     │        ┌───────────┤
     ▼        │           │
     D ───────┘           │
     ▲        │           │
     │        ▼           │
     │        E ──────────┘
     │
     │
     C ─────► A
(PR: 10)  
     │
     └──────► D
```

**Given Values:**
| Node | PageRank | Out-Degree | Outgoing Links |
|------|----------|------------|----------------|
| A    | **12** (given) | 2 | A → B, A → D |
| C    | **10** (given) | 2 | C → A, C → D |
| D    | Unknown  | 2 | D → B, D → E |
| E    | Unknown  | 1 | E → B |
| B    | **??**   | 0 | (dead end) |

### Directed Edges (Adjacency List)
```
C → A       C → D
A → B       A → D
D → B       D → E
E → B
```

---

### Step-by-Step Solution

We need to compute PR values in **dependency order** — start from nodes whose PR we already know, then work forward.

#### Step 1: Compute PR(D)

**Who links to D?** → A and C

```
PR(D) = PR(A) / Out(A)  +  PR(C) / Out(C)
      =   12   /   2     +    10  /   2
      =       6           +       5
      = 11
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| A → D  | PR(A) / Out(A) = 12 / 2 | **6** |
| C → D  | PR(C) / Out(C) = 10 / 2 | **5** |
| **Total** | | **PR(D) = 11** |

---

#### Step 2: Compute PR(E)

**Who links to E?** → Only D

```
PR(E) = PR(D) / Out(D)
      =   11  /   2
      = 5.5
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| D → E  | PR(D) / Out(D) = 11 / 2 | **5.5** |
| **Total** | | **PR(E) = 5.5** |

---

#### Step 3: Compute PR(B) ← THE ANSWER

**Who links to B?** → A, D, and E

```
PR(B) = PR(A) / Out(A)  +  PR(D) / Out(D)  +  PR(E) / Out(E)
      =   12  /   2      +    11  /   2      +   5.5  /   1
      =       6           +       5.5         +       5.5
      = 17
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| A → B  | PR(A) / Out(A) = 12 / 2 | **6** |
| D → B  | PR(D) / Out(D) = 11 / 2 | **5.5** |
| E → B  | PR(E) / Out(E) = 5.5 / 1 | **5.5** |
| **Total** | | **PR(B) = 17** |

### ✅ Answer: PR(B) = 17

---

## Quiz #2: Find PageRank of Page B (6 Nodes)

### Question
Given the following directed web graph with 6 nodes, find the **PageRank score of web page B**.

### Graph Structure

```
     A ─────────────────► B
     │ (PR: 12)           ▲  (PR: ??)
     │                    │
     ▼                    │
     D ──────► E ─────────┘
     ▲
     │
     C ──────► A
(PR: 12)
     │
     ├──────► D
     │
     └──────► F ──────► D
```

**Given Values:**
| Node | PageRank | Out-Degree | Outgoing Links |
|------|----------|------------|----------------|
| A    | **12** (given) | 2 | A → B, A → D |
| C    | **12** (given) | 3 | C → A, C → D, C → F |
| D    | Unknown  | 1 | D → E |
| E    | Unknown  | 1 | E → B |
| F    | Unknown  | 1 | F → D |
| B    | **??**   | 0 | (dead end) |

### Directed Edges (Adjacency List)
```
C → A       C → D       C → F
A → B       A → D
F → D
D → E
E → B
```

---

### Step-by-Step Solution

#### Step 1: Compute PR(F)

**Who links to F?** → Only C

```
PR(F) = PR(C) / Out(C)
      =   12  /   3
      = 4
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| C → F  | PR(C) / Out(C) = 12 / 3 | **4** |
| **Total** | | **PR(F) = 4** |

---

#### Step 2: Compute PR(D)

**Who links to D?** → A, C, and F

```
PR(D) = PR(A) / Out(A)  +  PR(C) / Out(C)  +  PR(F) / Out(F)
      =   12  /   2      +    12  /   3      +    4   /   1
      =       6           +       4           +       4
      = 14
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| A → D  | PR(A) / Out(A) = 12 / 2 | **6** |
| C → D  | PR(C) / Out(C) = 12 / 3 | **4** |
| F → D  | PR(F) / Out(F) = 4 / 1  | **4** |
| **Total** | | **PR(D) = 14** |

---

#### Step 3: Compute PR(E)

**Who links to E?** → Only D

```
PR(E) = PR(D) / Out(D)
      =   14  /   1
      = 14
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| D → E  | PR(D) / Out(D) = 14 / 1 | **14** |
| **Total** | | **PR(E) = 14** |

---

#### Step 4: Compute PR(B) ← THE ANSWER

**Who links to B?** → A and E

```
PR(B) = PR(A) / Out(A)  +  PR(E) / Out(E)
      =   12  /   2      +    14  /   1
      =       6           +       14
      = 20
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| A → B  | PR(A) / Out(A) = 12 / 2 | **6** |
| E → B  | PR(E) / Out(E) = 14 / 1 | **14** |
| **Total** | | **PR(B) = 20** |

### ✅ Answer: PR(B) = 20

> **💡 Key Observation:** Even though D has **three** incoming links (from A, C, and F), all of D's rank flows through a single outgoing link to E, which then flows entirely to B. This funneling effect amplifies B's score.

---

## Quiz #3: Find PageRank of Page A

### Question
Given the following directed web graph with 6 nodes, find the **PageRank score of web page A**.

### Graph Structure

```
     A ◄─────────────── B
     ▲  (PR: ??)        ▲  
     │                  │
     │                  ├──── E ◄──── C (PR: 12)
     │                  │              │
     D ◄──── C          └──── F ◄─────┘
                                       │
                                       └──► D
```

More precisely:

```
              C (PR: 12)
            / | \
           ▼  ▼  ▼
          D   E   F
          │   │   │
          ▼   ▼   ▼
          A   B   B
              ▲   
              │
          B ──► A
```

**Given Values:**
| Node | PageRank | Out-Degree | Outgoing Links |
|------|----------|------------|----------------|
| C    | **12** (given) | 3 | C → D, C → E, C → F |
| D    | Unknown  | 1 | D → A |
| E    | Unknown  | 1 | E → B |
| F    | Unknown  | 1 | F → B |
| B    | Unknown  | 1 | B → A |
| A    | **??**   | 0 | (dead end) |

### Directed Edges (Adjacency List)
```
C → D       C → E       C → F
D → A
E → B
F → B
B → A
```

---

### Step-by-Step Solution

#### Step 1: Compute PR(D), PR(E), PR(F)

All three receive from C equally (C has out-degree 3):

```
PR(D) = PR(C) / Out(C) = 12 / 3 = 4
PR(E) = PR(C) / Out(C) = 12 / 3 = 4
PR(F) = PR(C) / Out(C) = 12 / 3 = 4
```

| Node | Source | Formula | Value |
|------|--------|---------|-------|
| D | C → D | 12 / 3 | **4** |
| E | C → E | 12 / 3 | **4** |
| F | C → F | 12 / 3 | **4** |

---

#### Step 2: Compute PR(B)

**Who links to B?** → E and F

```
PR(B) = PR(E) / Out(E)  +  PR(F) / Out(F)
      =    4  /   1      +    4   /   1
      =       4           +       4
      = 8
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| E → B  | PR(E) / Out(E) = 4 / 1 | **4** |
| F → B  | PR(F) / Out(F) = 4 / 1 | **4** |
| **Total** | | **PR(B) = 8** |

---

#### Step 3: Compute PR(A) ← THE ANSWER

**Who links to A?** → D and B

```
PR(A) = PR(D) / Out(D)  +  PR(B) / Out(B)
      =    4  /   1      +    8   /   1
      =       4           +       8
      = 12
```

| Source | Contribution Formula | Value |
|--------|---------------------|-------|
| D → A  | PR(D) / Out(D) = 4 / 1 | **4** |
| B → A  | PR(B) / Out(B) = 8 / 1 | **8** |
| **Total** | | **PR(A) = 12** |

### ✅ Answer: PR(A) = 12

> **💡 Key Observation:** Interesting result — PR(A) = PR(C) = 12! This happens because ALL of C's rank eventually flows to A through two paths:
> - Path 1: C → D → A (contributes 4)
> - Path 2: C → E → B → A (contributes 4)
> - Path 3: C → F → B → A (contributes 4)
> - Total: 4 + 4 + 4 = 12 = PR(C) — **full rank conservation!**

---

## 📊 Summary of All Answers

| Quiz | Target Node | Answer | Key Strategy |
|------|------------|--------|--------------|
| Quiz #1 | PR(B) | **17** | Compute D first, then E, then B (3 incoming links) |
| Quiz #2 | PR(B) | **20** | Compute F → D → E → B (funnel effect amplifies rank) |
| Quiz #3 | PR(A) | **12** | Compute D,E,F → B → A (full rank conservation from C) |

---

## 🎯 Exam Quick-Reference: PageRank Problem-Solving Workflow

```
1. Draw the directed graph clearly
2. Identify all KNOWN PageRank values (given in problem)
3. For each node, list:
   - Incoming links (who links TO this node)
   - Out-degree of each linker
4. Compute in DEPENDENCY ORDER:
   - Start with nodes whose ALL incoming sources have KNOWN PR
   - Work forward until you reach the target node
5. For each node:  PR(X) = Σ [ PR(source) / Out(source) ]
6. Verify: if it's a closed system, total PR should be conserved
```

> **💡 Depth of Understanding:**
> In the simplified model (no damping factor), PageRank is purely a **flow conservation** problem — rank flows along edges, splitting equally among outgoing links. In the real Google model with damping factor `d = 0.85`, every node also receives a small baseline `(1-d)/N` representing a "random teleportation" probability. This prevents dead-end nodes (no outlinks) from absorbing all rank into a black hole. The damping factor models a random web surfer who follows links 85% of the time and jumps to a random page 15% of the time.
