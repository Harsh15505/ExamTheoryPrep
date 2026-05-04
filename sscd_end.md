# SSCD End-Semester Solutions

---

## Q-1(a) Can the back-end of a compiler be the same for different programming languages? (04 Marks)

**Yes.** A compiler is divided into two logical parts:

| Part | Responsibility |
|------|---------------|
| **Front-end** | Lexical, syntax, semantic analysis, IR generation (language-dependent) |
| **Back-end** | Code optimization, target code generation (machine-dependent) |

```
  ┌─────────────┐       ┌──────────────────────────────────┐
  │  C Source    │──► C Front-End ──┐                       │
  ├─────────────┤                  │    ┌──────────────┐    │
  │  C++ Source  │──► C++ Front-End┼──►│  Common IR    │──►│ Shared Back-End │──► Machine Code
  ├─────────────┤                  │    │(3-Addr Code) │    │  (Optimizer +   │
  │ Fortran Src  │──► Fortran FE ──┘    └──────────────┘    │   Code Gen)     │
  └─────────────┘                                           └─────────────────┘
```

**Justification:**
- Front-end produces a **language-independent IR** (e.g., three-address code, AST).
- Back-end takes this IR → target machine code. Since IR is **language-independent**, same back-end works for all languages.
- **Example:** GCC shares back-end for C, C++, Fortran. LLVM's back-end is shared by Clang, Rust, Swift.
- Reduces **M × N** problem to **M + N** components (retargetable compiler design).

---

## Q-1(b) DFA using Syntax Tree Method for: `c*d⁺(c|d)*e#` (08 Marks)

### Step 1: Rewrite

`d⁺ = dd*` → RE becomes: `c*·d·d*·(c|d)*·e·#`

### Step 2: Leaf positions

| Pos | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|-----|---|---|---|---|---|---|---|
| Sym | c | d | d | c | d | e | # |

### Step 3: Syntax Tree

```
                              ·₁₄ (root)
                           ╱        ╲
                        ·₁₃          #₇
                      ╱      ╲
                   ·₁₂        e₆
                 ╱      ╲
              ·₁₁       *₁₀
             ╱    ╲       │
           ·₉     *₈    |₉
          ╱  ╲     │    ╱  ╲
        *₇   d₂   d₃  c₄   d₅
         │
        c₁
```

### Nullable / Firstpos / Lastpos

| Node | nullable | firstpos | lastpos |
|------|:--------:|----------|---------|
| c₁ | F | {1} | {1} |
| c₁* | **T** | {1} | {1} |
| d₂ | F | {2} | {2} |
| c₁*·d₂ | F | **{1,2}** | {2} |
| d₃ | F | {3} | {3} |
| d₃* | **T** | {3} | {3} |
| (c₁*·d₂)·d₃* | F | {1,2} | **{2,3}** |
| c₄\|d₅ | F | {4,5} | {4,5} |
| (c₄\|d₅)* | **T** | {4,5} | {4,5} |
| ···(c₄\|d₅)* | F | {1,2} | **{2,3,4,5}** |
| ····e₆ | F | {1,2} | {6} |
| root | F | **{1,2}** | **{7}** |

### Step 4: Followpos

| Pos | Sym | followpos | Derivation |
|-----|-----|-----------|------------|
| 1 | c | **{1, 2}** | c₁* loop→{1}; cat to d₂→{2} |
| 2 | d | **{3, 4, 5, 6}** | cat→{3}; cat→{4,5}; cat→{6} |
| 3 | d | **{3, 4, 5, 6}** | d₃* loop→{3}; cat→{4,5}; cat→{6} |
| 4 | c | **{4, 5, 6}** | (c\|d)* loop→{4,5}; cat→{6} |
| 5 | d | **{4, 5, 6}** | (c\|d)* loop→{4,5}; cat→{6} |
| 6 | e | **{7}** | cat→{7} |
| 7 | # | **∅** | end |

### Step 5: DFA Construction

Start = firstpos(root) = **{1, 2}**

