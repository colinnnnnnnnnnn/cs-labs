#!/usr/bin/env python3
import sys

# Romanian alphabet with 31 letters in standard alphabetical order
ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
N = len(ALPHABET)
CHAR_TO_IDX = {ch: i for i, ch in enumerate(ALPHABET)}
IDX_TO_CHAR = {i: ch for i, ch in enumerate(ALPHABET)}

# Maps legacy Romanian cedilla characters to standard comma-below variants
CEDILLA_MAP = str.maketrans({"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"})


def clean_text(text: str) -> str:
    text = text.translate(CEDILLA_MAP)
    # Remove all whitespace before converting to uppercase
    text = "".join(text.split())
    return text.upper()


def find_invalid_chars(text: str) -> list[str]:
    # Returns characters that do not belong to the 31-letter Romanian alphabet
    return sorted(list({ch for ch in text if ch not in CHAR_TO_IDX}))


def validate_key(raw_key: str) -> tuple[str | None, str | None]:
    cleaned = clean_text(raw_key)
    if len(cleaned) < 7:
        return None, f"Eroare: Lungimea cheii trebuie să fie de cel puțin 7 caractere (lungime actuală: {len(cleaned)})."
    invalid = find_invalid_chars(cleaned)
    if invalid:
        inv_str = ", ".join(f"'{c}'" for c in invalid)
        hint = (
            f"Eroare: Cheia conține caractere nepermise: {inv_str}.\n"
            f"Diapazonul permis: literele alfabetului român (A-Z, Ă, Â, Î, Ș, Ț). "
            f"Cifrele și semnele de punctuație nu sunt permise."
        )
        return None, hint
    return cleaned, None


def validate_message(raw_msg: str) -> tuple[str | None, str | None]:
    cleaned = clean_text(raw_msg)
    if not cleaned:
        return None, "Eroare: Mesajul introdus este gol."
    invalid = find_invalid_chars(cleaned)
    if invalid:
        inv_str = ", ".join(f"'{c}'" for c in invalid)
        hint = (
            f"Eroare: Textul conține caractere nepermise: {inv_str}.\n"
            f"Diapazonul permis: literele alfabetului român (A-Z, Ă, Â, Î, Ș, Ț). "
            f"Cifrele și semnele de punctuație nu sunt permise."
        )
        return None, hint
    return cleaned, None


def encrypt(plaintext: str, key: str) -> str:
    res = []
    key_len = len(key)
    for i, ch in enumerate(plaintext):
        k_ch = key[i % key_len]
        # Mathematical model: c_i = (m_i + k_i) mod 31
        c_idx = (CHAR_TO_IDX[ch] + CHAR_TO_IDX[k_ch]) % N
        res.append(IDX_TO_CHAR[c_idx])
    return "".join(res)


def decrypt(ciphertext: str, key: str) -> str:
    res = []
    key_len = len(key)
    for i, ch in enumerate(ciphertext):
        k_ch = key[i % key_len]
        # Mathematical model: m_i = (c_i - k_i) mod 31
        m_idx = (CHAR_TO_IDX[ch] - CHAR_TO_IDX[k_ch]) % N
        res.append(IDX_TO_CHAR[m_idx])
    return "".join(res)


