# CNS PYQ 2025 -> Complete Solutions
**Subject:** Cryptography and Network Security | **Year:** 2025

---

## Q1a. Primitive Roots Modulo 26 (5 Marks)

**Question:** What is a primitive root? Examine whether primitive roots exist modulo 26. Determine the number of primitive roots, if any exist.

### Answer

**Definition:** A primitive root modulo n is an integer g such that every integer coprime to n can be expressed as a power of g modulo n. Formally, g is a primitive root mod n if the multiplicative order of g equals phi(n).

**Does a primitive root exist modulo 26?**

Primitive roots exist modulo n only when n is: 1, 2, 4, p^k, or 2p^k (where p is an odd prime).

26 = 2 x 13

Since 26 = 2 x 13 (form 2p^k with p=13, k=1), **primitive roots DO exist modulo 26**.

**Finding phi(26):**
phi(26) = phi(2) x phi(13) = 1 x 12 = **12**

**Number of primitive roots:**
If primitive roots exist, the number of primitive roots mod n = phi(phi(n)) = phi(12)

phi(12) = phi(4) x phi(3) = 2 x 2 = **4**

So there are **4 primitive roots modulo 26**.

**Finding them:** We need g where ord(g) = 12, and gcd(g,26)=1.

Candidates coprime to 26 (not divisible by 2 or 13): {1,3,5,7,9,11,15,17,19,21,23,25}

Test g=7: Compute powers mod 26:
7^(-1)=7, 7^(-1)=49=23, 7^(-1)=7 x 23=161=5, 74=7 x 5=35=9,
76=9 x 23=207=207-7 x 26=207-182=25, 7xx=25^(-1)=625=625-24 x 26=625-624=1

Check 7^d ? 1 for d | 12, d < 12: {1,2,3,4,6}
7^1=7?1, 7^2=23?1, 7^3=5?1, 7^4=9?1, 7^6=25?1 ?

**g=7 is a primitive root mod 26.**

Other primitive roots: 7^k mod 26 where gcd(k,12)=1 ? k ? {1,5,7,11}
- 7^1 mod 26 = **7**
- 7^5 = 7^4 x 7 = 9 x 7 = 63 mod 26 = 63-2 x 26 = **11**
- 7^7 = 7^6 x 7 = 25 x 7=175 mod 26 = 175-6 x 26=175-156 = **19**
- 7^11 = 7^12 x 7 = 1 x 7^(-1). 7?-> mod 26: 7 x 15=105=4 x 26+1 ? 7^(-1)=15 ? **15**

> **Primitive roots mod 26: {7, 11, 15, 19}** x 4 primitive roots total.

### Depth of Understanding

| Concept | Detail |
|---|---|
| Existence Condition | n = 1,2,4,p?,2p? only |
| Count Formula | phi(phi(n)) primitive roots |
| Why 26? | 26=2 x 13=2px -> satisfies condition |
| Generator Usage | DH key exchange uses primitive root as generator g |
| Order of element | Smallest k>0 where g^k = 1 mod n |

### Alternate Questions
1. Find all primitive roots mod 7.
2. Does a primitive root exist mod 8? Justify.
3. Prove that if g is a primitive root mod p, then g^k is a primitive root iff gcd(k, p-1)=1.

---

## Q1b. General Group vs Abelian Group -> Identity Uniqueness (5 Marks)

**Question:** What is the key difference between a general group and an abelian group? Prove with example that the identity element in a group is unique.

### Answer

**Key Difference:**

| Property | General Group | Abelian Group |
|---|---|---|
| Closure | ? | ? |
| Associativity | ? | ? |
| Identity | ? | ? |
| Inverse | ? | ? |
| **Commutativity** | ? NOT required | ? axb = bxa |

**Example of Non-Abelian Group:** Matrix multiplication under 2 x 2 invertible matrices. AB ? BA in general.

**Example of Abelian Group:** (Z, +) -> integer addition. a+b = b+a always.

**Proof: Identity Element is Unique**

*Claim:* In any group G, the identity element is unique.

*Proof by contradiction:*
Suppose e and e' are both identity elements of G.