| State | Set | On `c` | On `d` | On `e` |
|:-----:|-----|:------:|:------:|:------:|
| **A** | {1, 2} | A | B | — |
| **B** | {3, 4, 5, 6} | C | B | D |
| **C** | {4, 5, 6} | C | C | D |
| **D★** | {7} | — | — | — |

### DFA Diagram

```
                 c                d
          ┌──────────┐    ┌──────────┐
          │          │    │          │
          ▼          │    ▼          │
        ╔═══╗  d   ╔═══╗       c   ╔═══╗
  ───►  ║ A ║─────►║ B ║─────────►║ C ║
        ╚═══╝      ╚═══╝          ╚═══╝
                     │  │           │  ▲
                     │  │    c,d    │  │
                     │  │    ┌──────┘  │
                     │  │    └─────────┘
                   e │  │          e │
                     │  │            │
                     ▼  │            ▼
                   ╔═════════╗ ◄─────┘
                   ║  D (✓)  ║
                   ╚═════════╝

  Start: A     Accept: D
```

---

## Q-1(b) OR — DFA using Subset Construction for: `(x | y*) x*yz#` (08 Marks)

### Step 1: NFA (Thompson's Construction)

```
                    ┌─── x ───►(2)───ε──┐
                    │                    │
  ──►(0)───ε──►(1)─┤                    ├──►(5)──ε──►(6)
        │           │    ┌──ε──┐        │         │
        │           └─ε─►(3)─y►(4)─ε──►┘         │
        │                └─ε──────────►(5)        │
        └─────────────────────────────────────────┘
                                          │
                        ┌──ε──┐           │
                        │     ▼           ▼
                       (7)◄─x─(6)──ε──►(8)──y──►(9)──z──►((10))
```

### Step 2: Subset Construction Table

| DFA State | NFA ε-closure | On x | On y | On z |
|:---------:|--------------|:----:|:----:|:----:|
| **A** (start) | {0,1,3,5,6,8} | B | C | — |
| **B** | {2,5,6,7,8} | B | D | — |
| **C** | {3,4,5,6,8} | B | C | — |
| **D** | {9} | — | — | E |
| **E★** | {10} | — | — | — |

### DFA Diagram

```
          x         x           y         z
    ┌──────────┐  ┌───┐  ┌──────────┐  ┌──────────┐
    │          ▼  │   ▼  │          ▼  │          ▼
  ╔═══╗  x  ╔═══╗   ╔═══╗       ╔═══╗      ╔══════╗
  ║ A ║────►║ B ║   ║ C ║       ║ D ║─────►║ E(✓) ║
  ╚═══╝     ╚═══╝   ╚═══╝       ╚═══╝   z  ╚══════╝
    │  y      │ y      ▲
    └────────►└───────►│
              │        │
              │   x    │
              └────►(B)│
                       │
    A──y──►C──y──►C    │
    C──x──►B           │
```

**Cleaner version:**
```
           ┌──x──┐
           │     │
           ▼     │
  ──►(A)──x──►(B)├──y──►(D)──z──►((E))
       │         │
       y    x◄───┘
       │   │
       ▼   │
      (C)──┘
       ▲ │
       └y┘
```

---

## Q-2(a) LL(1) Parsing Table (07 Marks)

**Grammar:**
```
Program  → Section EOF        Section  → Command Section | ε
Command  → Loop | Print | Assign
Loop     → REPEAT num TIMES { Section }
Print    → SHOW text          Assign   → var : num
```

### FIRST & FOLLOW

| Non-terminal | FIRST | FOLLOW |
|-------------|-------|--------|
| Program | {REPEAT, SHOW, var, EOF} | {$} |
| Section | {REPEAT, SHOW, var, ε} | {EOF, }} |
| Command | {REPEAT, SHOW, var} | {REPEAT, SHOW, var, EOF, }} |
| Loop | {REPEAT} | {REPEAT, SHOW, var, EOF, }} |
| Print | {SHOW} | {REPEAT, SHOW, var, EOF, }} |
| Assign | {var} | {REPEAT, SHOW, var, EOF, }} |

### LL(1) Table

