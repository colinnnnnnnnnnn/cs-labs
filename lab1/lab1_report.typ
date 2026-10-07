#set document(
  title: "Laboratory Work 1: Caesar Cipher",
  author: "Poiata Calin",
)

#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.2cm, left: 2.5cm, right: 2.5cm),
  footer: context {
    let page-num = counter(page).get().first()
    if page-num > 0 {
      align(center)[
        #text(size: 10pt, font: "New Computer Modern")[#str(page-num)]
      ]
    }
  }
)

#set text(
  font: "New Computer Modern",
  size: 10.5pt,
  lang: "en",
)

#set par(
  justify: true,
  leading: 0.62em,
)

// Heading customization
#show heading.where(level: 1): it => block(
  above: 1.4em,
  below: 0.7em,
  text(size: 12.5pt, weight: "bold", it.body)
)

#show heading.where(level: 2): it => block(
  above: 1.1em,
  below: 0.5em,
  text(size: 11pt, weight: "bold", it.body)
)

#show heading.where(level: 3): it => block(
  above: 0.9em,
  below: 0.4em,
  text(size: 10.5pt, weight: "bold", it.body)
)

// Code block styling
#show raw: it => {
  if it.block {
    block(
      width: 100%,
      fill: rgb("#fafafa"),
      inset: (x: 9pt, y: 7pt),
      radius: 3pt,
      stroke: 0.4pt + rgb("#e0e0e0"),
      [
        #set text(font: "JetBrainsMono NF", size: 8pt, fill: rgb("#111827"))
        #set par(leading: 0.4em, justify: false)
        #it
      ]
    )
  } else {
    box(
      fill: rgb("#f3f4f6"),
      inset: (x: 3pt, y: 1pt),
      radius: 2pt,
      baseline: 0pt,
      text(font: "JetBrainsMono NF", size: 8pt, fill: rgb("#111827"))[#it]
    )
  }
}

// -------------------------------------------------------------
// Title Page
// -------------------------------------------------------------
#align(center)[
  #v(2cm)
  #text(size: 14pt, weight: "medium")[
    Ministerul Educației și Cercetării al Republicii Moldova\
    Universitatea Tehnică a Moldovei\
    Facultatea Calculatoare, Informatică și Microelectronică
  ]

  #v(5.5cm)

  #text(size: 15pt, weight: "regular")[Laboratory Work No. 1:]

  #v(0.3cm)

  #text(size: 13pt, weight: "regular")[Caesar Cipher]

  #v(6cm)
]

#grid(
  columns: (1fr, 1fr),
  align: (left, right),
  [
    #text(size: 11pt)[
      Elaborated:\
      Poiata Calin\
      \
      Verified:\
      Maia Zaica\
      \
    ]
  ],
  [
    #text(size: 11pt)[
      gr. FAF-243
    ]
  ]
)

#v(2.5cm)
#align(center)[
  #text(size: 11pt)[Chișinău – 2026]
]

#pagebreak()

// -------------------------------------------------------------
// Table of Contents
// -------------------------------------------------------------
#v(1cm)
#outline(
  title: [Table of Contents],
  indent: auto,
  depth: 2,
)

#pagebreak()

// Reset page counter for main content
#counter(page).update(1)

// =============================================================
// 1. Short Theory
// =============================================================
= Short Theory

== The Caesar Cipher

The Caesar cipher is one of the oldest and simplest known encryption techniques.
Every letter of the plaintext is replaced by the letter found a fixed number of
positions further along the alphabet. The secret numeric key $k$ is the same for
both encryption and decryption, and must satisfy $k in {1, 2, dots, n-1}$, where
$n$ is the size of the alphabet (the value $k = 0$ is excluded because it leaves
the message unchanged).

*Encryption and decryption formulas:*

$
  c = e_k (x) = (x + k) mod n
$
$
  m = d_k (y) = (y - k) mod n
$

