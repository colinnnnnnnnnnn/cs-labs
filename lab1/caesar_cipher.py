"""
Laboratory Work No. 1: Caesar Cipher Implementation
Supports Task 1.1 (Standard Caesar Cipher over Romanian alphabet)
and Task 1.2 (Caesar Cipher with Keyword Permutation over Romanian alphabet).
"""

import sys
import unicodedata
from typing import List, Tuple, Set, Dict


# ---------------------------------------------------------------------------
# Romanian Alphabet Specification (Table 2 from Laboratory Guide)
# n = 31 letters
# ---------------------------------------------------------------------------
ROMANIAN_ALPHABET: List[str] = [
    'A', 'Ă', 'Â', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    'I', 'Î', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
    'R', 'S', 'Ș', 'T', 'Ț', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

ALPHABET_SIZE: int = len(ROMANIAN_ALPHABET)  # 31

# Encoding dictionaries (A = 0, Ă = 1, ..., Z = 30)
# Custom letter-to-index mapping (never relying on ASCII/Unicode code points for shifts)
CHAR_TO_INDEX: Dict[str, int] = {char: idx for idx, char in enumerate(ROMANIAN_ALPHABET)}
INDEX_TO_CHAR: Dict[int, str] = {idx: char for idx, char in enumerate(ROMANIAN_ALPHABET)}

# Cedilla to Comma-below mapping for Romanian keyboard compatibility:
# Ş (U+015E) -> Ș (U+0218), ş (U+015F) -> ș (U+0219)
# Ţ (U+0162) -> Ț (U+021A), ţ (U+0163) -> ț (U+021B)
CEDILLA_TRANS = str.maketrans({
    'Ş': 'Ș',
    'ş': 'ș',
    'Ţ': 'Ț',
    'ţ': 'ț'
})


def normalize_input_text(raw_text: str) -> str:
    """
    Normalizes input text:
    - Normalizes Unicode composition (NFC)
    - Replaces cedilla variants (Ş, Ţ) with standard comma-below letters (Ș, Ț)
    - Converts to uppercase
    """
    normalized = unicodedata.normalize('NFC', raw_text)
    substituted = normalized.translate(CEDILLA_TRANS)
    return substituted.upper()


def validate_and_clean_text(raw_text: str) -> Tuple[bool, str, List[str], str]:
    """
    Validates and cleans input text (plaintext or ciphertext).
    Rules:
    - Spaces are allowed and removed.
    - Only Romanian alphabet letters (A-Z, Ă, Â, Î, Ș, Ț, case-insensitive) are allowed.
    - Built-in character encodings are not used for validation; membership in ROMANIAN_ALPHABET is checked.

    Returns:
        (is_valid, cleaned_text, rejected_chars, error_message)
    """
    if not raw_text or not raw_text.strip():
        return False, "", [], "Text cannot be empty. Please enter at least one Romanian letter."

    normalized = normalize_input_text(raw_text)
    
    cleaned_chars: List[str] = []
    rejected_chars: List[str] = []

    for orig_char, norm_char in zip(raw_text, normalized):
        if orig_char.isspace():
            continue  # Spaces are allowed and stripped
        if norm_char in CHAR_TO_INDEX:
            cleaned_chars.append(norm_char)
        else:
            if orig_char not in rejected_chars:
                rejected_chars.append(orig_char)

    if rejected_chars:
        rejected_repr = ", ".join(f"'{c}'" for c in rejected_chars)
        err = (
            f"Invalid character(s) rejected: {rejected_repr}.\n"
            f"Allowed characters: Romanian alphabet letters (A-Z, Ă, Â, Î, Ș, Ț, case-insensitive) and spaces."
        )
        return False, "", rejected_chars, err

    cleaned_text = "".join(cleaned_chars)
    if not cleaned_text:
        return False, "", [], "Text cannot contain only spaces. Please enter at least one Romanian letter."

    return True, cleaned_text, [], ""


def validate_key(key_str: str) -> Tuple[bool, int, str]:
    """
    Validates the numeric shift key.
    Rules:
    - Must be an integer between 1 and 30 inclusive (1 <= k <= 30).

    Returns:
        (is_valid, key_value, error_message)
    """
    key_str = key_str.strip()
    try:
        key_val = int(key_str)
    except ValueError:
        return (
            False,
            0,
            f"Invalid key '{key_str}'. The shift key must be an integer between 1 and 30 inclusive."
        )

    if not (1 <= key_val <= 30):
        return (
            False,
            0,
            f"Key value {key_val} is out of range. The shift key must be an integer between 1 and 30 inclusive."
        )

    return True, key_val, ""


def validate_keyword(raw_keyword: str) -> Tuple[bool, str, List[str], str]:
    """
    Validates Key 2 (keyword for Task 1.2).
    Rules:
    - Must contain only letters of the Romanian alphabet.
    - Minimum length of 7 characters.
    - Converted to uppercase before use.

    Returns:
        (is_valid, cleaned_keyword, rejected_chars, error_message)
    """
    if not raw_keyword or not raw_keyword.strip():
        return False, "", [], "Keyword cannot be empty. It must be at least 7 letters long."

    normalized = normalize_input_text(raw_keyword.strip())
    rejected_chars: List[str] = []
    cleaned_chars: List[str] = []

    for orig_char, norm_char in zip(raw_keyword.strip(), normalized):
        if norm_char in CHAR_TO_INDEX:
            cleaned_chars.append(norm_char)
        else:
            if orig_char not in rejected_chars:
                rejected_chars.append(orig_char)

    if rejected_chars:
        rejected_repr = ", ".join(f"'{c}'" for c in rejected_chars)
        err = (
            f"Invalid character(s) in keyword rejected: {rejected_repr}.\n"
            f"The keyword must contain only Romanian alphabet letters (A-Z, Ă, Â, Î, Ș, Ț)."
        )
        return False, "", rejected_chars, err

    keyword_cleaned = "".join(cleaned_chars)
    if len(keyword_cleaned) < 7:
        err = (
            f"Keyword '{keyword_cleaned}' is too short (length {len(keyword_cleaned)}). "
            f"The keyword must have a minimum length of 7 characters."
        )
        return False, "", [], err

    return True, keyword_cleaned, [], ""


# ---------------------------------------------------------------------------
# Task 1.1: Standard Caesar Cipher over Romanian Alphabet
# ---------------------------------------------------------------------------
def caesar_encrypt(plaintext: str, key: int) -> str:
    """
    Encrypts plaintext using the standard Caesar cipher:
    c = (x + k) mod 31
    """
    ciphertext_chars: List[str] = []
    for char in plaintext:
        x = CHAR_TO_INDEX[char]
        c = (x + key) % ALPHABET_SIZE
        ciphertext_chars.append(INDEX_TO_CHAR[c])
    return "".join(ciphertext_chars)


def caesar_decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypts ciphertext using the standard Caesar cipher:
    m = (y - k) mod 31
    (Explicitly adding ALPHABET_SIZE to ensure non-negative operand before modulo)
    """
    plaintext_chars: List[str] = []
    for char in ciphertext:
        y = CHAR_TO_INDEX[char]
        m = (y - key + ALPHABET_SIZE) % ALPHABET_SIZE
        plaintext_chars.append(INDEX_TO_CHAR[m])
    return "".join(plaintext_chars)


# ---------------------------------------------------------------------------
# Task 1.2: Caesar Cipher with Keyword Permutation over Romanian Alphabet
# ---------------------------------------------------------------------------
def generate_permuted_alphabet(keyword: str) -> List[str]:
    """
    Constructs the permuted alphabet from Key 2 (keyword):
    1. First, distinct letters of the keyword in order of their first appearance.
    2. Followed by the remaining letters of the Romanian alphabet in their natural order.
    The resulting alphabet contains all 31 Romanian letters.
    """
    permuted: List[str] = []
    seen: Set[str] = set()

    # Step 1: Distinct letters of keyword
    for char in keyword:
        if char not in seen:
            seen.add(char)
            permuted.append(char)

    # Step 2: Remaining letters of the Romanian alphabet in natural order
    for char in ROMANIAN_ALPHABET:
        if char not in seen:
            seen.add(char)
            permuted.append(char)

    return permuted


def caesar_permuted_encrypt(plaintext: str, key: int, keyword: str) -> Tuple[str, List[str]]:
    """
    Encrypts plaintext using Caesar cipher with keyword permutation:
    Letter positions are determined by the permuted alphabet.
    c = (x + k) mod 31 in permuted alphabet.

    Returns:
        (ciphertext, permuted_alphabet)
    """
    permuted_alphabet = generate_permuted_alphabet(keyword)
    perm_char_to_index = {ch: idx for idx, ch in enumerate(permuted_alphabet)}
    perm_index_to_char = {idx: ch for idx, ch in enumerate(permuted_alphabet)}

    ciphertext_chars: List[str] = []
    for char in plaintext:
        x = perm_char_to_index[char]
        c = (x + key) % ALPHABET_SIZE
        ciphertext_chars.append(perm_index_to_char[c])

    return "".join(ciphertext_chars), permuted_alphabet


def caesar_permuted_decrypt(ciphertext: str, key: int, keyword: str) -> Tuple[str, List[str]]:
    """
    Decrypts ciphertext using Caesar cipher with keyword permutation:
    m = (y - k) mod 31 in permuted alphabet.

    Returns:
        (plaintext, permuted_alphabet)
    """
    permuted_alphabet = generate_permuted_alphabet(keyword)
    perm_char_to_index = {ch: idx for idx, ch in enumerate(permuted_alphabet)}
    perm_index_to_char = {idx: ch for idx, ch in enumerate(permuted_alphabet)}

    plaintext_chars: List[str] = []
    for char in ciphertext:
        y = perm_char_to_index[char]
        m = (y - key + ALPHABET_SIZE) % ALPHABET_SIZE
        plaintext_chars.append(perm_index_to_char[m])

    return "".join(plaintext_chars), permuted_alphabet


# ---------------------------------------------------------------------------
# Visual Formatting Helpers
# ---------------------------------------------------------------------------
def format_alphabet_table(alphabet: List[str], title: str = "Alphabet Encoding") -> str:
    """
    Formats an alphabet and its 0-30 indices in a neat table.
    """
    lines = [f"=== {title} (n = {len(alphabet)}) ==="]
    
    # Split into two rows for pleasant terminal display (0..15 and 16..30)
    row1_chars = alphabet[:16]
    row1_idxs = list(range(16))
    row2_chars = alphabet[16:]
    row2_idxs = list(range(16, len(alphabet)))

    header1 = "Index:  " + " ".join(f"{i:2d}" for i in row1_idxs)
    chars1  = "Letter: " + " ".join(f"{c:2s}" for c in row1_chars)
    header2 = "Index:  " + " ".join(f"{i:2d}" for i in row2_idxs)
    chars2  = "Letter: " + " ".join(f"{c:2s}" for c in row2_chars)

    lines.extend([header1, chars1, "-" * len(header1), header2, chars2])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Interactive Prompts with Continuous Validation
# ---------------------------------------------------------------------------
def prompt_shift_key(prompt_text: str = "Enter shift key (integer 1-30): ") -> int:
    """Prompts repeatedly until a valid integer in [1, 30] is entered."""
    while True:
        try:
            user_input = input(prompt_text)
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, key_val, err_msg = validate_key(user_input)
        if is_valid:
            return key_val
        print(f"[ERROR] {err_msg}")


def prompt_keyword(prompt_text: str = "Enter keyword Key 2 (letters only, min length 7): ") -> str:
    """Prompts repeatedly until a valid keyword is entered."""
    while True:
        try:
            user_input = input(prompt_text)
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, cleaned_kw, _, err_msg = validate_keyword(user_input)
        if is_valid:
            return cleaned_kw
        print(f"[ERROR] {err_msg}")


def prompt_text(prompt_text: str = "Enter message: ") -> str:
    """Prompts repeatedly until valid Romanian text is entered."""
    while True:
        try:
            user_input = input(prompt_text)
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(0)

        is_valid, cleaned_txt, _, err_msg = validate_and_clean_text(user_input)
        if is_valid:
            return cleaned_txt
        print(f"[ERROR] {err_msg}")


# ---------------------------------------------------------------------------
# Interactive Menu and Main Loop
# ---------------------------------------------------------------------------
def run_task_1_1_cli():
    print("\n" + "=" * 60)
    print(" TASK 1.1: Standard Caesar Cipher (Romanian Alphabet, n=31)")
    print("=" * 60)
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Return to Main Menu")

    choice = input("Select operation (1-3): ").strip()
    if choice == '1':
        print("\n--- Encryption ---")
        key = prompt_shift_key("Enter shift key k (1-30): ")
        plaintext = prompt_text("Enter plaintext message: ")
        ciphertext = caesar_encrypt(plaintext, key)
        print("\n[RESULT]")
        print(f"  Input Plaintext (processed) : {plaintext}")
        print(f"  Shift Key k                : {key}")
        print(f"  Result Ciphertext          : {ciphertext}")
    elif choice == '2':
        print("\n--- Decryption ---")
        key = prompt_shift_key("Enter shift key k (1-30): ")
        ciphertext = prompt_text("Enter ciphertext: ")
        plaintext = caesar_decrypt(ciphertext, key)
        print("\n[RESULT]")
        print(f"  Input Ciphertext (processed): {ciphertext}")
        print(f"  Shift Key k                : {key}")
        print(f"  Result Plaintext           : {plaintext}")
    elif choice == '3':
        return
    else:
        print("[ERROR] Invalid selection. Returning to menu.")


def run_task_1_2_cli():
    print("\n" + "=" * 60)
    print(" TASK 1.2: Caesar Cipher with Permutation (Two Keys, n=31)")
    print("=" * 60)
    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Return to Main Menu")

    choice = input("Select operation (1-3): ").strip()
    if choice == '1':
        print("\n--- Encryption with Permutation ---")
        key1 = prompt_shift_key("Enter Key 1 (shift k, 1-30): ")
        key2 = prompt_keyword("Enter Key 2 (keyword, >=7 Romanian letters): ")
        plaintext = prompt_text("Enter plaintext message: ")

        ciphertext, permuted = caesar_permuted_encrypt(plaintext, key1, key2)
        print("\n" + format_alphabet_table(permuted, f"Permuted Alphabet (Keyword: '{key2}')"))
        print("\n[RESULT]")
        print(f"  Input Plaintext (processed) : {plaintext}")
        print(f"  Key 1 (Shift k)            : {key1}")
        print(f"  Key 2 (Keyword)            : {key2}")
        print(f"  Result Ciphertext          : {ciphertext}")
    elif choice == '2':
        print("\n--- Decryption with Permutation ---")
        key1 = prompt_shift_key("Enter Key 1 (shift k, 1-30): ")
        key2 = prompt_keyword("Enter Key 2 (keyword, >=7 Romanian letters): ")
        ciphertext = prompt_text("Enter ciphertext: ")

        plaintext, permuted = caesar_permuted_decrypt(ciphertext, key1, key2)
        print("\n" + format_alphabet_table(permuted, f"Permuted Alphabet (Keyword: '{key2}')"))
        print("\n[RESULT]")
        print(f"  Input Ciphertext (processed): {ciphertext}")
        print(f"  Key 1 (Shift k)            : {key1}")
        print(f"  Key 2 (Keyword)            : {key2}")
        print(f"  Result Plaintext           : {plaintext}")
    elif choice == '3':
        return
    else:
        print("[ERROR] Invalid selection. Returning to menu.")


def main():
    while True:
        print("\n" + "=" * 60)
        print("  CAESAR CIPHER - ROMANIAN ALPHABET (Laboratory Work No. 1)")
        print("=" * 60)
        print("1. Task 1.1: Standard Caesar Cipher (1 Key)")
        print("2. Task 1.2: Caesar Cipher with Permutation (2 Keys)")
        print("3. Display Standard Romanian Alphabet (Table 2)")
        print("4. Exit")

        choice = input("Enter option (1-4): ").strip()
        if choice == '1':
            run_task_1_1_cli()
        elif choice == '2':
            run_task_1_2_cli()
        elif choice == '3':
            print("\n" + format_alphabet_table(ROMANIAN_ALPHABET, "Standard Romanian Alphabet (Table 2)"))
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please select an option between 1 and 4.")


if __name__ == "__main__":
    main()