| | REPEAT | SHOW | var | EOF | } |
|---|---|---|---|---|---|
| **Program** | Sec EOF | Sec EOF | Sec EOF | Sec EOF | |
| **Section** | Cmd Sec | Cmd Sec | Cmd Sec | ε | ε |
| **Command** | Loop | Print | Assign | | |
| **Loop** | REPEAT num TIMES { Sec } | | | | |
| **Print** | | SHOW text | | | |
| **Assign** | | | var : num | | |

**No conflicts** → Grammar is **LL(1)** ✓

---

## Q-2(b) Parse Tree for `(id % (id + id * id)) ^ id ^ id` (04 Marks)

**Grammar** (precedence low→high: +,- < *,/,% < ^):
```
E → E + T | T       T → T * F | T % F | F
F → P ^ F | P       P → ( E ) | id
```

Note: `^` is **right-associative** via `F → P ^ F`

### Parse Tree

```
  E
  └── T
      └── F
          ├── P
          │   ├── (
          │   ├── E
          │   │   └── T
          │   │       ├── T
          │   │       │   └── F
          │   │       │       └── P
          │   │       │           └── id₁
          │   │       ├── %
          │   │       └── F
          │   │           └── P
          │   │               ├── (
          │   │               ├── E
          │   │               │   ├── E
          │   │               │   │   └── T
          │   │               │   │       └── F
          │   │               │   │           └── P
          │   │               │   │               └── id₂
          │   │               │   ├── +
          │   │               │   └── T
          │   │               │       ├── T
          │   │               │       │   └── F
          │   │               │       │       └── P
          │   │               │       │           └── id₃
          │   │               │       ├── *
          │   │               │       └── F
          │   │               │           └── P
          │   │               │               └── id₄
          │   │               └── )
          │   └── )
          ├── ^
          └── F  ◄── (right-associative)
              ├── P
              │   └── id₅
              ├── ^
              └── F
                  └── P
                      └── id₆
```

---

## Q-2(b) OR — Left Factored Grammar (04 Marks)

**Original:**
```
S → aSSbS | aSaSb | adb | bAa | d
A → a | ab
```

**Step 1:** Factor `a` from S:
```
S  → aS' | bAa | d
S' → SSbS | SaSb | db
```

**Step 2:** Factor `S` from S':
```
S' → SS'' | db
S'' → SbS | aSb
```

**Step 3:** Factor `a` from A:
```
A → aA'       A' → ε | b
```

### ✅ Final Left-Factored Grammar
```
S   → a S' | b A a | d
S'  → S S'' | d b
S'' → S b S | a S b
A   → a A'
A'  → ε | b
```

---

## Q-2(c) SDT — Octal to Decimal + Parse Tree for (126)₈ (07 Marks)

### SDT Rules
```
N → N₁ D    { N.val = N₁.val × 8 + D.val }
N → D       { N.val = D.val }
D → 0|1|…|7 { D.val = digit }
```

### Annotated Parse Tree for (126)₈

```
                N  ─── val = 86
              ╱   ╲
            N       D ─── val = 6
         val=10     │
          ╱  ╲      6
        N      D ─── val = 2
     val=1     │
        │      2
        D ─── val = 1
        │
        1
```

### Bottom-Up Evaluation

| Step | Rule Applied | Computation | Result |
|:----:|-------------|-------------|:------:|
| 1 | D → 1 | D.val = 1 | 1 |
| 2 | N → D | N.val = D.val | 1 |
| 3 | D → 2 | D.val = 2 | 2 |
| 4 | N → N₁ D | 1 × 8 + 2 | **10** |
| 5 | D → 6 | D.val = 6 | 6 |
| 6 | N → N₁ D | 10 × 8 + 6 | **86** |

**∴ (126)₈ = 86₁₀** ✓

---

## Q-3(a)(i) Is the grammar LALR? (07 Marks)

```
X → X + Y | Y       Y → YZ | Z       Z → Z* | a | b
```

### FIRST & FOLLOW