where $x$ is the numeric code (position, 0-indexed) of a plaintext letter and $y$
is the numeric code of a ciphertext letter. When $y - k$ is negative, $n$ is added
before applying modulo to keep the result in the range $[0, n-1]$.

For the Romanian alphabet ($n = 31$, Table~1) and key $k = 5$, letter *E* (code 6)
encrypts to *J* (code 11): $(6 + 5) mod 31 = 11$.

*Key space:* there are $n - 1 = 30$ possible keys, which makes the cipher trivially
breakable by exhaustive search (trying all keys in turn).

== The Caesar Cipher with a Keyword Permutation

To increase the key space, the alphabet is first permuted using a second key — a
keyword. The keyword letters (unique, in order of first appearance) are written
first, followed by the remaining alphabet letters in their natural order. All 31
letters appear exactly once in the permuted alphabet.

The numeric code of each letter is then its *position in the permuted alphabet*,
and the same shift formula is applied:

$
  c = e_(k_1, k_2)(x) = (x' + k_1) mod n,
  quad
  m = d_(k_1, k_2)(y) = (y' - k_1) mod n
$

where $x'$ and $y'$ are positions in the permuted alphabet.

*Key space:* there are $31! times 30$ possible key pairs $(k_1, k_2)$, an
astronomically larger space. However, the cipher remains vulnerable to
*frequency analysis*, because every plaintext letter is always mapped to the same
ciphertext letter.

#pagebreak()

// =============================================================
// 2. Implementation
// =============================================================
= Implementation

== Alphabet Encoding (Table 2)

The Romanian alphabet ($n = 31$) is stored as a Python list, giving each letter
an index from 0 to 30 without relying on ASCII or Unicode code points:

```python
ROMANIAN_ALPHABET: List[str] = [
    'A', 'Ă', 'Â', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'Î', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    'R', 'S', 'Ș', 'T', 'Ț', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
ALPHABET_SIZE: int = len(ROMANIAN_ALPHABET)   # 31

CHAR_TO_INDEX: Dict[str, int] = {ch: i for i, ch in enumerate(ROMANIAN_ALPHABET)}
INDEX_TO_CHAR: Dict[int, str] = {i: ch for i, ch in enumerate(ROMANIAN_ALPHABET)}
```

Two dictionaries (`CHAR_TO_INDEX` and `INDEX_TO_CHAR`) provide O(1) lookup in
both directions. The shift arithmetic operates on dictionary indices — never on
Unicode code points.

== Input Normalization

Romanian text may arrive with *cedilla* variants (Ş, Ţ) instead of
*comma-below* variants (Ș, Ț), depending on the keyboard layout.
A translation table converts them before any further processing:

```python
CEDILLA_TRANS = str.maketrans({'Ş': 'Ș', 'ş': 'ș', 'Ţ': 'Ț', 'ţ': 'ț'})

def normalize_input_text(raw: str) -> str:
    return unicodedata.normalize('NFC', raw).translate(CEDILLA_TRANS).upper()
```

`unicodedata.normalize('NFC', ...)` ensures that decomposed Unicode sequences
(e.g. `s` + combining cedilla) are first composed into a single code point before
the substitution map is applied.

== Input Validation

=== Key Validation

```python
def validate_key(key_str: str) -> Tuple[bool, int, str]:
    try:
        val = int(key_str.strip())
    except ValueError:
        return False, 0, f"Invalid key '{key_str}'. Must be an integer between 1 and 30."
    if not (1 <= val <= 30):
        return False, 0, f"Key {val} out of range. Must be between 1 and 30 inclusive."
    return True, val, ""
```

The function returns a `(is_valid, value, error_message)` triple. The caller
displays the error message and re-prompts until a valid value is entered.

=== Text Validation

```python
def validate_and_clean_text(raw: str) -> Tuple[bool, str, List[str], str]:
    normalized = normalize_input_text(raw)
    cleaned, rejected = [], []
    for orig, norm in zip(raw, normalized):
        if orig.isspace():
            continue          # spaces are allowed and stripped
        if norm in CHAR_TO_INDEX:
            cleaned.append(norm)
        elif orig not in rejected:
            rejected.append(orig)
    if rejected:
        return False, "", rejected, f"Invalid character(s): {rejected}"
    return True, "".join(cleaned), [], ""
```

Each character is checked against `CHAR_TO_INDEX`. Any character not in the
Romanian alphabet (after normalization) is collected and reported to the user.

=== Keyword Validation

```python
def validate_keyword(raw: str) -> Tuple[bool, str, List[str], str]:
    normalized = normalize_input_text(raw.strip())
    cleaned, rejected = [], []
    for orig, norm in zip(raw.strip(), normalized):
        if norm in CHAR_TO_INDEX:
            cleaned.append(norm)
        elif orig not in rejected:
            rejected.append(orig)
    if rejected:
        return False, "", rejected, f"Invalid character(s) in keyword: {rejected}"
    kw = "".join(cleaned)
    if len(kw) < 7:
        return False, "", [], f"Keyword '{kw}' too short ({len(kw)}). Minimum length is 7."
    return True, kw, [], ""
```

Spaces in the keyword are treated as invalid characters (unlike plaintext).
After removing bad characters the remaining length is checked against the minimum.

== Encryption and Decryption (Task 1.1)

```python
def caesar_encrypt(plaintext: str, key: int) -> str:
    return "".join(
        INDEX_TO_CHAR[(CHAR_TO_INDEX[ch] + key) % ALPHABET_SIZE]
        for ch in plaintext
    )

def caesar_decrypt(ciphertext: str, key: int) -> str:
    return "".join(
        INDEX_TO_CHAR[(CHAR_TO_INDEX[ch] - key + ALPHABET_SIZE) % ALPHABET_SIZE]
        for ch in ciphertext
    )
```

Adding `ALPHABET_SIZE` before the modulo in decryption avoids negative remainders,
which some languages (Python included) can produce for negative operands of `%`.

== Permuted Alphabet and Two-Key Cipher (Task 1.2)

```python
def generate_permuted_alphabet(keyword: str) -> List[str]:
    seen, permuted = set(), []
    for ch in keyword:              # distinct keyword letters first
        if ch not in seen:
            seen.add(ch); permuted.append(ch)
    for ch in ROMANIAN_ALPHABET:   # remaining letters in natural order
        if ch not in seen:
            seen.add(ch); permuted.append(ch)
    return permuted                 # always exactly 31 entries

def caesar_permuted_encrypt(plaintext, key, keyword):
    perm = generate_permuted_alphabet(keyword)
    c2i  = {ch: i for i, ch in enumerate(perm)}
    i2c  = {i: ch for i, ch in enumerate(perm)}
    return "".join(i2c[(c2i[ch] + key) % ALPHABET_SIZE] for ch in plaintext), perm

def caesar_permuted_decrypt(ciphertext, key, keyword):
    perm = generate_permuted_alphabet(keyword)
    c2i  = {ch: i for i, ch in enumerate(perm)}
    i2c  = {i: ch for i, ch in enumerate(perm)}
    return "".join(i2c[(c2i[ch] - key + ALPHABET_SIZE) % ALPHABET_SIZE] for ch in ciphertext), perm
```

The permuted alphabet is rebuilt on every call from the same keyword, so
encryption and decryption are perfectly symmetric.

#pagebreak()

// =============================================================
// 3. Results
// =============================================================
= Results

== Task 1.1: Standard Caesar Cipher

=== Encryption and Decryption

The screenshot below shows a full encryption and decryption cycle with key $k = 7$.
Input text containing Romanian diacritics is normalised, uppercased and stripped of
spaces before the cipher is applied; decryption recovers the exact processed plaintext.

#figure(
  image("screenshots/task1_1_enc_dec.png", width: 100%),
  caption: [Task 1.1 — encryption with $k = 7$ and subsequent decryption],
)

=== Invalid Key Input

The program re-prompts for a key when the value is out of range (0 or 31) or
non-numeric, displaying a clear message that states the allowed range $[1, 30]$.

#figure(
  image("screenshots/task1_1_invalid_key.png", width: 100%),
  caption: [Task 1.1 — invalid key handling (out-of-range and non-numeric values)],
)

