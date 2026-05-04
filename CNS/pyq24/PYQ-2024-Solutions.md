# CNS PYQ 2024 — Complete Solutions
**Subject:** Cryptography and Network Security  
**Year:** 2024 | **Max Marks:** 100 | **Each Question:** 10 marks

---

## Q1. SQL Injection Attack — Code Segment Analysis (10 Marks)

**Question:**  
For the following program segment the webpage provides output based on the user input. Which type of attack is possible? Give an example and discuss the coding technique to withstand against that attack.

```java
uName = getRequestString("username");
uPass  = getRequestString("userpassword");

sql = 'SELECT * FROM Users WHERE Name ="' + uName +
      '" AND Pass ="' + uPass + '"'
```

---

### ✅ Answer

#### Attack Type: **SQL Injection**

SQL Injection is an attack where a malicious user inserts or "injects" specially crafted SQL code into an input field that is then executed by the database. The vulnerable code directly concatenates user input into the SQL query **without sanitization**.

---

#### How the Attack Works — Example

**Normal Login:**
- uName = `alice`, uPass = `secret123`
- Query: `SELECT * FROM Users WHERE Name="alice" AND Pass="secret123"`
- ✅ Works normally.

**Injected Login (bypass password):**
- uName = `admin" --`, uPass = `anything`
- Query becomes:
```sql
SELECT * FROM Users WHERE Name="admin" --" AND Pass="anything"
```
- The `--` is a SQL comment → everything after it is **ignored**
- ✅ Attacker logs in as `admin` without knowing the password!

**Another variant (always-true injection):**
- uName = `" OR "1"="1`, uPass = `" OR "1"="1`
- Query: `SELECT * FROM Users WHERE Name="" OR "1"="1" AND Pass="" OR "1"="1"`
- Since `"1"="1"` is always true → **returns all users**

---

#### Coding Techniques to Withstand SQL Injection

**1. Prepared Statements (Parameterized Queries) — Best Practice**
```java
// Java Example
String sql = "SELECT * FROM Users WHERE Name=? AND Pass=?";
PreparedStatement stmt = conn.prepareStatement(sql);
stmt.setString(1, uName);   // Input treated as data, NOT code
stmt.setString(2, uPass);
ResultSet rs = stmt.executeQuery();
```
> The `?` placeholders separate code from data. User input is **never interpreted as SQL**.

**2. Input Validation & Whitelisting**
```java
// Allow only alphanumeric characters
if (!uName.matches("[a-zA-Z0-9_]+")) {
    throw new Exception("Invalid username characters!");
}
```

**3. Stored Procedures**
```sql
CREATE PROCEDURE LoginUser(@Name VARCHAR(50), @Pass VARCHAR(50))
AS
    SELECT * FROM Users WHERE Name=@Name AND Pass=@Pass;
```
Input is passed as a parameter — not concatenated into the query.

**4. Escaping Special Characters**
- Escape characters like `'`, `"`, `--`, `;` before using in queries.
- Use library functions: `mysql_real_escape_string()` in PHP, etc.

**5. Principle of Least Privilege**
- Database user for the web app should have **only SELECT** rights — not DROP or DELETE.

---

### 🔍 Depth of Understanding

| Concept | Detail |
|---|---|
| Root Cause | String concatenation of unvalidated input into SQL |
| OWASP Rank | #1 on OWASP Top 10 Web Application Security Risks |
| Impact | Data leakage, Authentication bypass, DB destruction |
| Best Fix | Parameterized queries — input treated as literal data |
| Secondary Defense | WAF (Web Application Firewall) + Input validation |

> **Exam Tip:** Always say "Prepared Statements" as the primary defense. Mention that `--` causes line-comment injection and `OR 1=1` causes always-true bypass.

---

### 💡 Alternate Questions That Could Be Asked
1. What is the difference between SQL Injection and Blind SQL Injection?
2. How does a WAF help prevent SQL injection?
3. What is Second-Order SQL Injection? Give an example.
4. Why is input validation alone not sufficient to prevent SQL injection?

---

## Q2. RSA vs El-Gamal: Deterministic vs Randomized (10 Marks)

**Question:**  
Two well-known public key encryption algorithms are RSA and El-Gamal. Discuss which one is the deterministic encryption algorithm and which one is the randomized encryption algorithm. Justify your decision.

---

### ✅ Answer

#### RSA — Deterministic Encryption

In **RSA**, the encryption of a message `M` using public key `(e, n)` is:
```
C = M^e mod n
```
- There is **no random component** in the encryption formula.
- The **same plaintext M** always produces the **same ciphertext C** for a given key.
- RSA is therefore a **deterministic encryption algorithm**.

**Implication:** If an attacker suspects the plaintext is one of a small set (e.g., YES or NO), they can encrypt both with the public key and compare with intercepted ciphertext → **Chosen Plaintext Attack (CPA) succeeds**.

---

#### El-Gamal — Randomized Encryption

In **El-Gamal**, encryption requires choosing a **random ephemeral key `k`** each time:

Setup:
- Public key: `(p, g, y)` where `y = g^x mod p`, `x` = private key

Encryption of message `M`:
```
Choose random k
C1 = g^k mod p
C2 = M * y^k mod p
Ciphertext = (C1, C2)
```

- The **same plaintext M** encrypted twice with **different k** produces **different (C1, C2)** pairs.
- El-Gamal is therefore a **randomized (probabilistic) encryption algorithm**.
- It is **semantically secure** / **IND-CPA secure** (secure against Chosen Plaintext Attacks).

---

#### Summary Comparison

| Property | RSA | El-Gamal |
|---|---|---|
| Type | Deterministic | Randomized (Probabilistic) |
| Random Component | ❌ None | ✅ Random `k` each encryption |
| Same PT → Same CT? | ✅ Yes (for same key) | ❌ No (different `k` → different CT) |
| CPA Security | ❌ Not IND-CPA secure (textbook) | ✅ IND-CPA secure |
| Ciphertext Size | Equal to plaintext | **2x plaintext** (pair C1,C2) |
| Based On | Integer Factorization | Discrete Logarithm Problem |

---

### 🔍 Depth of Understanding

- **Textbook RSA** is deterministic but **RSA-OAEP** (with padding) is randomized and CPA-secure.
- El-Gamal's randomness comes from the **ephemeral key k** — if the same `k` is reused, security breaks (similar to nonce reuse in AES-GCM).
- The security of El-Gamal relies on the **Decisional Diffie-Hellman (DDH) problem**.
- Deterministic encryption always **leaks equality** — an attacker can tell if two ciphertexts encrypt the same message.

---

### 💡 Alternate Questions That Could Be Asked
1. What is semantic security (IND-CPA)? Which of RSA/El-Gamal satisfies it natively?
2. What happens to El-Gamal security if the same random `k` is used twice?
3. How does RSA-OAEP achieve probabilistic encryption?
4. What is the Decisional Diffie-Hellman problem and how does it relate to El-Gamal?

---

## Q3. Small Message Space Attack on RSA vs El-Gamal (10 Marks)

**Question:**  
A faculty conveys a grade (0–10) confidentially using a student's RSA public key.  
(a) Which type of attack is possible? Explain with reasons.  
(b) Whether the same attack is possible with El-Gamal cryptosystem? Why?

---

### ✅ Answer

#### (a) Attack on RSA — Exhaustive Search / Chosen Plaintext Attack

**Setup:**
- Grade is a value in {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10} — only **11 possible messages**.
- Faculty encrypts grade `G` using student's public key `(e, n)`:  
  `C = G^e mod n`

**Attack:**
Since RSA is **deterministic**, an attacker (another student) who intercepts `C` can:
1. Compute `C_i = i^e mod n` for all `i` in {0, 1, ..., 10} — only 11 computations needed.
2. Compare each `C_i` with intercepted `C`.
3. When `C_i = C` → grade is `i`. ✅