| | FIRST | FOLLOW |
|---|---|---|
| X | {a, b} | {$, +} |
| Y | {a, b} | {$, +, a, b} |
| Z | {a, b} | {$, +, a, b, *} |

### LR(0) Automaton

```
  ┌─────────────────────────────────────────────────────────┐
  │  I₀: X'→.X  X→.X+Y  X→.Y                              │
  │      Y→.YZ  Y→.Z  Z→.Z*  Z→.a  Z→.b                  │
  └───┬──────────┬──────────┬──────────┬──────────┬─────────┘
      │X         │Y         │Z         │a         │b
      ▼          ▼          ▼          ▼          ▼
  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
  │I₁:     │ │I₂:     │ │I₃:     │ │I₄:     │ │I₅:     │
  │X'→X.   │ │X→Y.    │ │Y→Z.   │ │Z→a.   │ │Z→b.   │
  │X→X.+Y  │ │Y→Y.Z   │ │Z→Z.*  │ └────────┘ └────────┘
  └───┬─────┘ └───┬─────┘ └───┬────┘
      │+          │Z          │*
      ▼          ▼          ▼
  ┌─────────┐ ┌────────┐ ┌────────┐
  │I₆:      │ │I₇:     │ │I₈:     │
  │X→X+.Y   │ │Y→YZ.  │ │Z→Z*.  │
  │Y→.YZ... │ │Z→Z.*  │ └────────┘
  └───┬──────┘ └────────┘
      │Y
      ▼
  ┌─────────┐
  │I₉:      │
  │X→X+Y.   │
  │Y→Y.Z    │
  └──────────┘
```

### Conflict Analysis (SLR)

| State | Reduce on | Shift on | Overlap? |
|:-----:|-----------|----------|:--------:|
| I₂ | X→Y on {$,+} | Z on {a,b} | ∅ ✓ |
| I₃ | Y→Z on {$,+,a,b} | * on {*} | ∅ ✓ |
| I₇ | Y→YZ on {$,+,a,b} | * on {*} | ∅ ✓ |
| I₉ | X→X+Y on {$,+} | Z on {a,b} | ∅ ✓ |

**No conflicts → SLR(1) → Since SLR(1) ⊂ LALR(1), the grammar IS LALR** ✓

---

## Q-3(a)(ii) Is the grammar CLR? (07 Marks)

```
S → A &       A → i E | E !       E → i
```

### CLR(1) Item Sets

```
┌──────────────────────────┐
│ I₀:                      │
│   S'→ .S,    {$}         │
│   S → .A&,   {$}         │
│   A → .iE,   {&}         │
│   A → .E!,   {&}         │
│   E → .i,    {!}         │
└──┬─────┬──────┬──────┬───┘
   │S    │A     │i     │E
   ▼     ▼      ▼      ▼
┌──────┐┌──────┐┌────────────┐┌──────────┐
│ I₁:  ││ I₂:  ││ I₃:        ││ I₄:      │
│S'→S. ││S→A.& ││ A→i.E, {&} ││ A→E.!, {&}│
│{$}   ││{$}   ││ E→i.,  {!} │└────┬─────┘
│ACCEPT│└──┬───┘│ E→.i,  {&} │     │!
└──────┘   │&   └──┬────┬────┘     ▼
           ▼      │i   │E    ┌──────────┐
       ┌──────┐   ▼    ▼     │ I₈:      │
       │ I₇:  │┌──────┐┌────┐│ A→E!.,{&}│
       │S→A&. ││ I₅:  ││I₆: ││ REDUCE   │
       │{$}   ││E→i., ││A→iE│└──────────┘
       │REDUCE││{&}   ││.{&}│
       └──────┘│REDUCE││RED.│
               └──────┘└────┘
```

### Conflict Check

| State | Actions | Conflict? |
|:-----:|---------|:---------:|
| I₃ | Reduce E→i on {!}, Shift i on {i} | {!}∩{i} = ∅ ✓ |
| I₅ | Reduce E→i on {&} only | None ✓ |
| I₆ | Reduce A→iE on {&} only | None ✓ |
| I₇ | Reduce S→A& on {$} only | None ✓ |
| I₈ | Reduce A→E! on {&} only | None ✓ |

