"""
Demonstration script showing:
1. Task 1.1: Standard Caesar Cipher encryption, decryption, and error handling.
2. Task 1.2: Permuted Caesar Cipher alphabet display, encryption, decryption, and error handling.
This provides sample test runs and demonstration outputs suitable for laboratory reports and screenshots.
"""

from caesar_cipher import (
    ROMANIAN_ALPHABET,
    format_alphabet_table,
    validate_key,
    validate_and_clean_text,
    validate_keyword,
    caesar_encrypt,
    caesar_decrypt,
    caesar_permuted_encrypt,
    caesar_permuted_decrypt
)


def print_section(title: str):
    print("\n" + "=" * 70)
    print(f" {title.upper()}")
    print("=" * 70)


def demo_task_1_1():
    print_section("DEMONSTRATION: TASK 1.1 (Standard Caesar Cipher, n=31)")

    # 1. Successful Encryption and Decryption
    sample_text = "Cifrul Cezar pentru limba română cu diacritice ă â î ș ț"
    key = 7

    print("\n[SCENARIO 1: Encryption & Decryption]")
    print(f"Input text (raw)     : {sample_text}")
    is_valid, cleaned, _, _ = validate_and_clean_text(sample_text)
    print(f"Cleaned/Processed    : {cleaned}")
    print(f"Shift key (k)        : {key}")

    ciphertext = caesar_encrypt(cleaned, key)
    print(f"Ciphertext (c)       : {ciphertext}")

    decrypted = caesar_decrypt(ciphertext, key)
    print(f"Decrypted text (m)   : {decrypted}")
    print(f"Match verified       : {cleaned == decrypted}")

    # 2. Error handling: invalid keys
    print("\n[SCENARIO 2: Invalid Key Validation]")
    for invalid_k in ["0", "31", "-5", "abc"]:
        valid, _, err = validate_key(invalid_k)
        print(f"Input key: '{invalid_k}' -> Valid? {valid} | Error: {err}")

    # 3. Error handling: invalid characters in text
    print("\n[SCENARIO 3: Invalid Characters in Text]")
    invalid_text = "Salutare! Anul 2026 aduce securitate 100%."
    valid, _, rej, err = validate_and_clean_text(invalid_text)
    print(f"Input text: '{invalid_text}'")
    print(f"Valid? {valid}")
    print(f"Rejected characters: {rej}")
    print(f"Error message displayed to user:\n{err}")


def demo_task_1_2():
    print_section("DEMONSTRATION: TASK 1.2 (Caesar Cipher with Permutation, n=31)")

    # 1. Alphabet permutation and display
    keyword = "CRIPTOGRAFIE"
    key1 = 12
    sample_text = "Securitatea Informației și Tehnologia Calculatoarelor"

    print("\n[SCENARIO 1: Permuted Alphabet Generation]")
    print(f"Keyword (Key 2)      : {keyword}")
    print(f"Shift Key (Key 1)    : {key1}")

    is_valid_kw, clean_kw, _, _ = validate_keyword(keyword)
    is_valid_txt, clean_txt, _, _ = validate_and_clean_text(sample_text)

    ciphertext, permuted_alphabet = caesar_permuted_encrypt(clean_txt, key1, clean_kw)

    print("\n" + format_alphabet_table(permuted_alphabet, f"Permuted Alphabet (Keyword: {clean_kw})"))

    print("\n[SCENARIO 2: Permuted Encryption & Decryption]")
    print(f"Input text (raw)     : {sample_text}")
    print(f"Cleaned/Processed    : {clean_txt}")
    print(f"Ciphertext (c)       : {ciphertext}")

    decrypted, _ = caesar_permuted_decrypt(ciphertext, key1, clean_kw)
    print(f"Decrypted text (m)   : {decrypted}")
    print(f"Match verified       : {clean_txt == decrypted}")

    # 2. Error handling: Keyword validation
    print("\n[SCENARIO 3: Keyword Validation (Too Short & Invalid Characters)]")
    invalid_keywords = [
        "CEZAR",         # too short (5 < 7)
        "CRIPTO 123",    # spaces and digits
        "ALGORITM!",     # punctuation
    ]
    for kw in invalid_keywords:
        valid, _, rej, err = validate_keyword(kw)
        print(f"\nKeyword input: '{kw}'")
        print(f"Valid? {valid}")
        print(f"Error: {err}")


def main():
    print_section("Romanian Alphabet (Table 2 Encoding)")
    print(format_alphabet_table(ROMANIAN_ALPHABET, "Table 2: Standard Romanian Alphabet"))

    demo_task_1_1()
    demo_task_1_2()
    print("\n" + "=" * 70)
    print(" ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