**This is a Chosen Plaintext Attack (CPA) / Exhaustive Search Attack.**

> **Root Cause:** RSA is deterministic **+** the message space is tiny (only 11 values). Both conditions together make the attack trivial.

---

#### (b) Is the Same Attack Possible with El-Gamal? No — Here's Why

In El-Gamal:
```
C = (C1, C2) = (g^k mod p, G * y^k mod p)
```
where `k` is a **fresh random number** for each encryption.

**Why attack fails:**
- Even if the attacker computes `C2_i = i * y^k mod p` for all 11 grades, they **do not know `k`**.
- Since `k` is different every time, computing `C1 = g^k` and relating it to `C2` is the **Discrete Logarithm Problem** — computationally infeasible.
- Even encrypting the same grade twice gives **completely different ciphertexts**.

**El-Gamal is IND-CPA secure** — the adversary cannot distinguish encryptions of any two messages, regardless of message space size.

---

### 🔍 Depth of Understanding

| Aspect | RSA | El-Gamal |
|---|---|---|
| Message Space Attack | ✅ Trivially feasible | ❌ Infeasible |
| Reason RSA Fails | Determinism → encrypt all, compare | Random `k` → no comparison possible |
| Formal Security | Not IND-CPA (textbook) | IND-CPA secure |
| Fix for RSA | Use RSA-OAEP padding (adds randomness) | N/A — inherently random |

> **Key Insight:** This is why deterministic encryption should **never** be used for small, guessable message spaces (passwords, grades, YES/NO decisions).

---

### 💡 Alternate Questions That Could Be Asked
1. What is a Chosen Ciphertext Attack (CCA)? Is El-Gamal secure against CCA?
2. A system uses RSA to encrypt a single bit (0 or 1). Describe the attack.
3. What is IND-CPA and IND-CCA security? Formally define them.
4. Why does RSA-OAEP resist the small message space attack?

---

## Q4. GF(2⁴) Polynomial Arithmetic (10 Marks)

**Question:**  
Compute A(x)+B(x) mod P(x) and A(x)xB(x) mod P(x) in GF(2⁴).  
**P(x) = x⁴ + x + 1**  
- Case 1: A(x) = x²+1, B(x) = x³+x²+1  
- Case 2: A(x) = x²+1, B(x) = x+1

---

### ✅ Answer

> **GF(2⁴) Rules:** All coefficients are in {0,1}. Addition = XOR (so 1+1=0, no carry). Multiplication = polynomial multiply, then reduce mod P(x).

---

#### Case 1: A(x) = x²+1, B(x) = x³+x²+1

**Addition: A(x) + B(x)**
```
  x² + 1
+ x³ + x² + 1
─────────────
  x³ + 0*x² + 0*1   (x²+x²=0, 1+1=0 in GF(2))
= x³
```
> **A(x) + B(x) = x³**  (no reduction needed, degree < 4)

---

**Multiplication: A(x) x B(x)**
```
(x²+1)(x³+x²+1)
= x²(x³+x²+1) + 1(x³+x²+1)
= x⁵ + x⁴ + x² + x³ + x² + 1
= x⁵ + x⁴ + x³ + (x²+x²) + 1
= x⁵ + x⁴ + x³ + 1        [since x²+x²=0]
```

**Reduce mod P(x) = x⁴+x+1:**

Since P(x) = 0 → **x⁴ = x + 1** (in GF(2))  
Therefore: **x⁵ = x * x⁴ = x(x+1) = x²+x**

Substituting:
```
x⁵ + x⁴ + x³ + 1
= (x²+x) + (x+1) + x³ + 1
= x³ + x² + (x+x) + (1+1)
= x³ + x² + 0 + 0
= x³ + x²
```
> **A(x) x B(x) mod P(x) = x³ + x²**

---

#### Case 2: A(x) = x²+1, B(x) = x+1

**Addition: A(x) + B(x)**
```
  x² + 1
+      x + 1
────────────
  x² + x + 0   (1+1=0)
= x² + x
```
> **A(x) + B(x) = x² + x**

---

**Multiplication: A(x) x B(x)**
```
(x²+1)(x+1)
= x²(x+1) + 1(x+1)
= x³ + x² + x + 1
```
Degree = 3 < 4, **no reduction needed**.

> **A(x) x B(x) mod P(x) = x³ + x² + x + 1**

---

#### Summary Table

| | Addition | Multiplication mod P(x) |
|---|---|---|
| **Case 1** | x³ | x³ + x² |
| **Case 2** | x² + x | x³ + x² + x + 1 |

---

### 🔍 Depth of Understanding

| Concept | Detail |
|---|---|
| Why GF(2⁴)? | Used in AES for SubBytes (operates in GF(2⁸)) and MixColumns |
| Irreducible Polynomial | P(x) must be irreducible over GF(2) — cannot be factored |
| Addition in GF(2ⁿ) | Coefficient-wise XOR — no carries |
| Multiplication | Polynomial multiply then reduce by P(x) — similar to modular arithmetic |
| x⁴ equiv x+1 | Because P(x)=0 → x⁴+x+1=0 → x⁴=x+1 in GF(2) |

> **AES Connection:** AES uses GF(2⁸) with P(x) = x⁸+x⁴+x³+x+1. Every byte in AES is an element of this field.

---

### 💡 Alternate Questions That Could Be Asked
1. Why must the modulus polynomial P(x) be irreducible in GF(2ⁿ)?
2. Find the multiplicative inverse of x²+1 in GF(2⁴) with P(x) = x⁴+x+1.
3. How is GF(2⁸) used in the AES MixColumns operation?
4. Compute (x³+x+1)² mod (x⁴+x+1) in GF(2⁴).

---

## Q5 (Option A). Extended Euclidean Algorithm (10 Marks)

**Question:**  
Using the extended Euclidean algorithm, compute the GCD and parameters s, t for:  
- (i) 198 and 243  
- (ii) 1819 and 3587

*(Note: s, t satisfy: gcd = s*a + t*b)*

---

### ✅ Answer

#### (i) GCD(198, 243) and s, t

**Step 1 — Euclidean Division:**

| Step | Equation | Quotient | Remainder |
|---|---|---|---|
| 1 | 243 = **1**x198 + **45** | 1 | 45 |
| 2 | 198 = **4**x45 + **18** | 4 | 18 |
| 3 | 45 = **2**x18 + **9** | 2 | 9 |
| 4 | 18 = **2**x9 + **0** | 2 | 0 |

**GCD(198, 243) = 9**

**Step 2 — Back-Substitution:**
```
9 = 45 - 2x18                                     ... from Step 3
18 = 198 - 4x45                                    ... from Step 2
9 = 45 - 2x(198 - 4x45) = 9x45 - 2x198            ... substitute
45 = 243 - 1x198                                   ... from Step 1
9 = 9x(243 - 198) - 2x198 = 9x243 - 11x198        ... substitute
```

**Result:**
```
9 = (-11)x198 + (9)x243
```
> **s = -11, t = 9**  
> **Verification:** (-11)x198 + 9x243 = -2178 + 2187 = **9** ✓

---

#### (ii) GCD(1819, 3587) and s, t

**Step 1 — Euclidean Division:**

| Step | Equation | Quotient | Remainder |
|---|---|---|---|
| 1 | 3587 = **1**x1819 + **1768** | 1 | 1768 |
| 2 | 1819 = **1**x1768 + **51** | 1 | 51 |
| 3 | 1768 = **34**x51 + **34** | 34 | 34 |
| 4 | 51 = **1**x34 + **17** | 1 | 17 |
| 5 | 34 = **2**x17 + **0** | 2 | 0 |

**GCD(1819, 3587) = 17**