**No shift-reduce or reduce-reduce conflicts → Grammar IS CLR(1)** ✓

---

## Q-3(b) Operator Precedence Graph and Table (07 Marks)

```
A → ABA | A* | (A) | a       B → + | .
```
`+`, `.`, `*` are operators of regular expressions.

### Precedence Hierarchy

```
  Highest ──► *  (closure)       ─── Precedence = 3
              .  (concatenation) ─── Precedence = 2
  Lowest  ──► +  (union)         ─── Precedence = 1
```

### Operator Precedence Table

| ↓Row \ Col→ | **+** | **.** | **\*** | **(** | **)** | **a** | **$** |
|:-----------:|:-----:|:-----:|:------:|:-----:|:-----:|:-----:|:-----:|
| **+**       |   ⟩   |   ⟨   |   ⟨    |   ⟨   |   ⟩   |   ⟨   |   ⟩   |
| **.**       |   ⟩   |   ⟩   |   ⟨    |   ⟨   |   ⟩   |   ⟨   |   ⟩   |
| **\***      |   ⟩   |   ⟩   |   ⟩    |   —   |   ⟩   |   —   |   ⟩   |
| **(**        |   ⟨   |   ⟨   |   ⟨    |   ⟨   |   ≐   |   ⟨   |   —   |
| **)**        |   ⟩   |   ⟩   |   ⟩    |   —   |   ⟩   |   —   |   ⟩   |
| **a**        |   ⟩   |   ⟩   |   ⟩    |   —   |   ⟩   |   —   |   ⟩   |
| **$**        |   ⟨   |   ⟨   |   ⟨    |   ⟨   |   —   |   ⟨   |   —   |

### Precedence Functions (f and g)

| Symbol | f (left) | g (right) |
|:------:|:--------:|:---------:|
| + | 2 | 1 |
| . | 4 | 3 |
| * | 6 | 5 |
| ( | 0 | 6 |
| ) | 6 | 0 |
| a | 6 | 5 |
| $ | 0 | 0 |

### Precedence Graph

```
  f-nodes                g-nodes
  ═══════                ═══════

  f($)=0 ──────────────► g($)=0

  f(()=0 ──────────────► g()=0  ◄─── ')' yields to everything

  f(+)=2 ──────────────► g(+)=1
    ▲                      │
    │    f(+) > g(+)       │  g(+) < f(.)
    │    so + ⟩ +          ▼
  f(.)=4 ──────────────► g(.)=3
    ▲                      │
    │    f(.) > g(.)       │  g(.) < f(*)
    │    so . ⟩ .          ▼
  f(*)=6 ──────────────► g(*)=5
  f(a)=6 ──────────────► g(a)=5
  f())=6 ──────────────► g(()=6  ◄─── '(' absorbs everything

  Rule: if f(a) > g(b) → a ⟩ b (reduce)
        if f(a) < g(b) → a ⟨ b (shift)
        if f(a) = g(b) → a ≐ b
```

No conflicts → Grammar **is an operator precedence grammar** ✓

---

## Q-4(a) Compare and Contrast Triples vs Indirect Triples (04 Marks)

| Feature | Triples | Indirect Triples |
|---------|---------|-------------------|
| **Structure** | (op, arg1, arg2) — 3 fields | Pointer table → triple table |
| **Result reference** | By triple number (e.g., (0), (1)) | By pointer into triple table |
| **Reordering** | Difficult — changing order breaks references | Easy — just reorder pointer list |
| **Space** | Less (no pointer table) | More (extra pointer table) |
| **Optimization** | Hard to rearrange | Easy to rearrange for optimization |

**Example:** `a = b * c + d`

**Triples:**

| # | op | arg1 | arg2 |
|---|-----|------|------|
| (0) | * | b | c |
| (1) | + | (0) | d |
| (2) | = | a | (1) |

**Indirect Triples:**