def display_calculation_table(text: str, key: str, is_encrypt: bool = True) -> None:
    op_symbol = "+" if is_encrypt else "-"
    key_len = len(key)
    
    repeated_key = "".join(key[i % key_len] for i in range(len(text)))
    text_nums = [CHAR_TO_IDX[c] for c in text]
    key_nums = [CHAR_TO_IDX[c] for c in repeated_key]
    
    if is_encrypt:
        res_nums = [(t + k) % N for t, k in zip(text_nums, key_nums)]
    else:
        res_nums = [(t - k) % N for t, k in zip(text_nums, key_nums)]
    res_chars = [IDX_TO_CHAR[n] for n in res_nums]
    
    col_width = 4
    header1 = "Text (M):" if is_encrypt else "Criptogramă (C):"
    header2 = "Cheie (K):"
    header3 = f"M {op_symbol} K (mod 31):" if is_encrypt else f"C {op_symbol} K (mod 31):"
    header4 = "Rezultat:"
    
    # Chunk display for long texts
    chunk_size = 20
    for start in range(0, len(text), chunk_size):
        end = min(start + chunk_size, len(text))
        print("\n" + "-" * 75)
        print(f"{header1:<22} " + " ".join(f"{text[i]:>{col_width}}" for i in range(start, end)))
        print(f"{header2:<22} " + " ".join(f"{repeated_key[i]:>{col_width}}" for i in range(start, end)))
        print(f"{'Valori text:':<22} " + " ".join(f"{text_nums[i]:>{col_width}}" for i in range(start, end)))
        print(f"{'Valori cheie:':<22} " + " ".join(f"{key_nums[i]:>{col_width}}" for i in range(start, end)))
        print(f"{header3:<22} " + " ".join(f"{res_nums[i]:>{col_width}}" for i in range(start, end)))
        print(f"{header4:<22} " + " ".join(f"{res_chars[i]:>{col_width}}" for i in range(start, end)))
    print("-" * 75)


def show_alphabet() -> None:
    print("\n" + "=" * 65)
    print("ALFABETUL LIMBII ROMÂNE (31 DE LITERE) ȘI CODIFICAREA LOR")
    print("=" * 65)
    row1 = " ".join(f"{ch:>3}" for ch in ALPHABET)
    row2 = " ".join(f"{i:>3}" for i in range(N))
    print(f"Litera: {row1}")
    print(f"Indice: {row2}")
    print("=" * 65 + "\n")


def prompt_valid_key() -> str:
    while True:
        raw = input("\nIntroduceți cheia (minim 7 caractere): ")
        cleaned_key, err = validate_key(raw)
        if err:
            print(f"\n{err}")
            continue
        return cleaned_key


def prompt_valid_message(prompt_str: str) -> str:
    while True:
        raw = input(prompt_str)
        cleaned_msg, err = validate_message(raw)
        if err:
            print(f"\n{err}")
            continue
        return cleaned_msg


def main() -> None:
    print("=================================================================")
    print("   CIFRUL VIGENÈRE PENTRU LIMBA ROMÂNĂ (ALFABETUL CU 31 LITERE)  ")
    print("=================================================================")
    
    while True:
        print("\nMeniu principal:")
        print("  1. Criptare mesaj")
        print("  2. Decriptare mesaj")
        print("  3. Afișare alfabet și codificare (0..30)")
        print("  4. Ieșire")
        
        choice = input("\nAlegeți o opțiune (1-5): ").strip()
        
        if choice == "1":
            msg = prompt_valid_message("\nIntroduceți mesajul clar: ")
            key = prompt_valid_key()
            ciphertext = encrypt(msg, key)
            print("\nRezultatul criptării:")
            print(f"Mesaj prelucrat: {msg}")
            print(f"Cheie utilizată: {key}")
            print(f"Criptogramă:     {ciphertext}")
            display_calculation_table(msg, key, is_encrypt=True)
            
        elif choice == "2":
            cipher = prompt_valid_message("\nIntroduceți criptograma: ")
            key = prompt_valid_key()
            plaintext = decrypt(cipher, key)
            print("\nRezultatul decriptării:")
            print(f"Criptogramă:     {cipher}")
            print(f"Cheie utilizată: {key}")
            print(f"Mesaj decriptat: {plaintext}")
            display_calculation_table(cipher, key, is_encrypt=False)
            
        elif choice == "3":
            show_alphabet()
            
        elif choice == "4":
            print("\nProgram încheiat.")
            break
        else:
            print("Opțiune invalidă. Introduceți o cifră între 1 și 5.")


if __name__ == "__main__":
    main()