**Step 2 — Back-Substitution:**
```
17 = 51 - 1x34                                              ... from Step 4
34 = 1768 - 34x51                                           ... from Step 3
17 = 51 - 1x(1768 - 34x51) = 35x51 - 1768                  ... substitute
51 = 1819 - 1x1768                                          ... from Step 2
17 = 35x(1819 - 1768) - 1768 = 35x1819 - 36x1768           ... substitute
1768 = 3587 - 1x1819                                        ... from Step 1
17 = 35x1819 - 36x(3587 - 1819) = 71x1819 - 36x3587        ... substitute
```

**Result:**
```
17 = (71)x1819 + (-36)x3587
```
> **s = 71, t = -36**  
> **Verification:** 71x1819 + (-36)x3587 = 129149 - 129132 = **17** ✓

---

### 🔍 Depth of Understanding

| Concept | Detail |
|---|---|
| Bézout's Identity | For any a,b: gcd(a,b) = s*a + t*b always has integer solutions s,t |
| Use in Cryptography | Finding modular inverse: if gcd(a,n)=1, then s from extended EA gives a⁻¹ mod n |
| RSA Connection | Used to compute private key d = e⁻¹ mod φ(n) |
| Time Complexity | O(log min(a,b)) — very efficient |
| Negative s or t? | Perfectly valid — means subtraction in the linear combination |

---

### 💡 Alternate Questions That Could Be Asked
1. Use extended EA to find 7⁻¹ mod 26 (classic cipher key computation).
2. Verify that gcd(35, 78) = 1 and find s, t. Use it to find 35⁻¹ mod 78.
3. Why must gcd(e, φ(n)) = 1 in RSA, and how is extended EA used to find d?
4. What is Bézout's Identity? State and prove it.

---

## Q5 (Option B). Fast Exponentiation -> Square and Multiply (10 Marks)

**Question:** Compute x^e mod m using square-and-multiply:
- x=2, e=79, m=101
- x=3, e=197, m=101

---

### Answer

> **Algorithm:** Convert e to binary. Scan bits left to right. For each bit: square result. If bit=1, multiply by x. Reduce mod m at each step.

#### (i) 2^79 mod 101

79 in binary = **10011112** (7 bits)

| Bit | Operation | Result mod 101 |
|-----|-----------|---------------|
| 1 (MSB) | init=1, x2 | 2 |
| 0 | 2^(-1)=4 | 4 |
| 0 | 4^(-1)=16 | 16 |
| 1 | 16^(-1)=256=54, x2=108=7 | 7 |
| 1 | 7^(-1)=49, x2=98 | 98 |
| 1 | 98^(-1)=9604=9, x2=18 | 18 |
| 1 | 18^(-1)=324=21, x2=42 | 42 |

> **2^79 mod 101 = 42**

**Verify 79 in binary:** 64+8+4+2+1 = 79 ?  
**Check:** 9604 mod 101 ? 9604 = 95 x 101+9 ? 9 ?  
324 mod 101 ? 3 x 101=303 ? 324-303=21 ?

---

#### (ii) 3^197 mod 101

197 in binary = **110001012** (8 bits) ? 128+64+4+1=197 ?

| Bit | Operation | Result mod 101 |
|-----|-----------|---------------|
| 1 | init=1, x3 | 3 |
| 1 | 3^(-1)=9, x3=27 | 27 |
| 0 | 27^(-1)=729=22 | 22 |
| 0 | 22^(-1)=484=80 | 80 |
| 0 | 80^(-1)=6400=37 | 37 |
| 1 | 37^(-1)=1369=56, x3=168=67 | 67 |
| 0 | 67^(-1)=4489=45 | 45 |
| 1 | 45^(-1)=2025=5, x3=15 | 15 |

> **3^197 mod 101 = 15**

**Key mod computations:**
- 729 mod 101: 7 x 101=707, 729-707=**22** ?
- 484 mod 101: 4 x 101=404, 484-404=**80** ?
- 6400 mod 101: 63 x 101=6363, 6400-6363=**37** ?
- 1369 mod 101: 13 x 101=1313, 1369-1313=**56** ?
- 4489 mod 101: 44 x 101=4444, 4489-4444=**45** ?
- 2025 mod 101: 20 x 101=2020, 2025-2020=**5** ?

---

### Depth of Understanding

| Concept | Detail |
|---|---|
| Why Square-and-Multiply? | Reduces O(e) multiplications to O(log e) |
| For e=79 (7 bits) | 6 squares + 4 multiplies = 10 ops vs 79 naxve |
| Usage | RSA encryption/decryption, Diffie-Hellman |
| Timing Attack Risk | Non-constant time -> if-bit=1 branch leaks key bits |
| Defense | Montgomery ladder -> always square AND multiply |

### Alternate Questions
1. Compute 5^11 mod 13 using square-and-multiply. Show all steps.
2. How does the square-and-multiply algorithm relate to RSA decryption efficiency?
3. What is a timing side-channel attack on fast exponentiation? How is it mitigated?

---

## Q6 (Option A). SSL Protocol and Handshake (10 Marks)

**Question:** The SSL Protocol aids security in HTTP. Justify this statement. Describe the handshake in SSL Protocol.

---

### Answer

#### How SSL/TLS Secures HTTP

HTTP alone transmits data in **plaintext** -> any eavesdropper can read passwords, cookies, and sensitive data. SSL (Secure Sockets Layer) / TLS wraps HTTP with:

| Security Goal | SSL Mechanism |
|---|---|
| **Confidentiality** | Symmetric encryption (AES) of all data |
| **Integrity** | MAC (Message Authentication Code) / HMAC |
| **Authentication** | X.509 digital certificates (server identity) |
| **Key Exchange** | Public-key crypto (RSA/ECDH) to share session key |

This transforms HTTP ? **HTTPS** (HTTP over SSL/TLS).

---

#### SSL Handshake -> Step by Step

```
Client                                Server
  |                                     |
  |------- 1. ClientHello ------------>|
  |   (TLS version, cipher suites,      |
  |    client_random)                   |
  |                                     |
  |<------ 2. ServerHello -------------|
  |   (chosen cipher suite,             |
  |    server_random, session ID)       |
  |                                     |
  |<------ 3. Certificate -------------|
  |   (server's X.509 certificate)      |
  |                                     |
  |<------ 4. ServerHelloDone ---------|
  |                                     |
  |------- 5. ClientKeyExchange ------>|
  |   (Pre-Master Secret encrypted      |
  |    with server's public key)        |
  |                                     |
  [Both derive Master Secret & Session Keys]
  [Master Secret = PRF(pre_master, client_random, server_random)]
  |                                     |
  |------- 6. ChangeCipherSpec ------->|
  |------- 7. Finished (encrypted) --->|
  |                                     |
  |<------ 8. ChangeCipherSpec --------|
  |<------ 9. Finished (encrypted) ----|
  |                                     |
  |====== Encrypted HTTPS Data ========|
```

**Key Steps Explained:**