| Pointer | → | # | op | arg1 | arg2 |
|---------|---|---|-----|------|------|
| [0] | → | (0) | * | b | c |
| [1] | → | (1) | + | (0) | d |
| [2] | → | (2) | = | a | (1) |

To reorder: just swap pointers [0],[1],[2] without touching the triple table.

---

## Q-4(b) Differentiate AST and DAG with Examples (05 Marks)

| Feature | AST (Abstract Syntax Tree) | DAG (Directed Acyclic Graph) |
|---------|---------------------------|------------------------------|
| **Redundancy** | Duplicate nodes for repeated subexpressions | Shared nodes — no duplication |
| **Structure** | Pure tree (each node has exactly one parent) | Graph (nodes can have multiple parents) |
| **Size** | Larger | Smaller (more compact) |
| **Use** | Intermediate representation, parsing | Code optimization, CSE detection |
| **Construction** | Directly from parse tree | From AST by merging common subexpressions |

**Example:** `a + a * (b - c) + (b - c) * d`

**AST:**
```
              +
            ╱   ╲
          +       *
        ╱   ╲   ╱   ╲
       a     * b-c    d       ← (b-c) appears TWICE
           ╱   ╲
          a   b-c
```

**DAG:**
```
              +
            ╱   ╲
          +       *
        ╱   ╲   ╱   ╲
       a     * ╱     d
           ╱  ╲╱
          a   b-c              ← (b-c) appears ONCE, shared
```

**Key:** DAG detects **common sub-expressions (CSE)** and eliminates redundant computation.

---

## Q-4(c) Three Address Code for Bubble Sort (08 Marks)

**Source:**
```c
for (i = 0; i < n - 1; i++) {
  for (j = 0; j < n - i - 1; j++) {
    if (arr[j] > arr[j + 1]) {
      arr[j] = arr[j + 1];
    }
  }
}
```

### Three Address Code

```
      i = 0                         // (1)
L1:   t1 = n - 1                    // (2)
      if i >= t1 goto L_end         // (3)
      j = 0                         // (4)
L2:   t2 = n - i                    // (5)
      t3 = t2 - 1                   // (6)
      if j >= t3 goto L3            // (7)
      t4 = j * w                    // (8)  w = width of array element
      t5 = arr[t4]                  // (9)  arr[j]
      t6 = j + 1                    // (10)
      t7 = t6 * w                   // (11)
      t8 = arr[t7]                  // (12) arr[j+1]
      if t5 <= t8 goto L4           // (13)
      arr[t4] = t8                  // (14) arr[j] = arr[j+1]
L4:   j = j + 1                     // (15)
      goto L2                       // (16)
L3:   i = i + 1                     // (17)
      goto L1                       // (18)
L_end:                               // (19)
```

---

## Q-5(a) Basic Blocks and Flow Graph from Q-4(c) (10 Marks)

### Identifying Basic Blocks

**Leaders:**
1. First statement → (1)
2. Target of goto → L1:(2), L2:(5), L3:(17), L4:(15), L_end:(19)
3. Statement after conditional goto → (4), (8), (14), (15)

### Basic Blocks