=== Invalid Characters and Cedilla Normalization

Digits, punctuation and other non-Romanian characters are rejected with a message
listing the offending symbols. The cedilla variants Ş/ş and Ţ/ţ are silently
normalised to the correct comma-below forms Ș/ș and Ț/ț.

#figure(
  image("screenshots/task1_1_invalid_char.png", width: 100%),
  caption: [Task 1.1 — invalid character rejection and automatic cedilla normalization],
)

#pagebreak()

== Task 1.2: Caesar Cipher with Permutation

=== Permuted Alphabet, Encryption and Decryption

With keyword *CRIPTOGRAFIE* and shift $k_1 = 12$ the program first displays the
31-letter permuted alphabet (for manual verification), then encrypts the plaintext
and subsequently decrypts the ciphertext back to the original.

#figure(
  image("screenshots/task1_2_enc_dec.png", width: 100%),
  caption: [Task 1.2 — permuted alphabet display, encryption and decryption with $k_1 = 12$, keyword CRIPTOGRAFIE],
)

=== Invalid Keyword Input

The program rejects keywords that are too short (fewer than 7 letters), contain
spaces, digits or punctuation, and continues prompting until a valid keyword is
given.

#figure(
  image("screenshots/task1_2_invalid_keys.png", width: 100%),
  caption: [Task 1.2 — keyword validation: too short, digits, and punctuation errors],
)