1. **ClientHello** -> Client announces supported TLS versions, cipher suites (e.g., TLS_RSA_WITH_AES_128), and sends a random nonce.
2. **ServerHello** -> Server picks the best cipher suite, sends its own nonce.
3. **Certificate** -> Server sends its digital certificate (contains server's public key, signed by a CA).
4. **Client verifies** the certificate against trusted CAs.
5. **ClientKeyExchange** -> Client generates a Pre-Master Secret, encrypts it with server's public key, sends it.
6. **Key Derivation** -> Both sides independently derive the same session key using PRF over (pre-master + both randoms).
7. **ChangeCipherSpec + Finished** -> Both sides confirm switching to encrypted mode. The Finished message is a hash of all handshake messages.

---

### Depth of Understanding

- **Why two random nonces?** Prevents replay attacks -> an old recording of a handshake cannot be reused.
- **Forward Secrecy:** Modern TLS uses ECDHE (ephemeral Diffie-Hellman) so even if the server's private key is later compromised, past sessions remain secure.
- **Certificate Chain:** Server cert ? Intermediate CA ? Root CA. Browser trusts Root CAs pre-installed.
- **TLS 1.3 Change:** Eliminates RSA key exchange entirely; mandates ECDHE for forward secrecy.

### Alternate Questions
1. What is the difference between SSL 3.0 and TLS 1.3?
2. What is Perfect Forward Secrecy and how does ECDHE provide it?
3. Explain man-in-the-middle attacks on SSL and how certificates prevent them.

---

## Q6 (Option B). Hybrid Encryption -> Public + Symmetric (10 Marks)

**Question:** For secure communication over a public channel, we need to use the combination of public and symmetric key encryption. Is it true? Why?

---

### Answer

**Yes, it is true.** This combination is called **Hybrid Encryption** and is the foundation of all modern secure protocols (TLS, PGP, SSH).

#### Why Pure Symmetric Encryption Fails
- Requires a **shared secret key** to be established beforehand.
- Over a public channel, how do two strangers exchange a key securely? ? **Key Distribution Problem**.

#### Why Pure Asymmetric Encryption Fails
- RSA/El-Gamal are **1000^(-1) slower** than AES for bulk data.
- El-Gamal **doubles** ciphertext size.
- Not suitable for encrypting large files or streams.

#### Hybrid Solution

```
Step 1: Key Exchange (Asymmetric)
  - Sender encrypts a random symmetric key K using recipient's PUBLIC KEY
  - C_key = E_pub(K)

Step 2: Bulk Encryption (Symmetric)
  - Sender encrypts actual message M using AES with key K
  - C_msg = AES_K(M)

Step 3: Transmission
  - Send (C_key, C_msg)

Step 4: Decryption
  - Recipient decrypts C_key using PRIVATE KEY ? recovers K
  - Decrypts C_msg using AES with K ? recovers M
```

| Layer | Algorithm | Purpose |
|---|---|---|
| Key Wrapping | RSA / ECDH | Securely transmit symmetric key |
| Data Encryption | AES-256-GCM | Fast bulk encryption |
| Integrity | HMAC-SHA256 | Message authentication |

**Examples:** TLS, PGP, SSH all use hybrid encryption.

### Depth of Understanding
- The symmetric key used is called a **session key** -> ephemeral, used for one session only.
- Using a new session key every time provides **forward secrecy** (if key is compromised, only that session is affected).
- AES-GCM provides both confidentiality AND integrity in one pass -> no separate MAC needed.

### Alternate Questions
1. What is the key encapsulation mechanism (KEM)? How does it relate to hybrid encryption?
2. Why is ECDH preferred over RSA for key exchange in modern systems?

---

## Q7. Cryptographically Secure PRNG -> Two Tests (10 Marks)

**Question:** List the two tests that a pseudorandom number generator must pass to become a cryptographically secure random number generator.

---

### Answer

A PRNG that passes general statistical tests (NIST, Diehard) is **statistically random** but NOT necessarily **cryptographically secure**. To be a **CSPRNG**, it must additionally pass:

---

#### Test 1: The Next-Bit Test (Unpredictability)

**Definition:** A PRNG passes the next-bit test if there is **no polynomial-time algorithm** that, given the first k bits of the output sequence, can predict the (k+1)th bit with probability greater than **1/2 + negligible(k)**.

**Why it matters:**
- A regular PRNG like a Linear Congruential Generator (LCG) can be fully predicted from just a few output bits by solving linear equations.
- A CSPRNG's output must be **computationally indistinguishable from true randomness**.

**Formal statement (Yao, 1982):** A PRNG is CSPRNG if and only if it passes all polynomial-time statistical tests, which is equivalent to passing the next-bit test.

---

#### Test 2: State Compromise Resistance (Backward Security)

**Definition:** Even if an adversary learns the **current internal state** of the PRNG, they cannot:
- Reconstruct any **previous** output sequences (backward security).
- *(Forward security is also desirable -> future outputs cannot be predicted after state compromise if the state is updated.)*

**Why it matters:**
- An LCG is completely reversible: knowing x_n lets you compute x_{n-1}, x_{n-2}, etc.
- A CSPRNG must use **one-way functions** in its state transition so the state cannot be inverted.

**Example:** Blum Blum Shub (BBS) -> state x_{n+1} = x_n-> mod (pxq). Reversing requires factoring n = pxq.

---

### Summary Table

| Test | Requirement | Fails If |
|---|---|---|
| Next-Bit Test | No poly-time predictor for next bit | Output has statistical patterns |
| State Compromise | Past outputs unrecoverable from current state | State transition is invertible |

### Depth of Understanding

- **NIST SP 800-90A** defines approved CSPRNGs: Hash_DRBG, HMAC_DRBG, CTR_DRBG.
- The Dual_EC_DRBG (NIST) was backdoored by NSA -> it passed statistical tests but was not truly unpredictable to the designer.
- **/dev/urandom** in Linux is a CSPRNG -> seeded from hardware entropy, uses ChaCha20.
- The next-bit test is equivalent to semantic security of the PRNG's output.

### Alternate Questions
1. What is the Blum Blum Shub generator? Prove it passes the next-bit test.
2. What is the difference between /dev/random and /dev/urandom in Linux?
3. Why was Dual_EC_DRBG considered backdoored? What does this teach about CSPRNG design?
4. Define forward security and backward security for PRNGs.

---

## Q8. Do Any Two -> Elliptic Curve, Shamir, CRT (10 Marks)

### Part (a): Elliptic Curve Points for E: yx = xx + 5 (mod 7)

#### Method: Test x = 0 to 6, compute RHS, check if it's a quadratic residue mod 7

**Quadratic Residues mod 7:** {1^(-1)=1, 2^(-1)=4, 3^(-1)=2, 4^(-1)=2, 5^(-1)=4, 6^(-1)=1} ? QR = {0,1,2,4}

| x | xx+5 mod 7 | Is QR mod 7? | y values | Points |
|---|---|---|---|---|
| 0 | 0+5=5 | ? No | x | x |
| 1 | 1+5=6 | ? No | x | x |
| 2 | 8+5=13=6 | ? No | x | x |
| 3 | 27+5=32=4 | ? Yes | y=2,5 | (3,2),(3,5) |
| 4 | 64+5=69=6 | ? No | x | x |
| 5 | 125+5=130=4 | ? Yes | y=2,5 | (5,2),(5,5) |
| 6 | 216+5=221=4 | ? Yes | y=2,5 | (6,2),(6,5) |

**Verification of mod reductions:**
- x=3: 32 mod 7 = 32-4 x 7 = 32-28 = **4** ?
- x=5: 130 mod 7 = 130-18 x 7 = 130-126 = **4** ?
- x=6: 221 mod 7 = 221-31 x 7 = 221-217 = **4** ?

**y values for RHS=4:** 2^(-1)=4 and 5^(-1)=25=4 mod 7 ? y = 2 or 5

> **All Points on E: {O, (3,2), (3,5), (5,2), (5,5), (6,2), (6,5)}**  
> Total = **7 points** (including point at infinity O)

---

### Part (b): Shamir (3,5) Secret Sharing -> p=17, Shares: (1,8),(3,10),(5,11)

**Goal:** Find secret = f(0) using Lagrange interpolation mod 17.

f(x) = a0 + a1x + a2x-> mod 17, using shares (x1,y1)=(1,8), (x2,y2)=(3,10), (x3,y3)=(5,11)

**Lagrange Basis at x=0:**

```
L1(0) = [(0-3)(0-5)] / [(1-3)(1-5)]
       = [(-3)(-5)] / [(-2)(-4)]
       = 15/8 mod 17

L3(0) = [(0-1)(0-5)] / [(3-1)(3-5)]
       = [(-1)(-5)] / [(2)(-2)]
       = 5/(-4) mod 17

L5(0) = [(0-1)(0-3)] / [(5-1)(5-3)]
       = [(-1)(-3)] / [(4)(2)]
       = 3/8 mod 17
```

**Modular Inverses:**
- 8?-> mod 17: 8 x 15=120=7 x 17+1 ? **8?x = 15**
- (-4) mod 17 = 13; 13?-> mod 17: 13 x 4=52=3 x 17+1 ? **13?x = 4**

**Compute Basis Values:**
- L1(0) = 15 x 15 mod 17 = 225 mod 17 = 225-13 x 17 = **4**
- L3(0) = 5 x 4 mod 17 = 20 mod 17 = **3**
- L5(0) = 3 x 15 mod 17 = 45 mod 17 = 45-2 x 17 = **11**

**Secret = f(0):**
```
f(0) = y1xL1(0) + y2xL3(0) + y3xL5(0) mod 17
     = 8 x 4 + 10 x 3 + 11 x 11 mod 17
     = 32 + 30 + 121 mod 17
     = 183 mod 17
     = 183 - 10 x 17 = 183 - 170 = 13
```

> **Secret = 13**

**Verification:** f(x) = 13 + 10x + 2x-> mod 17
- f(1) = 13+10+2 = 25 mod 17 = **8** ?
- f(3) = 13+30+18 = 61 mod 17 = 61-3 x 17 = **10** ?
- f(5) = 13+50+50 = 113 mod 17 = 113-6 x 17 = **11** ?

---

### Part (c): Chinese Remainder Theorem

**System:** x = 2 (mod 5), x = 3 (mod 7), x = 10 (mod 11)

**Step 1:** M = 5 x 7x11 = **385**

**Step 2:** M1 = 385/5 = 77, M2 = 385/7 = 55, M3 = 385/11 = 35

**Step 3:** Find inverses y? = M??-> mod m?:
- y1 = 77?-> mod 5: 77 mod 5 = 2, 2?-> mod 5 = 3 (since 2 x 3=6=1) ? **y1=3**
- y2 = 55?-> mod 7: 55 mod 7 = 6, 6?-> mod 7 = 6 (since 6 x 6=36=1) ? **y2=6**
- y3 = 35?-> mod 11: 35 mod 11 = 2, 2?-> mod 11 = 6 (since 2 x 6=12=1) ? **y3=6**

**Step 4:**
```
x = (a1M1y1 + a2M2y2 + a3M3y3) mod M
  = (2 x 77 x 3 + 3 x 55 x 6 + 10 x 35 x 6) mod 385
  = (462 + 990 + 2100) mod 385
  = 3552 mod 385
  = 3552 - 9 x 385 = 3552 - 3465 = 87
```

> **x = 87**

**Verify:** 87 mod 5=2 ?, 87 mod 7=87-84=3 ?, 87 mod 11=87-77=10 ?

---

## Q9. Shamir (3,5) Secret Sharing -> Full Lagrange Polynomial (10 Marks)

*(Same calculation as Q8b -> this is the standalone version with full polynomial reconstruction)*

**Shares given:** (1,8), (3,10), (5,11), p=17, threshold t=3, total n=5

The full polynomial is f(x) = **13 + 10x + 2xx** mod 17

*(All steps are identical to Q8b above -> refer for complete working)*

**Key points to highlight in exam:**
- This is a **(3,5) scheme** ? any 3 of 5 shares can reconstruct; 2 shares reveal nothing.
- The secret is the **constant term** f(0) = **13**.
- Lagrange interpolation works in any finite field -> here mod prime p=17.
- Security: with fewer than t=3 shares, the system is **information-theoretically secure** (not just computationally).

### Depth of Understanding

| Concept | Detail |
|---|---|
| (t,n) Scheme | t = threshold (min shares to reconstruct), n = total shares |
| Security Basis | Information-theoretic -> not based on computational hardness |
| Why prime modulus? | Ensures Z? is a field -> every nonzero element has an inverse |
| Lagrange Interpolation | Unique degree-(t-1) polynomial through t points |
| Verifiable SSS | Feldman's scheme adds commitments to detect cheating shareholders |

### Alternate Questions
1. In a (2,4) Shamir scheme with p=7, shares (1,3),(2,5). Find the secret.
2. What is the security guarantee of Shamir's scheme when only t-1 shares are known?
3. What is Feldman's Verifiable Secret Sharing? How does it improve Shamir's scheme?
4. Can Shamir's scheme be used over non-prime moduli? Why or why not?

---

## Q10. Identity-Based vs Attribute-Based Encryption (10 Marks)

**Question:** Compare: Identity-based encryption vs Attribute-based encryption. Provide reasons for your selection in each scenario.

---

### Answer

#### Identity-Based Encryption (IBE)

**Core Idea:** A user's **public key = their identity string** (e.g., email, employee ID). No certificates needed.

**Setup:**
- **PKG** (Private Key Generator) holds master secret.
- To encrypt to alice@company.com: `C = Encrypt("alice@company.com", M)`
- Alice requests her private key from PKG (after authentication).
- Alice decrypts: `M = Decrypt(sk_alice, C)`

**Properties:**
- ? No certificate management (no PKI overhead)
- ? Sender can encrypt without recipient ever registering first
- ? Key escrow problem -> PKG knows all private keys
- ? No fine-grained access control
- Based on: Bilinear pairings (Boneh-Franklin IBE)

---

#### Attribute-Based Encryption (ABE)

**Core Idea:** Keys and/or ciphertexts are associated with **sets of attributes** and **access policies**.

**Two types:**
1. **KP-ABE (Key-Policy ABE):** Key has policy, ciphertext has attributes.
2. **CP-ABE (Ciphertext-Policy ABE):** Ciphertext has policy, key has attributes.

**Example (CP-ABE):**  
Policy: `(Role=Doctor) AND (Department=Cardiology) OR (Clearance=High)`  
Only users whose attributes satisfy this policy can decrypt.

**Properties:**
- ? Fine-grained, expressive access control
- ? One encryption for multiple authorized users
- ? Complex key management
- ? Computationally heavier than IBE

---

#### Scenario Comparison

| Scenario | Choose | Reason |
|---|---|---|
| Email encryption in small company | **IBE** | Email = identity, no complex policies needed |
| Healthcare records: only "Cardiologist in ICU" can read | **ABE** | Role+department policy -> only ABE can express this |
| Cloud storage with role-based access | **ABE** | Multiple attribute conditions per ciphertext |
| Encrypt to future employee before they join | **IBE** | Identity (email) known even before key is issued |
| IoT device authentication by device ID | **IBE** | Device ID as identity, no PKI needed |
| Government document: "Top Secret AND Need-to-Know" | **ABE** | Conjunction of clearance attributes |

---

### Depth of Understanding

| Feature | IBE | ABE |
|---|---|---|
| Public Key | Identity string | Attribute set |
| Access Policy | Fixed (one recipient) | Expressive (AND/OR of attributes) |
| Key Escrow | ? Yes (PKG issue) | ? Yes (authority issue) |
| Expressiveness | Low | High |
| Overhead | Moderate | High |
| Standard Use | Email, device auth | Healthcare, cloud, gov |
| Mathematical Basis | Bilinear pairings | Bilinear pairings + secret sharing |

### Alternate Questions
1. What is the key escrow problem in IBE? How can it be mitigated?
2. Explain KP-ABE vs CP-ABE with examples.
3. How is Shamir's Secret Sharing used inside ABE constructions?
4. What is Hierarchical IBE (HIBE) and when is it preferred over flat IBE?

---

## Quick Revision Summary

| Q | Topic | Key Answer |
|---|---|---|
| 1 | SQL Injection | Use Prepared Statements; `--` bypasses auth |
| 2 | RSA vs El-Gamal | RSA=deterministic; El-Gamal=randomized (random k) |
| 3 | Small message attack | CPA on RSA (11 values); El-Gamal immune (random k) |
| 4 | GF(24) arithmetic | Case1: +?xx, x?xx+xx; Case2: +?xx+x, x?xx+xx+x+1 |
| 5A | Extended Euclidean | gcd(198,243)=9, s=-11,t=9; gcd(1819,3587)=17, s=71,t=-36 |
| 5B | Fast Exponentiation | 2^79 mod 101=42; 3^197 mod 101=15 |
| 6A | SSL Handshake | 9-step handshake: Hello?Cert?KeyExchange?Finished |
| 6B | Hybrid Encryption | Public key wraps session key; AES encrypts data |
| 7 | CSPRNG Tests | (1) Next-bit test (2) State compromise resistance |
| 8/9 | Shamir + CRT + EC | Secret=13; x=87; EC Points: {O,(3,2),(3,5),(5,2),(5,5),(6,2),(6,5)} |
| 10 | IBE vs ABE | IBE=identity-based simple auth; ABE=policy-based fine-grained |

---

# APPENDIX: Alternate Questions -> Answered (PYQ 2024)

---

## Q1 Alternates Answered -> SQL Injection

**1. What is the difference between SQL Injection and Blind SQL Injection?**

| | SQL Injection | Blind SQL Injection |
|---|---|---|
| Visibility | Error messages or data returned directly | No visible output -> attacker infers from app behavior |
| Technique | Direct data extraction via UNION, error | Boolean-based (true/false responses) or Time-based (SLEEP) |
| Example | `UNION SELECT username,password FROM users` | `' AND SLEEP(5)--` -> if page delays, condition is true |
| Difficulty | Easier | Harder but equally dangerous |

**2. How does a WAF help prevent SQL injection?**
A Web Application Firewall (WAF) sits between the client and server and inspects HTTP requests against a ruleset:
- Detects known SQL keywords (`UNION`, `SELECT`, `DROP`, `--`) in input fields
- Blocks or sanitizes suspicious requests before they reach the application
- Uses both signature-based (known attack patterns) and anomaly-based detection
- **Limitation:** WAFs can be bypassed using encoding (URL encoding, hex encoding) -> they are a defense-in-depth measure, NOT a replacement for parameterized queries.

**3. What is Second-Order SQL Injection? Give an example.**
Second-Order SQL Injection occurs when malicious input is **stored** in the database first (seemingly safe), and then **retrieved and used unsafely** in a subsequent SQL query.

Example:
```
Step 1 -> Registration (stored safely):
  Username: admin'--
  Safely escaped and stored in DB: admin'--

Step 2 -> Password change (used unsafely):
  sql = "UPDATE users SET pass='" + newpass + "' WHERE user='" + stored_username + "'"
  ? UPDATE users SET pass='x' WHERE user='admin'--'
  ? Updates admin's password! (-- comments out the rest)
```
The injection happens at retrieval time, not at input time -> evading input-time sanitization.

**4. Why is input validation alone not sufficient to prevent SQL injection?**
- Input validation checks format (e.g., no special chars) but attackers use **encoding tricks**: `%27` = `'`, `0x27` = `'`, double-encoding, etc.
- Validation is **context-unaware** -> a username with apostrophe (`O'Brien`) is valid but breaks unsafe SQL.
- Blacklisting SQL keywords fails: attackers use `/**/`, `CONCAT()`, or case variation (`SeLeCt`).
- **Parameterized queries** separate code from data at the database driver level -> no bypass possible regardless of input content.

---

## Q2 Alternates Answered -> RSA vs El-Gamal

**1. What is semantic security (IND-CPA)? Which satisfies it natively?**

**IND-CPA (Indistinguishability under Chosen Plaintext Attack):**
A scheme is IND-CPA secure if no polynomial-time adversary can win the following game with probability > 1/2 + negligible:
1. Adversary picks two messages m0, m1
2. Challenger encrypts one: C = Enc(m?) for random b ? {0,1}
3. Adversary must guess b

**RSA (textbook):** NOT IND-CPA secure. Same m always gives same C ? adversary encrypts m0 and m1, compares with C.
**El-Gamal:** ? IND-CPA secure. Random k means Enc(m0) ? Enc(m0) across runs -> adversary cannot distinguish.

**2. What happens to El-Gamal security if the same k is used twice?**

If k is reused for two messages M1 and M2:
- C1 = g^k (same both times)
- C2 = M1xy^k and C2' = M2xy^k

Attacker observes same C1 ? knows same k was used:
```
C2 / C2' = (M1xy^k) / (M2xy^k) = M1/M2 mod p
```
If M1 is known, M2 = M1x(C2'/C2) mod p -> immediately recovered!
This is identical to the **two-time pad problem** in stream ciphers.

**3. How does RSA-OAEP achieve probabilistic encryption?**
OAEP (Optimal Asymmetric Encryption Padding) adds randomness before RSA encryption:
```
Input: Message M, random seed r
1. Pad M with r using two hash functions (MGF -> Mask Generation Function)
2. Produce padded message M' = OAEP(M, r)
3. Encrypt: C = (M')^e mod n
```
Different r each time ? different C even for same M ? probabilistic. RSA-OAEP is IND-CCA2 secure (proven secure against adaptive chosen ciphertext attacks).

**4. What is the DDH problem and its relation to El-Gamal?**
**Decisional Diffie-Hellman (DDH):** Given (g, g^a, g^b, g^c) in a group, determine if c = ab mod (p-1) or c is random. This is believed to be computationally hard.

El-Gamal security **reduces to DDH**: Breaking El-Gamal IND-CPA means distinguishing (g^k, Mxy^k) from (g^k, Rxy^k) for random R -> equivalent to solving DDH.

---

## Q3 Alternates Answered -> Small Message Space

**1. What is a CCA? Is El-Gamal secure against CCA?**
**Chosen Ciphertext Attack (CCA):** Adversary can submit ciphertexts to a decryption oracle and receive plaintexts, except for the target ciphertext.

**El-Gamal is NOT CCA secure** -> it is **malleable**:
Given valid ciphertext (C1, C2) = Enc(M):
- Attacker constructs (C1, 2xC2 mod p) -> this decrypts to 2M
- Attacker can submit this to decryption oracle, get 2M, then compute M
- This breaks CCA security

Fix: Use **DHAES/ECIES** (El-Gamal with integrity protection) for CCA security.

**2. A system uses RSA to encrypt a single bit (0 or 1). Describe the attack.**
Bit message space = {0, 1}. Attacker:
1. Compute C0 = 0^e mod n = 0
2. Compute C1 = 1^e mod n = 1
3. If intercepted C = 0 ? message is 0; if C = 1 ? message is 1
Trivially broken -> RSA of 0 is always 0, RSA of 1 is always 1.

**3. What is IND-CPA and IND-CCA? Define formally.**
- **IND-CPA:** Adversary with encryption oracle cannot distinguish Enc(m0) from Enc(m1) for chosen m0,m1.
- **IND-CCA1 (Lunchtime):** Adversary has decryption oracle access before seeing challenge ciphertext.
- **IND-CCA2 (Adaptive):** Adversary has decryption oracle before AND after challenge ciphertext (cannot query challenge itself).
IND-CCA2 ? IND-CCA1 ? IND-CPA (strictly stronger each time).

**4. Why does RSA-OAEP resist small message space attack?**
RSA-OAEP pads M with a random value r before encryption. Even if M ? {0,1,...,10}, the padded message M' = OAEP(M,r) is different each time (due to random r). Attacker cannot pre-compute and compare ciphertexts because they don't know r.

---

## Q4 Alternates Answered -> GF(24)

**1. Why must P(x) be irreducible in GF(2n)?**
GF(2n) is a field -> every nonzero element must have a multiplicative inverse. If P(x) = A(x)xB(x) is reducible, then A(x) mod P(x) ? 0 but A(x)xB(x) = 0 mod P(x). So A(x) is a zero divisor -> no inverse exists. A ring with zero divisors is NOT a field. Irreducibility guarantees no zero divisors, making it a valid field.

**2. Find (xx+1)?-> in GF(24) with P(x) = x4+x+1**

Use Extended Euclidean Algorithm on polynomials:
```
x4+x+1 = xxx(xx+1) + (xx+x+1)     ... Step 1
xx+1    = 1x(xx+x+1) + x             ... Step 2  [GF(2): 1+1=0]
xx+x+1  = (x+1)xx + 1               ... Step 3
```
GCD = 1. Back-substitute:
```
1 = (xx+x+1) - (x+1)xx                          [from Step 3]
x = (xx+1) + (xx+x+1)                            [from Step 2, GF(2)]
1 = (xx+x+1) - (x+1)x[(xx+1)+(xx+x+1)]
  = (xx+x+1)xx + (x+1)x(xx+1)                   [GF(2) arithmetic]
xx+x+1 = (x4+x+1) + xxx(xx+1)                  [from Step 1]
1 = xx(x4+x+1) + (xx+x+1)x(xx+1)
```
> **(xx+1)?x = xx+x+1**

**Verify:** (xx+1)(xx+x+1) = x5+xx+xx+xx+x+1 = x5+xx+x+1
x5 = xx+x (since x4=x+1 ? x5=xx+x) ? (xx+x)+xx+x+1 = 1 ?

**3. How is GF(28) used in AES MixColumns?**
In AES, each byte is an element of GF(28) with P(x)=x8+x4+xx+x+1. MixColumns treats each column of the 4 x 4 state matrix as a vector of 4 GF(28) elements and multiplies by a fixed MDS matrix:
```
[2 3 1 1]   [b0]   [b0']
[1 2 3 1] x [b1] = [b1']  (all operations in GF(28))
[1 1 2 3]   [b2]   [b2']
[3 1 1 2]   [b3]   [b3']
```
Multiplication by 2 = left shift + conditional XOR with 0x1B (if high bit was 1). Provides **diffusion** -> each output byte depends on all 4 input bytes.

**4. Compute (xx+x+1)-> mod (x4+x+1) in GF(24)**
In GF(2): (a+b+c)x = ax+bx+c-> (cross terms have coefficient 2 = 0)
```
(xx+x+1)x = x6 + xx + 1
```
Reduce: x4=x+1, x5=xx+x, x6=xx+xx
```
x6 + xx + 1 = (xx+xx) + xx + 1 = xx + (xx+xx) + 1 = xx + 0 + 1 = xx+1
```
> **(xx+x+1)-> mod (x4+x+1) = xx+1**

---

## Q5A Alternates Answered -> Extended Euclidean

**1. Find 7?-> mod 26 using Extended EA**
```
26 = 3 x 7 + 5
7  = 1 x 5 + 2
5  = 2 x 2 + 1
```
Back-sub:
```
1 = 5 - 2 x 2
2 = 7 - 1 x 5
1 = 5 - 2(7-5) = 3 x 5 - 2 x 7
5 = 26 - 3 x 7
1 = 3(26-3 x 7) - 2 x 7 = 3 x 26 - 11 x 7
```
7?-> mod 26 = -11 mod 26 = **15**  
Verify: 7 x 15 = 105 = 4 x 26+1 ?

**2. gcd(35,78) and find 35?-> mod 78**
```
78 = 2 x 35 + 8
35 = 4 x 8 + 3
8  = 2 x 3 + 2
3  = 1 x 2 + 1
```
GCD = 1. Back-sub:
```
1 = 3 - 1 x 2 = 3 - (8-2 x 3) = 3 x 3 - 8
  = 3(35-4 x 8) - 8 = 3 x 35 - 13 x 8
  = 3 x 35 - 13(78-2 x 35) = 29 x 35 - 13 x 78
```
s=29, t=-13. **35?-> mod 78 = 29**  
Verify: 35 x 29 = 1015 = 13 x 78+1 ?

**3. Why must gcd(e, phi(n))=1 in RSA? How is extended EA used to find d?**
RSA requires computing d = e?-> mod phi(n) (the private key). A modular inverse exists if and only if gcd(e, phi(n)) = 1. Extended EA directly computes s such that sxe + txf(n) = 1, so sxe = 1 mod phi(n), giving d = s mod phi(n).

**4. What is Bxzout's Identity?**
For any integers a,b (not both zero): there exist integers s,t such that **gcd(a,b) = sxa + txb**.
The integers s,t are called Bxzout coefficients and are not unique (adding multiples of b/gcd to s and subtracting multiples of a/gcd from t preserves the equation). The Extended Euclidean Algorithm efficiently computes these coefficients.

---

## Q5B Alternates Answered -> Fast Exponentiation

**1. Compute 5^11 mod 13 using square-and-multiply**
11 = 10112 (4 bits)

| Bit | Operation | Result mod 13 |
|---|---|---|
| 1 | init x5 | 5 |
| 0 | 5^(-1)=25=12 | 12 |
| 1 | 12^(-1)=144=1, x5=5 | 5 |
| 1 | 5^(-1)=25=12, x5=60=8 | 8 |

> **5^11 mod 13 = 8**  
Verify: ord(5) mod 13=4. 5^4=1, 5^8=1, 5^11=5^8 x 5^3=1 x 8=**8** ?

**2. How does square-and-multiply relate to RSA decryption efficiency?**
RSA decryption: M = C^d mod n. Private key d is typically ~2048 bits. Naxve multiplication needs d-1 x 2048 multiplications. Square-and-multiply uses only ~1.5xlog2(d) x 3072 operations -> a 600^(-1) speedup. Combined with CRT-RSA (compute mod p and mod q separately, combine), decryption is ~4^(-1) faster still.

**3. What is a timing side-channel attack on fast exponentiation?**
The square-and-multiply algorithm takes **different time** for bit=0 (only square) vs bit=1 (square + multiply). By measuring decryption time across many ciphertexts, an attacker statistically recovers each key bit.

**Defense -> Montgomery Ladder (constant-time):**
```
R0 = 1, R1 = x
For each bit b of e (MSB to LSB):
    if b == 0: R1 = R0xR1; R0 = R0^(-1)
    if b == 1: R0 = R0xR1; R1 = R1^(-1)
```
Always performs both a multiplication and a squaring -> timing is identical for bit 0 and bit 1.

---

## Q6A Alternates Answered -> SSL

**1. What is the difference between SSL 3.0 and TLS 1.3?**

| Feature | SSL 3.0 | TLS 1.3 |
|---|---|---|
| Status | Deprecated (POODLE attack) | Current standard |
| Key Exchange | RSA or DH | ECDHE only (mandatory PFS) |
| Handshake Round Trips | 2 | 1 (or 0-RTT resumption) |
| Cipher Suites | Many weak ones (RC4, DES) | Only strong: AES-GCM, ChaCha20 |
| Authentication | RSA signatures | ECDSA, EdDSA |
| Forward Secrecy | Optional | Mandatory |

**2. What is Perfect Forward Secrecy (PFS)? How does ECDHE provide it?**
PFS means: compromising the server's long-term private key **does not expose past session keys**.

ECDHE achieves this with **ephemeral** key pairs:
- For every session, both parties generate a fresh ECDH key pair
- Session key = ECDH(client_ephemeral_pub, server_ephemeral_priv)
- Ephemeral keys are discarded after the session
- Even if server's signing key is later compromised, attacker cannot reconstruct the ephemeral private key ? past sessions safe

**3. Explain MITM attacks on SSL and how certificates prevent them.**
Without certificates, an attacker could:
1. Intercept ClientHello
2. Present their own public key to client (impersonating server)
3. Present their own public key to server (impersonating client)
4. Decrypt, read, re-encrypt all traffic -> invisible to both parties

**Certificate Chain Prevention:**
- Server presents certificate signed by a trusted CA
- Client verifies CA signature using CA's public key (pre-installed in browser)
- Attacker cannot forge a valid certificate for a domain they don't control (CA policy)
- Certificate includes domain name -> mismatch ? browser alert

---

## Q6B Alternates Answered -> Hybrid Encryption

**1. What is the Key Encapsulation Mechanism (KEM)?**
KEM is a formal abstraction of the "encrypt a symmetric key with a public key" step in hybrid encryption:
- **Encapsulate(pk)** ? (ciphertext C_key, symmetric key K): generates K and its encryption
- **Decapsulate(sk, C_key)** ? K: recovers K using private key
Combined with **DEM (Data Encapsulation Mechanism)** = Enc_K(M), this forms a complete hybrid scheme. KEM+DEM is the modern formal framework for hybrid encryption (replaces ad-hoc RSA+AES constructions).

**2. Why is ECDH preferred over RSA for key exchange in modern systems?**
| | RSA Key Exchange | ECDH Key Exchange |
|---|---|---|
| Forward Secrecy | ? (static keys) | ? (ephemeral ECDHE) |
| Key Size for 128-bit security | 3072-bit RSA | 256-bit ECC |
| Performance | Slower | Much faster |
| TLS 1.3 support | ? Removed | ? Mandatory |

---

## Q7 Alternates Answered -> CSPRNG

**1. What is Blum Blum Shub (BBS)? Does it pass the next-bit test?**
BBS Generator: Choose n = pxq (p,q = 3 mod 4, both prime). Choose seed x0 coprime to n.
```
x??1 = x?-> mod n
Output bit: b? = x? mod 2 (LSB)
```
**Security:** Inverting x??1 = x?-> mod n requires factoring n (integer factorization problem -> assumed hard). Therefore predicting the next bit is as hard as factoring ? **passes the next-bit test** (proven reduction).
BBS is **the** theoretically secure PRNG but very slow (one modular squaring per bit).

**2. /dev/random vs /dev/urandom in Linux**
| | /dev/random | /dev/urandom |
|---|---|---|
| Blocks when? | Entropy pool exhausted | Never blocks |
| Source | Hardware entropy (keyboard, mouse, interrupts) | CSPRNG (ChaCha20) seeded from entropy |
| Security | Theoretically stronger | Practically equivalent for most uses |
| Use case | Key generation (GPG) | General cryptographic use, TLS |
**Recommendation:** Use /dev/urandom (or getrandom() syscall) for almost all purposes. /dev/random's blocking is unnecessary with modern CSPRNGs.

**3. Why was Dual_EC_DRBG considered backdoored?**
Dual_EC_DRBG uses two elliptic curve points P and Q where Q = exP. If the backdoor designer knows e (the discrete log of Q with respect to P), they can predict all future outputs from just 32 bytes of output. The NSA chose the standardized P and Q values -> implying they knew e. Revealed by Snowden documents in 2013. Lesson: Never use standardized constants in CSPRNGs without verifiable proof that no one knows their discrete logs ("nothing-up-my-sleeve numbers").

**4. Define forward security and backward security for PRNGs**
- **Forward Security:** If the internal state is compromised at time t, the adversary **cannot predict outputs after time t** (if the state is updated using a one-way function).
- **Backward Security:** If the internal state is compromised at time t, the adversary **cannot reconstruct outputs before time t** (state transition must be irreversible -> one-way).
A fully secure CSPRNG achieves both: forward security via one-way state updates, backward security via periodic re-seeding from fresh entropy.

---

## Q8/9 Alternates Answered -> Shamir, CRT, EC

**1. What is Shamir scheme security with < t shares?**
With t-1 or fewer shares, the secret is **information-theoretically secure** -> the shares are uniformly distributed over all possible secrets in Z?. An adversary with t-1 shares learns **zero** information about the secret (not just computationally -> even with infinite compute). This follows because for any candidate secret s', there exists a unique degree-(t-1) polynomial passing through the t-1 shares and evaluating to s' at 0.

**2. What is Feldman's Verifiable Secret Sharing (VSS)?**
Feldman's VSS adds **public commitments** to Shamir's scheme so shareholders can verify their share is correct:
- Dealer publishes: C? = g^{a?} mod p for each coefficient a? of f(x)
- Shareholder i verifies their share f(i) satisfies: g^{f(i)} = ? C?^{i?} mod p
- If the check passes ? share is valid; if fails ? dealer cheated
This adds verifiability without revealing the secret (discrete log hardness).

**3. Why does Shamir's scheme require a prime modulus?**
Shamir's scheme uses Lagrange interpolation which requires computing modular inverses (division). Inverses exist for all nonzero elements only in a **field**. Z? is a field only when p is prime. If n is composite, some elements have no inverse (zero divisors exist), making Lagrange interpolation undefined for those values.

**4. What is the Discrete Logarithm Problem (DLP)?**
Given prime p, generator g, and y = g^x mod p -> find x. No efficient classical algorithm exists for large p. Best known: Index Calculus (sub-exponential, but impractical for 2048+ bit p). DLP is the security basis for El-Gamal, Diffie-Hellman, DSA, and EC cryptography.

---

## Q10 Alternates Answered -> IBE vs ABE

**1. What is the key escrow problem in IBE? How can it be mitigated?**
In IBE, the PKG (Private Key Generator) generates ALL private keys. This means:
- PKG can decrypt any message in the system
- If PKG is compromised, all past and future communications are exposed
- PKG must be trusted absolutely

**Mitigations:**
- **Threshold PKG:** Split master secret using Shamir's SSS across multiple PKG servers. Private key generated only when t of n PKG servers cooperate.
- **Distributed IBE:** Multiple independent PKGs, each holding a share; user's private key requires cooperation of all.
- **Certificateless PKE:** Hybrid approach -> user contributes randomness to their own key so even PKG cannot decrypt alone.

**2. Explain KP-ABE vs CP-ABE with examples**

**KP-ABE (Key-Policy):**
- Policy in the KEY, attributes on the CIPHERTEXT
- Example: Alice's key = policy "News AND 2025"; Ciphertext tagged {News, 2025, India} ? Alice can decrypt

**CP-ABE (Ciphertext-Policy):**
- Policy in the CIPHERTEXT, attributes in the KEY
- Example: Encrypt with policy "(Doctor AND Cardiology) OR Admin"; Bob's key has {Doctor, Cardiology} ? Bob can decrypt
- More natural for access control (encryptor defines who can decrypt)

**3. How is Shamir's Secret Sharing used inside ABE?**
In ABE, the secret key is split according to the access policy/attributes using secret sharing:
- The master secret s is split into shares {s?} -> one per attribute
- Each share is bound to a specific attribute using bilinear pairing operations
- A user possessing attributes satisfying the threshold/policy can reconstruct s and decrypt
- This ensures that only users with the correct attribute combination can recover the decryption key

**4. What is Multi-Authority ABE?**
In standard ABE, a single authority manages all attributes -> a single point of failure/trust.
Multi-Authority ABE distributes attribute management across multiple independent authorities:
- Authority 1 manages {Department, Role} attributes
- Authority 2 manages {Clearance, Location} attributes
- No single authority can decrypt on its own
- Users collect attribute keys from multiple authorities
- Useful for cross-organizational scenarios (e.g., healthcare spanning multiple hospitals)