```
┌─────────────────────────────┐
│  B1:  (1) i = 0             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  B2:  (2) t1 = n - 1       │◄──────────────────────┐
│       (3) if i >= t1        │                       │
│           goto L_end        │                       │
└──────┬──────────────┬───────┘                       │
       │ F            │ T                             │
       ▼              ▼                               │
┌──────────────┐  ┌─────────┐                         │
│  B3:         │  │  B7:    │                         │
│  (4) j = 0   │  │  L_end  │                         │
└──────┬───────┘  │  (EXIT) │                         │
       │          └─────────┘                         │
       ▼                                              │
┌─────────────────────────────┐                       │
│  B4:  (5)  t2 = n - i      │◄──────────┐           │
│       (6)  t3 = t2 - 1     │           │           │
│       (7)  if j >= t3       │           │           │
│            goto L3          │           │           │
└──────┬──────────────┬───────┘           │           │
       │ F            │ T                 │           │
       ▼              │                   │           │
┌─────────────────────┤                   │           │
│  B5:  (8)  t4=j*w   │                   │           │
│       (9)  t5=arr[t4]│                  │           │
│       (10) t6=j+1    │                  │           │
│       (11) t7=t6*w   │                  │           │
│       (12) t8=arr[t7]│                  │           │
│       (13) if t5<=t8 │                  │           │
│            goto L4   │                  │           │
└──────┬───────┬───────┘                  │           │
       │ F     │ T                        │           │
       ▼       │                          │           │
┌──────────┐   │                          │           │
│B5a:      │   │                          │           │
│(14)arr[t4│   │                          │           │
│   = t8   │   │                          │           │
└──────┬───┘   │                          │           │
       │       │                          │           │
       ▼       ▼                          │           │
┌─────────────────────┐                   │           │
│  B6: (15) j = j + 1 │                   │           │
│      (16) goto L2    │───────────────────┘           │
└──────────────────────┘                               │
               │ (from B4 T-branch)                    │
               ▼                                       │
┌──────────────────────────┐                           │
│  B6a: (17) i = i + 1    │                            │
│       (18) goto L1       │───────────────────────────┘
└──────────────────────────┘
```

### Summary of Blocks

| Block | Statements | Description |
|:-----:|-----------|-------------|
| B1 | (1) | Initialize i |
| B2 | (2)-(3) | Outer loop header |
| B3 | (4) | Initialize j |
| B4 | (5)-(7) | Inner loop header |
| B5 | (8)-(13) | Compare arr[j], arr[j+1] |
| B5a | (14) | Swap assignment |
| B6 | (15)-(16) | Inner loop increment |
| B6a | (17)-(18) | Outer loop increment |
| B7 | (19) | Exit |

---

## Q-5(b) Two Loop Optimization Techniques (08 Marks)

### 1. Loop Invariant Code Motion (LICM)

Move computations that produce the **same result in every iteration** outside the loop.

**Before:**
```
for (i = 0; i < n; i++) {
    x = y + z;          // ← y+z doesn't change inside loop
    a[i] = x * i;
}
```

**After:**
```
x = y + z;               // ← moved outside loop
for (i = 0; i < n; i++) {
    a[i] = x * i;
}
```

**Benefit:** Eliminates redundant computation of `y + z` across n iterations.

---

### 2. Induction Variable Elimination / Strength Reduction

Replace **expensive operations** (multiply) with **cheaper ones** (addition) for variables that change by a fixed amount each iteration.

**Before:**
```
for (i = 0; i < n; i++) {
    t = i * 4;           // ← multiplication every iteration
    a[t] = 0;
}
```

**After (Strength Reduction):**
```
t = 0;
for (i = 0; i < n; i++) {
    a[t] = 0;
    t = t + 4;           // ← replaced multiply with addition
}
```

**Benefit:** Addition is much cheaper than multiplication in hardware. If `i` is only used to compute `t`, then `i` can be **eliminated** entirely (induction variable elimination).

---

## Q-6(a) Loader — Language Processor for Relocation (05 Marks)

The **Loader** is responsible for relocating the program's code.

### Roles of a Loader

| Role | Description |
|------|-------------|
| **1. Allocation** | Allocates memory space for the program in main memory |
| **2. Relocation** | Adjusts all address-sensitive instructions to reflect actual load address. Adds relocation factor (start address − origin) to all relocatable addresses |
| **3. Linking** | Resolves external references between separately compiled modules |
| **4. Loading** | Physically places the machine code into the allocated memory locations |

### Types of Loaders:

```
  ┌──────────────────┐
  │ Compile-and-Go   │ ── No separate loader, assembler places code directly
  ├──────────────────┤
  │ Absolute Loader  │ ── No relocation, loads at fixed address
  ├──────────────────┤
  │ Relocating Loader│ ── Adjusts addresses based on load address
  ├──────────────────┤
  │ Dynamic Loader   │ ── Loads modules on demand at runtime
  └──────────────────┘
```

---

## Q-6(a) OR — Linker (05 Marks)

The **Linker** is responsible for combining different object files and libraries into a single executable.

### Roles of a Linker