#pagebreak()

// =============================================================
// 4. Conclusions
// =============================================================
= Conclusions

*Security of the standard Caesar cipher.* With only $n - 1 = 30$ possible keys for
the Romanian alphabet, an attacker can recover the plaintext in at most 30 trials
— a trivially fast exhaustive search. The cipher provides no meaningful security
and should never be used to protect real information.

*Security of the permuted Caesar cipher.* Adding a keyword-based permutation
inflates the key space to $31! times 30 approx 10^{33}$ possible key pairs,
making brute-force enumeration completely infeasible. Despite this, the cipher
remains vulnerable to *frequency analysis*: because each plaintext letter is
always replaced by the same ciphertext letter, the statistical structure of the
Romanian language (letter frequencies, common digraphs, etc.) is preserved in the
ciphertext and can be exploited to recover the plaintext without knowing the key.

*What was learned.*
- How to map an arbitrary alphabet to integer codes and apply modular arithmetic
  for encryption and decryption, without relying on built-in character encodings.
- How a keyword permutation is constructed and how it extends the classical Caesar
  cipher.
- The practical limitations of both ciphers: small key space (Caesar) and
  susceptibility to frequency analysis (both variants), which are the fundamental
  reasons why modern symmetric ciphers use much more complex transformations.
- Implementation considerations for real-world Romanian text: Unicode normalization,
  NFC composition, and handling of the two keyboard variants for Ș/Ț.

// =============================================================
// 5. Source Code
// =============================================================
= Source Code

The full source code for this laboratory work is available on GitHub:\

#link("https://github.com/colinnnnnnnnnnn/cs-labs")[https://github.com/colinnnnnnnnnnn/cs-labs]

The repository contains:
- `caesar_cipher.py` — core implementation and interactive CLI (Tasks 1.1 and 1.2)
- `test_caesar.py` — unit test suite (8 tests, all passing)
- `demo.py` — non-interactive demonstration script
- `generate_screenshots.py` — script used to render the terminal screenshots in this report