Since e is an identity: **e -> e' = e'** (by definition of e acting on e')
Since e' is an identity: **e -> e' = e** (by definition of e' acting on e)

Therefore: e = e -> e' = e'

Hence e = e', which means the identity is **unique**. ?

*Example verification:* In (Z,+), suppose 0 and 0' are both identities.
- 0 + 0' = 0' (since 0 is identity)
- 0 + 0' = 0 (since 0' is identity)
- Therefore 0 = 0' ?

### Alternate Questions
1. State and prove that the inverse of each element in a group is unique.
2. Is (Z?, x) a group for any n? When is it a group?
3. Give an example of a group that is not abelian and prove it is not abelian.

---

## Q2a. Compute X = 3^160 + 5^(-1) mod 17 (5 Marks)

**Question:** Calculate the value of X modulo 17 where X = 3^160 + 5^(-1) mod 17

### Answer

**Part 1: Compute 3^160 mod 17**

By **Fermat's Little Theorem:** If p is prime and gcd(a,p)=1, then a^(p-1) = 1 mod p.

Here p=17 (prime), a=3, so: **3^16 = 1 mod 17**

160 = 16 x 10, so:
```
3^160 = (3^16)^10 = 1^10 = 1 mod 17
```
**3^160 mod 17 = 1**

**Part 2: Compute 5^(-1) mod 17**

Find x such that 5x = 1 mod 17 (using extended EA or inspection):

5 x 7 = 35 = 2 x 17 + 1 = 1 mod 17

**5^(-1) mod 17 = 7**

**Final Answer:**
```
X = 3^160 + 5^(-1) mod 17
  = 1 + 7
  = 8 mod 17
```
> **X = 8**

### Depth of Understanding
- Fermat's Little Theorem is the foundation of RSA (phi(n) replaces p-1).
- Modular inverse exists only when gcd(5,17)=1 -> true since 17 is prime.
- Extended EA gives the general method for modular inverses.

---

## Q2b. Discrete Log: 4^x = 13 mod 19 (5 Marks)

**Question:** Find the smallest positive integer x satisfying 4^x = 13 mod 19.

### Answer

Compute all powers of 4 mod 19 systematically:

| x | 4^x mod 19 |
|---|---|
| 1 | 4 |
| 2 | 16 |
| 3 | 64=7 |
| 4 | 28=9 |
| 5 | 36=17 |
| 6 | 68=11 |
| 7 | 44=6 |
| 8 | 24=5 |
| 9 | 20=**1** |

**Order of 4 mod 19 = 9** (since 4^9 = 1 and 9 | phi(19)=18 ?)

The subgroup generated by 4 = {1, 4, 5, 6, 7, 9, 11, 16, 17}

Since **13 ? {1,4,5,6,7,9,11,16,17}**, the equation 4^x = 13 mod 19 has **no solution**.

**Why?** 4 is not a primitive root mod 19 (order 9 ? 18 = phi(19)). Only elements in the subgroup ?4? can be expressed as powers of 4.

> **No solution exists.** This tests whether students understand subgroup structure in discrete logarithm problems.

### Alternate Questions
1. Verify that 2 is a primitive root mod 19 and find 2^x = 13 mod 19.
2. What is the discrete logarithm problem? Why is it hard in general?

---

## Q2a (OR). Extended Euclidean: 35x = 1 mod 48 (8 Marks)

**Question:** Use Extended Euclidean Algorithm to find smallest positive x such that 35x = 1 mod 48.

### Answer

**Step 1 -> Euclidean Division:**

| Step | Equation | Remainder |
|---|---|---|
| 1 | 48 = 1 x 35 + **13** | 13 |
| 2 | 35 = 2 x 13 + **9** | 9 |
| 3 | 13 = 1 x 9 + **4** | 4 |
| 4 | 9 = 2 x 4 + **1** | 1 |
| 5 | 4 = 4 x 1 + **0** | 0 |

**GCD(35,48) = 1** ? (inverse exists)

**Step 2 -> Back Substitution:**
```
1 = 9 - 2 x 4                               ... Step 4
4 = 13 - 1 x 9                              ... Step 3
1 = 9 - 2x(13-9) = 3 x 9 - 2 x 13            ... substitute
9 = 35 - 2 x 13                             ... Step 2
1 = 3x(35-2 x 13) - 2 x 13 = 3 x 35 - 8 x 13    ... substitute
13 = 48 - 1 x 35                            ... Step 1
1 = 3 x 35 - 8x(48-35) = 11 x 35 - 8 x 48     ... substitute
```

Therefore: **35 x 11 = 1 mod 48**

> **x = 11** (smallest positive integer)

**Verification:** 35 x 11 = 385 = 8 x 48 + 1 = 1 mod 48 ?

---

## Q2b (OR). Ciphertext-Only Attack (COA) (2 Marks)

**Question:** What is a COA? What primary information is available to the attacker?

### Answer

**Ciphertext-Only Attack (COA):** The weakest and most common attack model. The attacker has access **only to the ciphertext** -> no knowledge of plaintext, no ability to choose messages.

**Information Available:**
- One or more ciphertext samples encrypted under the same key
- Possibly the encryption algorithm used (Kerckhoffs's Principle -> algorithm is public)
- Statistical properties of the expected plaintext language (e.g., English letter frequencies)

**Goal:** Recover the plaintext or the key.

**Example:** Frequency analysis on Caesar cipher ciphertext x 'e' most common in English maps to most frequent ciphertext letter.

**Why it's the weakest attack:** Any cipher that cannot withstand COA is completely broken. Modern ciphers (AES, RSA) must be secure even against much stronger attacks (CPA, CCA).

---

## Q3a. CRT: x=2(mod3), x=3(mod5), x=2(mod7) (10 Marks)

### Answer

**M = 3 x 5 x 7 = 105**

| i | m? | a? | M?=M/m? | y?=M??-> mod m? | a?M?y? |
|---|---|---|---|---|---|
| 1 | 3 | 2 | 35 | 35 mod 3=2; 2?-> mod 3=2 | 2 x 35 x 2=140 |
| 2 | 5 | 3 | 21 | 21 mod 5=1; 1?-> mod 5=1 | 3 x 21 x 1=63 |
| 3 | 7 | 2 | 15 | 15 mod 7=1; 1?-> mod 7=1 | 2 x 15 x 1=30 |

**Verify inverses:**
- 2 x 2=4=1 mod 3 ?
- 1 x 1=1=1 mod 5 ?
- 1 x 1=1=1 mod 7 ?

```
x = (140 + 63 + 30) mod 105
  = 233 mod 105
  = 233 - 2 x 105
  = 233 - 210 = 23
```

> **x = 23**

**Verify:** 23 mod 3 = 2 ? | 23 mod 5 = 3 ? | 23 mod 7 = 2 ?

### Depth of Understanding
- CRT: unique solution exists when all moduli are pairwise coprime.
- Solution is unique modulo M = m1xm2xm3 = 105.
- Used in RSA for fast decryption (CRT-RSA).

---

## Q3a (OR-i). Elliptic Curve E: yx = xx+1 (mod 7) (5 Marks)

### Answer

**QR mod 7:** 1^(-1)=1, 2^(-1)=4, 3^(-1)=2, 4^(-1)=2, 5^(-1)=4, 6^(-1)=1 ? QR = {0,1,2,4}

| x | xx+1 mod 7 | Is QR? | y values | Points |
|---|---|---|---|---|
| 0 | 0+1=1 | ? | 1,6 | (0,1),(0,6) |
| 1 | 1+1=2 | ? | 3,4 | (1,3),(1,4) |
| 2 | 8+1=9=2 | ? | 3,4 | (2,3),(2,4) |
| 3 | 27+1=28=0 | ? | 0 | (3,0) |
| 4 | 64+1=65=2 | ? | 3,4 | (4,3),(4,4) |
| 5 | 125+1=126=0 | ? | 0 | (5,0) |
| 6 | 216+1=217=0 | ? | 0 | (6,0) |

**Mod checks:** 28=4 x 7=0 ? | 65-63=2 ? | 126=18 x 7=0 ? | 217=31 x 7=0 ?

> **All Points: {O, (0,1),(0,6),(1,3),(1,4),(2,3),(2,4),(3,0),(4,3),(4,4),(5,0),(6,0)} -> Total: 13 points**

---

## Q3a (OR-ii). GF(25) Multiplication (5 Marks)

**Compute axb mod p(x) in GF(25)**
a = x4+xx+xx+1, b = xx+xx+x+1, p(x) = x5+xx+1

**Step 1 -> Multiply:**
```
(x4+xx+xx+1)(xx+xx+x+1):

x7: x4xxx            ? 1
x6: x4xxx + xxxxx    ? 1+1=0
x5: x4xx + xxxxx + xxxxx ? 1+1+1=1
x4: x4 x 1 + xxxx + xxxxx ? 1+1+1=1
xx: xxx1 + xxxx + 1xxx  ? 1+1+1=1
xx: xxx1 + 1xxx         ? 1+1=0
xx: 1xx                 ? 1
xx: 1 x 1                 ? 1
```
Product = **x7 + x5 + x4 + xx + x + 1**

**Step 2 -> Reduce mod p(x) = x5+xx+1:**

p(x)=0 ? x5 = xx+1

x6 = xxx5 = x(xx+1) = xx+x
x7 = xxx6 = x(xx+x) = x4+xx

**Substitute:**
```
x7 + x5 + x4 + xx + x + 1
= (x4+xx) + (xx+1) + x4 + xx + x + 1
= (x4+x4) + (xx+xx) + (1+1) + xx + x
= 0 + 0 + 0 + xx + x
= xx + x
```
> **a -> b mod p(x) = xx + x**

---

## Q4a. El-Gamal Cryptosystem -> Key Gen, Encryption, Decryption (10 Marks)

**Question:** Describe the three main algorithms (Key Generation, Encryption, Decryption) of El-Gamal. Explain how a recipient recovers the plaintext.

### Answer

El-Gamal is a **public-key cryptosystem** based on the **Discrete Logarithm Problem (DLP)**. It is a **randomized** (probabilistic) encryption scheme.

---

#### Algorithm 1: Key Generation

1. Choose a large prime **p** and a primitive root **g** of p. (Both public)
2. Choose a random private key **x** where 1 < x < p-1. (Secret)
3. Compute **y = g^x mod p**. (Public)

**Public Key:** (p, g, y)  
**Private Key:** x

**Example:** p=23, g=5, x=6 ? y = 5^6 mod 23 = 15625 mod 23 = 8

---

#### Algorithm 2: Encryption

To encrypt message M (where 1 < M < p):

1. Choose a **random ephemeral key k** (1 < k < p-1, gcd(k,p-1)=1, new each time)
2. Compute **C1 = g^k mod p**
3. Compute **C2 = M -> y^k mod p**
4. **Ciphertext = (C1, C2)**

**Example (continued):** M=10, k=3
- C1 = 5^3 mod 23 = 125 mod 23 = 10
- y^k = 8^3 mod 23 = 512 mod 23 = 512-22 x 23=512-506=6
- C2 = 10 x 6 mod 23 = 60 mod 23 = 60-2 x 23=14
- Ciphertext = **(10, 14)**

---

#### Algorithm 3: Decryption

Given ciphertext (C1, C2) and private key x:

1. Compute **s = C1^x mod p** (this equals g^(kx) = y^k)
2. Compute **s^(-1) mod p** (modular inverse of s)
3. Recover **M = C2 -> s^(-1) mod p**

**Why this works:**
```
C2 -> s^(-1) = (M -> y^k) -> (C1^x)^(-1)
            = M -> y^k -> (g^(kx))^(-1)
            = M -> y^k -> (y^k)^(-1)   [since y = g^x ? y^k = g^(kx)]
            = M ?
```

**Example (continued):** C1=10, C2=14, x=6
- s = 10^6 mod 23: 10^(-1)=100=8, 10^(-1)=8 x 10=80=80-3 x 23=11, 10^6=11^(-1)=121=121-5 x 23=6
- s^(-1) mod 23: 6 x 4=24=1 ? 6^(-1)=4
- M = 14 x 4 mod 23 = 56 mod 23 = 56-2 x 23 = **10** ?

---

#### Security Summary

| Aspect | Detail |
|---|---|
| Security Basis | Discrete Logarithm Problem (DLP) |
| Randomness | Random k ensures same M ? different CT each time |
| Ciphertext Size | 2^(-1) plaintext (pair C1,C2) |
| CPA Security | ? IND-CPA secure |
| If k reused | Security collapses -> attacker can find M |

### Depth of Understanding
- The shared secret is **y^k = C1^x** -> this is Diffie-Hellman key agreement embedded in El-Gamal.
- El-Gamal is **malleable**: given Enc(M) = (C1,C2), attacker can form Enc(2M) = (C1, 2xC2 mod p). Not IND-CCA secure.
- El-Gamal over **elliptic curves** (EC-ElGamal) gives same security with smaller key sizes.

### Alternate Questions
1. Show that El-Gamal is malleable. How does this break CCA security?
2. Compare El-Gamal and Diffie-Hellman key exchange -> what do they have in common?
3. What happens if an attacker learns k for one El-Gamal ciphertext?

---

## Q5a. Identity-Based Encryption (IBE) (5 Marks)

**Question:** Explain the fundamental concept of IBE. How does IBE simplify public key management compared to traditional PKI?

### Answer

**Fundamental Concept:**

IBE is a public-key scheme where a user's **identity string** (email, name, employee ID) **serves directly as the public key**. No certificate is required.

**Traditional PKI Problem:**
- Alice wants to send an encrypted email to Bob.
- She must first **obtain Bob's certificate** from a CA, verify it hasn't expired/revoked, then use the public key inside it.
- Certificate management is expensive, complex, and error-prone.

**IBE Solution:**
```
Alice wants to encrypt to "bob@company.com":
  C = IBE_Encrypt("bob@company.com", M, master_params)

Bob requests his private key from PKG (Private Key Generator):
  sk_bob = Extract(master_secret, "bob@company.com")

Bob decrypts:
  M = IBE_Decrypt(sk_bob, C)
```

**IBE System Components:**

| Component | Role |
|---|---|
| PKG (Private Key Generator) | Holds master secret; issues private keys |
| Master Public Parameters | Public system parameters (like a global public key) |
| Identity String | User's public key -> no certificate needed |
| Private Key | Issued by PKG after identity verification |

**IBE vs PKI:**

| Feature | PKI | IBE |
|---|---|---|
| Public Key | Certificate with public key | Identity string itself |
| Certificate Management | Required | Not needed |
| Pre-registration | Required before encryption | Not required |
| Encrypt before user exists | ? No | ? Yes (key issued later) |
| Key Escrow | No (private keys self-generated) | ? Yes (PKG knows all keys) |

**Key Insight:** In IBE, Alice can encrypt to "bob@company.com" even **before Bob has ever registered** with the system. Bob gets his private key later and decrypts.

**Mathematical Basis:** Boneh-Franklin IBE -> based on **bilinear pairings** on elliptic curves (x: GxG?GT).

### Alternate Questions
1. What is the key escrow problem in IBE? Propose a mitigation.
2. What is Hierarchical IBE (HIBE)? When is it used?
3. How do bilinear pairings enable IBE?

---

## Q5b. Attribute-Based Encryption (ABE) (5 Marks)

**Question:** Explain the core idea and purpose of ABE. How does ABE enable more flexible and fine-grained access control?

### Answer

**Core Idea:**

ABE extends IBE by associating **sets of attributes** and **access policies** with keys and ciphertexts, enabling one-to-many encryption with fine-grained policy enforcement.

**Two Main Types:**

**KP-ABE (Key-Policy ABE):**
- Ciphertext tagged with attributes (e.g., {Doctor, Cardiology, 2025})
- Private key encodes an access policy (e.g., "Doctor AND Cardiology")
- User can decrypt if their key's policy is satisfied by the ciphertext's attributes

**CP-ABE (Ciphertext-Policy ABE):**
- Ciphertext encodes the access policy (e.g., "(Doctor AND ICU) OR Admin")
- Private key contains user's attributes
- User can decrypt if their attributes satisfy the ciphertext's policy

**Why ABE > Traditional PKE for fine-grained access:**

```
Scenario: Hospital encrypts patient record for:
  "Any Cardiologist OR any Admin with Clearance=High"

Traditional PKE: Must encrypt separately for each qualifying person.
ABE (CP-ABE):   Encrypt once with policy.
                Anyone whose attributes match can decrypt.
                New qualifying staff automatically have access.
```

**Real-World Use Cases:**

| Domain | ABE Use |
|---|---|
| Healthcare | Records accessible only to treating physicians |
| Cloud Storage | Files decryptable by role+department combinations |
| Government | "Top Secret AND Need-to-Know" clearance policies |
| IoT | Device firmware updates for specific device classes |

**IBE vs ABE Summary:**

| Feature | IBE | ABE |
|---|---|---|
| Access Granularity | One identity = one recipient | Policy over many attributes |
| Expressiveness | Low (identity only) | High (AND/OR policies) |
| Use Case | Email, device auth | Healthcare, cloud, gov |
| Complexity | Moderate | Higher |

### Alternate Questions
1. Design an ABE policy for a university where only "Professor AND CS Department" can decrypt exam papers.
2. How is Shamir's Secret Sharing used inside ABE constructions?
3. What is multi-authority ABE?

---

## Q6a. Shamir (3,4) Secret Sharing -> p=19, Shares (1,10),(2,0),(4,11) (10 Marks)

**Question:** In a (3,4) Shamir scheme with p=19, shares: (1,10), (2,0), (4,11). Find secret s.

### Answer

**Setup:** f(x) = a0 + a1x + a2x-> mod 19. Secret = f(0) = a0.

Use Lagrange interpolation with (x1,y1)=(1,10), (x2,y2)=(2,0), (x3,y3)=(4,11):

**Lagrange Basis Polynomials at x=0:**

```
L1(0) = [(0-2)(0-4)] / [(1-2)(1-4)]
       = [(-2)(-4)] / [(-1)(-3)]
       = 8/3 mod 19

L2(0) = [(0-1)(0-4)] / [(2-1)(2-4)]
       = [(-1)(-4)] / [(1)(-2)]
       = 4/(-2) mod 19

L4(0) = [(0-1)(0-2)] / [(4-1)(4-2)]
       = [(-1)(-2)] / [(3)(2)]
       = 2/6 mod 19
```

**Compute Modular Inverses:**
- 3?-> mod 19: 3 x 13=39=2 x 19+1 ? **3?x = 13**
- (-2) mod 19 = 17. 17?-> mod 19: 17 x 9=153=8 x 19+1 ? **17?x = 9** (so (-2)?x = 9)
- 6?-> mod 19: 6 x 16=96=5 x 19+1 ? **6?x = 16**

**Evaluate Basis:**
- L1(0) = 8 x 13 mod 19 = 104 mod 19 = 104-5 x 19 = **9**
- L2(0) = 4 x 9 mod 19 = 36 mod 19 = **17**
- L4(0) = 2 x 16 mod 19 = 32 mod 19 = **13**

**Compute Secret:**
```
f(0) = y1xL1(0) + y2xL2(0) + y3xL4(0) mod 19
     = 10 x 9 + 0 x 17 + 11 x 13 mod 19
     = 90 + 0 + 143 mod 19
     = 233 mod 19
     = 233 - 12 x 19 = 233-228 = 5
```

> **Secret s = f(0) = 5**

**Verification -> Recover polynomial f(x) = 5 + a1x + a2xx:**

From f(1)=10: 5+a1+a2=10 ? a1+a2=5
From f(2)=0: 5+2a1+4a2=0 ? 2a1+4a2=14 mod 19

Subtract: 2a2=4 ? **a2=2**, **a1=3**

**f(x) = 5 + 3x + 2x-> mod 19**
- f(1) = 5+3+2 = 10 ?
- f(2) = 5+6+8 = 19 = 0 ?
- f(4) = 5+12+32 = 49 = 2 x 19+11 = 11 ?

### Depth of Understanding

| Concept | Detail |
|---|---|
| (t,n) = (3,4) | 3 shares needed, 4 distributed |
| Security | With < 3 shares: information-theoretically secure |
| Polynomial degree | t-1 = 2 (quadratic) |
| Prime modulus | p=19 ensures Z? is a field (all inverses exist) |
| Lagrange uniqueness | Exactly one degree-(t-1) polynomial through t points |

### Alternate Questions
1. In a (2,3) scheme mod 7 with shares (1,3),(2,1), find the secret.
2. Why must p > n and p > secret in Shamir's scheme?
3. What is Verifiable Secret Sharing? How does Feldman's scheme extend Shamir's?

---

## Q7. Network Security, Firewall, IDS (3+3+4 Marks)

### 7a. Define Network Security and Its Primary Objective

**Network Security** is the practice of protecting a computer network infrastructure from unauthorized access, misuse, malfunction, modification, destruction, or improper disclosure, thereby creating a secure platform for computers, users, and programs to perform their permitted critical functions.

**Primary Objective:** Ensure the **CIA Triad**:
- **Confidentiality** -> Prevent unauthorized access to data
- **Integrity** -> Ensure data is not altered without authorization
- **Availability** -> Ensure network services are accessible to authorized users

Secondary objectives: Authentication, Non-repudiation, Access Control.

---

### 7b. Firewall as Barrier Between Internal and External Networks

A **firewall** is a hardware/software security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.

```
  Internet                     Internal Network
 (Untrusted)  --? [FIREWALL] --?  (Trusted)
                      |
               [Rule Engine]
               ALLOW/DENY
               based on:
               - IP address
               - Port number
               - Protocol
               - State (stateful)
```

**Types of Firewalls:**
| Type | How it Works |
|---|---|
| Packet Filtering | Checks IP/port headers -> fast but shallow |
| Stateful Inspection | Tracks connection state -> knows if packet belongs to established session |
| Application Layer (WAF) | Deep packet inspection -> understands HTTP, FTP content |
| Next-Gen Firewall (NGFW) | IDS/IPS + application awareness + SSL inspection |

**Example Rule:** DENY all inbound traffic on port 23 (Telnet). ALLOW port 443 (HTTPS) inbound.

---

### 7c. Intrusion Detection System (IDS)

**Definition:** An IDS monitors network or system activities for malicious activities or policy violations and **reports** them to a management system (unlike a firewall which blocks).

**Objectives:**
- Detect attacks, intrusions, and policy violations in real-time
- Log and alert administrators about suspicious activity
- Provide forensic evidence for post-incident analysis

**Two Types of IDS:**

| Type | Method | Pros | Cons |
|---|---|---|---|
| **Signature-Based (SIDS)** | Matches traffic against known attack patterns | High accuracy for known attacks | Cannot detect zero-day attacks |
| **Anomaly-Based (AIDS)** | Baselines normal behavior; flags deviations | Detects unknown/novel attacks | High false-positive rate |

> **IDS vs IPS:** IDS detects and alerts; IPS (Intrusion Prevention System) also actively blocks the attack.

### Alternate Questions
1. What is a DMZ (Demilitarized Zone) in network architecture?
2. Compare NIDS (Network IDS) vs HIDS (Host IDS).
3. What is a honeypot and how does it complement IDS?

---

## Q8a. Malware -> Worm vs Virus (3+5+2 Marks)

**Question:** Malicious code spreads automatically to all computers on the network without user intervention.
i. What kind of malware? ii. How it differs from a traditional virus.

### i. Type of Malware: WORM

A **worm** is self-replicating malware that **spreads automatically across networks** without requiring user interaction or a host file.

The key indicator: *"automatic spreading without user intervention"* = **Worm**.

**Famous Examples:** WannaCry (2017), Stuxnet, ILOVEYOU, Morris Worm.

### ii. Worm vs Traditional Virus

| Property | Virus | Worm |
|---|---|---|
| Host required | ? Needs a host file to attach to | ? Self-contained, standalone |
| User action needed | ? User must execute infected file | ? Spreads automatically |
| Propagation | Via file sharing, email attachments | Via network connections, vulnerabilities |
| Primary damage | File corruption, data destruction | Network congestion, bandwidth consumption |
| Example | Melissa virus, CIH | WannaCry, Slammer, Conficker |
| Replication target | Files/programs on same machine | Other machines on the network |

### Depth of Understanding
- Worms exploit **network vulnerabilities** (open ports, unpatched services) to propagate.
- WannaCry used EternalBlue (MS17-010 SMB exploit) to spread as a worm.
- Worm damage is often **indirect** (network saturation) rather than direct file damage.

---

## Q8b. How a Trojan Horse Enters a System (5 Marks)

**Question:** How does a Trojan Horse typically enter a user's system?

### Answer

A **Trojan Horse** is malware disguised as legitimate, useful software. Unlike viruses/worms, it does **not self-replicate** -> it relies entirely on **social engineering** to trick users into executing it.

**Common Entry Vectors:**

1. **Email Attachments:** "Invoice.pdf.exe" -> appears to be a PDF, executes malware.

2. **Fake Software Downloads:** Cracked software, free games, "free antivirus" tools from untrusted sources.

3. **Malvertising:** Malicious ads on legitimate websites that auto-download when clicked.

4. **Social Engineering:** Phishing messages: "Your account will be suspended -> click here to verify."

5. **Drive-by Downloads:** Visiting a compromised website that silently downloads an executable.

6. **Bundled Software:** Freeware that bundles a Trojan in the installer (hidden behind "I Agree").

**What Trojans do once inside:**
- Open backdoors for remote access (RAT -> Remote Access Trojan)
- Log keystrokes, steal credentials
- Download additional malware (dropper)
- Join the machine to a botnet

**Defense:** User education, application whitelisting, email filtering, code signing verification.

---

## Q9a. Buffer Overflow -> char user[10]; gets(user) (2+3+3+2 Marks)

**Question:** A C-based login uses `char user[10]; gets(user);`. Program crashes when >10 chars entered.
i. Identify vulnerability. ii. How can it be exploited? iii. Two coding practices to prevent it. iv. Why is gets() unsafe?

### i. Vulnerability: Buffer Overflow

The program allocates only **10 bytes** for `user` but uses `gets()` which reads **unlimited input**. Inputting >10 characters writes beyond the allocated buffer into adjacent memory -> a **Stack Buffer Overflow**.

### ii. How It Can Be Exploited

**Stack Layout during gets(user):**
```
[High address]
  Return Address  ? attacker overwrites this!
  Saved Frame Ptr
  user[9]
  user[8]
  ...
  user[0]         ? buffer starts here
[Low address]
```

**Attack (classic ret2shellcode):**
1. Attacker inputs 10+ chars: fills `user[0..9]`
2. Extra bytes overwrite saved frame pointer, then **return address**
3. Attacker places shellcode (e.g., `/bin/sh` launcher) in the buffer
4. Overwrite return address with buffer's address
5. When function returns ? jumps to shellcode ? **arbitrary code execution**

**Impact:** Remote code execution, privilege escalation, system takeover.

### iii. Two Coding Practices to Prevent

**1. Use `fgets()` instead of `gets()`:**
```c
// SAFE: limits input to buffer size - 1
fgets(user, sizeof(user), stdin);
// reads max 9 chars + null terminator
```

**2. Validate input length before processing:**
```c
char input[256];
fgets(input, sizeof(input), stdin);
if (strlen(input) >= sizeof(user)) {
    printf("Error: Username too long\n");
    exit(1);
}
strncpy(user, input, sizeof(user)-1);
user[sizeof(user)-1] = '\0'; // ensure null-termination
```

**Other mitigations:** Stack canaries (`-fstack-protector`), ASLR, DEP/NX bit, safe string libraries.

### iv. Why is gets() Unsafe?

`gets()` reads characters from stdin until a newline `\n` or EOF x **with NO bounds checking**. It has absolutely **no way to know** the size of the destination buffer. The C standard explicitly says:

> *"Never use gets(). Use fgets() instead."*

`gets()` was officially **removed from the C11 standard** because it is fundamentally impossible to use safely. Any input longer than the buffer causes undefined behavior.

### Depth of Understanding

| Concept | Detail |
|---|---|
| Buffer Overflow | Writing past allocated buffer boundary |
| Stack Smashing | Overwriting return address on the stack |
| Shellcode | Injected machine code (typically spawns a shell) |
| ASLR | Randomizes memory addresses -> harder to predict target |
| Stack Canary | Random value before return address -> checked before return |
| NX/DEP | Marks stack as non-executable -> shellcode can't run |

### Alternate Questions
1. What is a heap overflow? How does it differ from stack overflow?
2. Explain Return-Oriented Programming (ROP) and how it bypasses NX.
3. What is ASLR? How does it mitigate buffer overflow attacks?

---

## Q10a. SQL Injection Analysis (2+2+1+5 Marks)

**Given query:**
```sql
SELECT * FROM users WHERE username = 'USER_INPUT' AND password = 'USER_PASSWORD'
```
Attacker enters: `' OR '1'='1` in username field, blank password.

**Resulting query:**
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' AND password = ''
```

### i. What causes the SQL injection vulnerability?

The vulnerability is **direct string concatenation** of unvalidated user input into the SQL query. The application treats user input as part of the SQL command rather than as data. The single quote `'` terminates the string literal and allows injection of arbitrary SQL.

### ii. Potential Consequences

- **Authentication Bypass** -> attacker logs in without valid credentials
- **Data Exfiltration** -> UNION attacks to extract all table data
- **Data Modification** -> INSERT/UPDATE/DELETE via stacked queries
- **Database Destruction** -> DROP TABLE if permissions allow
- **OS Command Execution** -> via `xp_cmdshell` in MS SQL Server

### iii. Two Methods to Prevent SQL Injection

1. **Parameterized Queries (Prepared Statements):**
```python
cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
               (user_input, pass_input))
# Input treated as data -> never interpreted as SQL
```

2. **Input Validation + Whitelisting:**
```python
import re
if not re.match("^[a-zA-Z0-9_]+$", username):
    raise ValueError("Invalid username")
```

---

## Q10b. How SSL Ensures CIA in Secure Communication (5 Marks)

**Question:** Explain how SSL ensures confidentiality, integrity, and authentication.

### Answer

| CIA Goal | SSL Mechanism | How it Works |
|---|---|---|
| **Confidentiality** | Symmetric Encryption (AES-256) | After handshake, all data encrypted with session key. Eavesdroppers see only ciphertext. |
| **Integrity** | HMAC (SHA-256) | Each record includes a MAC. Any tampering changes the MAC ? receiver detects modification. |
| **Authentication** | X.509 Digital Certificates | Server proves identity via certificate signed by trusted CA. Client verifies before trusting. |

**In Detail:**

**Confidentiality:** During SSL handshake, client and server establish a shared **session key** (via RSA or ECDHE). All subsequent HTTP data is encrypted with AES using this key. Even if intercepted, the data is unreadable.

**Integrity:** Every SSL record includes a **MAC (Message Authentication Code)** computed using a shared MAC key (also derived during handshake). The receiver recomputes MAC and compares -> any bit change is detected. AES-GCM combines encryption and MAC in one step.

**Authentication:** The server presents a **digital certificate** signed by a Certificate Authority (CA). The client:
1. Verifies the CA signature (using CA's public key built into the browser)
2. Checks domain name matches
3. Checks certificate hasn't expired or been revoked (CRL/OCSP)

This prevents Man-in-the-Middle attacks -> an attacker cannot forge a valid certificate for a domain they don't own.

**Note:** Client authentication (mutual TLS) is optional -> server can also request client's certificate.

### Depth of Understanding
- **TLS 1.3** (latest): Removes RSA key exchange, mandates ECDHE ? perfect forward secrecy.
- **HSTS (HTTP Strict Transport Security):** Forces browsers to always use HTTPS -> prevents downgrade attacks.
- **Certificate Pinning:** App hardcodes expected certificate -> prevents rogue CA attacks.

### Alternate Questions
1. What is a Man-in-the-Middle attack on SSL? How do certificates prevent it?
2. What is certificate pinning and when is it used?
3. What is OCSP stapling? How does it improve SSL performance?

---

## Quick Revision Summary -> PYQ 2025

| Q | Topic | Key Answer |
|---|---|---|
| 1a | Primitive roots mod 26 | 26=2 x 13 ? roots exist; phi(phi(26))=phi(12)=4 roots: {7,11,15,19} |
| 1b | Abelian vs Group | Abelian adds commutativity; Identity unique by Bxzout proof |
| 2a | 3^160+5^(-1) mod 17 | FLT: 3^160=1; 5^(-1)=7; X=**8** |
| 2b | 4^x=13 mod 19 | ord(4)=9; 13??4? ? **No solution** |
| 2a-OR | 35x=1 mod 48 | Extended EA ? x=**11** |
| 2b-OR | COA | Only ciphertext available; statistical analysis used |
| 3a | CRT | x=2(3),3(5),2(7) ? x=**23** |
| 3a-OR | EC + GF(25) | 13 EC points; axb = **xx+x** |
| 4a | El-Gamal | KeyGen(p,g,x,y); Enc(C1=g^k,C2=Mxy^k); Dec(M=C2xC1^(-x)) |
| 5a | IBE | Identity=public key; PKG issues private keys; no certs needed |
| 5b | ABE | Policy-based; CP-ABE embeds policy in CT; fine-grained access |
| 6a | Shamir (3,4) mod 19 | Lagrange interpolation ? Secret = **5** |
| 7 | Network Security | CIA triad; Firewall=traffic filter; IDS=Signature/Anomaly |
| 8a | Worm vs Virus | Worm=self-propagating, no host; Virus=needs host file |
| 8b | Trojan | Enters via social engineering (fake downloads, email) |
| 9a | Buffer Overflow | gets() unchecked; use fgets(); overwrite return address |
| 10a | SQL Injection | OR 1=1 bypass; fix: Prepared statements |
| 10b | SSL CIA | AES?Confidentiality; HMAC?Integrity; X.509 Cert?Auth |