| Role | Description |
|------|-------------|
| **1. Symbol Resolution** | Matches every external reference with exactly one symbol definition across all object files |
| **2. Relocation** | Adjusts relative addresses in each object module to absolute addresses in combined executable |
| **3. Library Linking** | Searches and includes required library routines (static linking) |
| **4. Merging Sections** | Combines .text, .data, .bss sections from multiple object files into single sections |
| **5. Output Generation** | Produces final executable file with correct memory layout |

```
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ main.o   │   │ utils.o  │   │ libc.a   │
  │ (Object) │   │ (Object) │   │(Library) │
  └────┬─────┘   └────┬─────┘   └────┬─────┘
       │               │              │
       └───────────┬───┘──────────────┘
                   │
              ┌────▼────┐
              │  LINKER │
              └────┬────┘
                   │
            ┌──────▼──────┐
            │  a.exe      │
            │ (Executable)│
            └─────────────┘
```

---

## Q-6(b) Assembler Pass-I (10 Marks)

**Source Program:**
```
        START  210
        MOVER  AREG, N
L1      MOVER  BREG, ='2'
        ADD    AREG, ='3'
        SUB    BREG, X
BACK    COMP   BREG, Y
        BC     ANY, L1
        LTORG
        ORIGIN BACK + 5
        DIV    BREG, ='3'
        STOP
Y       DS     3
N       DS     4
X       DC     '5'
        END
```

### Step 1: Symbol Table (SYMTAB)

| Symbol | Address |
|:------:|:-------:|
| L1 | 211 |
| BACK | 215 |
| Y | 222 |
| N | 225 |
| X | 229 |

### Step 2: Literal Table (LITTAB)

| Literal | Address |
|:-------:|:-------:|
| ='2' | 217 |
| ='3' | 218 |
| ='3' | 220 |

### Step 3: Pool Table (POOLTAB)

| Pool # | Starting Literal Index |
|:------:|:---------------------:|
| 1 | 0 |
| 2 | 2 |

### Step 4: Location Counter Trace & Intermediate Code

| LC | Source Statement | Intermediate Code |
|:---:|-----------------|-------------------|
| 210 | MOVER AREG, N | (IS, 04) (1) (S, 225) |
| 211 | L1: MOVER BREG, ='2' | (IS, 04) (2) (L, 0) |
| 212 | ADD AREG, ='3' | (IS, 01) (1) (L, 1) |
| 213 | SUB BREG, X | (IS, 02) (2) (S, 229) |
| 214 | — | — |
| 215 | BACK: COMP BREG, Y | (IS, 06) (2) (S, 222) |
| 216 | BC ANY, L1 | (IS, 07) (6) (S, 211) |
| — | LTORG | — |
| 217 | ='2' | (DL, 02) (C, 2) |
| 218 | ='3' | (DL, 02) (C, 3) |
| — | ORIGIN BACK+5 | (AD, 05) (C, 220) |
| 220 | DIV BREG, ='3' | (IS, 08) (2) (L, 2) |
| 221 | STOP | (IS, 00) |
| 222 | Y: DS 3 | (DL, 01) (C, 3) |
| 225 | N: DS 4 | (DL, 01) (C, 4) |
| 229 | X: DC '5' | (DL, 02) (C, 5) |
| — | END | (AD, 02) |

### LC Trace Explanation

```
  210 ← START 210
  211 ← L1 defined here
  212
  213
  214 ← (skipped/internal)
  215 ← BACK defined here
  216
  ─── LTORG processes pool #1 ───
  217 ← ='2' placed here
  218 ← ='3' placed here
  ─── ORIGIN BACK+5 = 215+5 = 220 ───
  220 ← LC jumps to 220
  221 ← STOP
  222 ← Y (DS 3 → occupies 222,223,224)
  225 ← N (DS 4 → occupies 225,226,227,228)
  229 ← X (DC '5')
  ─── END: remaining literal ='3' placed ───
  230 ← ='3' (pool #2) placed here
```

**Note:** At END, any unprocessed literals in the current pool are assigned addresses.

---
