"""
Comprehensive unit tests for Romanian Caesar Cipher (Tasks 1.1 & 1.2).
"""

import unittest
from caesar_cipher import (
    ROMANIAN_ALPHABET,
    ALPHABET_SIZE,
    CHAR_TO_INDEX,
    INDEX_TO_CHAR,
    normalize_input_text,
    validate_and_clean_text,
    validate_key,
    validate_keyword,
    caesar_encrypt,
    caesar_decrypt,
    generate_permuted_alphabet,
    caesar_permuted_encrypt,
    caesar_permuted_decrypt
)


class TestCaesarCipherRomanian(unittest.TestCase):

    def test_alphabet_specification(self):
        """Table 2 alphabet size and exact ordering."""
        self.assertEqual(len(ROMANIAN_ALPHABET), 31)
        self.assertEqual(ALPHABET_SIZE, 31)

        expected = [
            'A', 'Ă', 'Â', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'Î', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
            'R', 'S', 'Ș', 'T', 'Ț', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ]
        self.assertEqual(ROMANIAN_ALPHABET, expected)
        self.assertEqual(CHAR_TO_INDEX['A'], 0)
        self.assertEqual(CHAR_TO_INDEX['Ă'], 1)
        self.assertEqual(CHAR_TO_INDEX['Â'], 2)
        self.assertEqual(CHAR_TO_INDEX['Ș'], 22)
        self.assertEqual(CHAR_TO_INDEX['Ț'], 24)
        self.assertEqual(CHAR_TO_INDEX['Z'], 30)
        self.assertEqual(INDEX_TO_CHAR[30], 'Z')

    def test_key_validation(self):
        """Numeric shift key must be integer between 1 and 30 inclusive."""
        for k in range(1, 31):
            valid, val, _ = validate_key(str(k))
            self.assertTrue(valid)
            self.assertEqual(val, k)

        # Invalid bounds
        valid, _, err = validate_key("0")
        self.assertFalse(valid)
        self.assertIn("out of range", err)

        valid, _, err = validate_key("31")
        self.assertFalse(valid)
        self.assertIn("out of range", err)

        valid, _, err = validate_key("-5")
        self.assertFalse(valid)
        self.assertIn("out of range", err)

        # Non-integer
        valid, _, err = validate_key("abc")
        self.assertFalse(valid)
        self.assertIn("must be an integer", err)

    def test_text_validation_and_cleaning(self):
        """Text must allow Romanian letters and spaces, reject invalid chars."""
        # Spaces removed and lowercase capitalized
        valid, clean, rej, _ = validate_and_clean_text("salut lume")
        self.assertTrue(valid)
        self.assertEqual(clean, "SALUTLUME")
        self.assertEqual(rej, [])

        # Diacritics
        valid, clean, _, _ = validate_and_clean_text("învățământul românesc")
        self.assertTrue(valid)
        self.assertEqual(clean, "ÎNVĂȚĂMÂNTULROMÂNESC")

        # Cedilla variants converted to comma-below
        valid, clean, _, _ = validate_and_clean_text("Ştefan cel Mare şi Sfânt ţara")
        self.assertTrue(valid)
        self.assertEqual(clean, "ȘTEFANCELMAREȘISFÂNTȚARA")

        # Invalid characters (digits, symbols, foreign letters)
        valid, clean, rej, err = validate_and_clean_text("Parola123!@#")
        self.assertFalse(valid)
        self.assertIn("1", rej)
        self.assertIn("2", rej)
        self.assertIn("3", rej)
        self.assertIn("!", rej)
        self.assertIn("Invalid character(s) rejected", err)

        # Empty / whitespace-only text
        valid, _, _, err = validate_and_clean_text("   ")
        self.assertFalse(valid)

    def test_keyword_validation(self):
        """Keyword must have only Romanian letters and length >= 7."""
        # Valid keyword
        valid, clean, _, _ = validate_keyword("criptografie")
        self.assertTrue(valid)
        self.assertEqual(clean, "CRIPTOGRAFIE")

        # Valid with Romanian diacritics
        valid, clean, _, _ = validate_keyword("învățător")
        self.assertTrue(valid)
        self.assertEqual(clean, "ÎNVĂȚĂTOR")

        # Too short (< 7)
        valid, _, _, err = validate_keyword("salut")
        self.assertFalse(valid)
        self.assertIn("too short", err)

        # Invalid characters
        valid, _, rej, err = validate_keyword("cripto123")
        self.assertFalse(valid)
        self.assertIn("1", rej)
        self.assertIn("Invalid character(s) in keyword rejected", err)

    def test_caesar_standard_roundtrip(self):
        """Verify Task 1.1 encryption and decryption consistency for all keys."""
        test_message = "ACESTAESTEUNTESTPENTRUCIFRULCEZARCUĂÂÎȘȚ"
        for k in range(1, 31):
            cipher = caesar_encrypt(test_message, k)
            recovered = caesar_decrypt(cipher, k)
            self.assertEqual(recovered, test_message)

    def test_caesar_standard_manual_trace(self):
        """Check exact manual shifting and wrap-around."""
        # 'Z' has index 30. With k=3: (30 + 3) % 31 = 33 % 31 = 2 -> 'Â'
        self.assertEqual(caesar_encrypt("Z", 3), "Â")
        self.assertEqual(caesar_decrypt("Â", 3), "Z")

        # 'A' (0) + 1 = 'Ă' (1)
        self.assertEqual(caesar_encrypt("A", 1), "Ă")
        self.assertEqual(caesar_decrypt("Ă", 1), "A")

        # 'Ț' (24) + 1 = 'U' (25)
        self.assertEqual(caesar_encrypt("Ț", 1), "U")
        self.assertEqual(caesar_decrypt("U", 1), "Ț")

    def test_permuted_alphabet_generation(self):
        """Verify Task 1.2 permuted alphabet satisfies all rules."""
        keyword = "CRIPTOGRAFIE"  # distinct: C, R, I, P, T, O, G, A, F, E
        permuted = generate_permuted_alphabet(keyword)

        self.assertEqual(len(permuted), 31)
        self.assertEqual(len(set(permuted)), 31)  # All distinct

        # Keyword unique letters must be at the beginning
        expected_prefix = ['C', 'R', 'I', 'P', 'T', 'O', 'G', 'A', 'F', 'E']
        self.assertEqual(permuted[:len(expected_prefix)], expected_prefix)

        # Remaining letters must be in Romanian alphabetical order
        remaining_in_permuted = permuted[len(expected_prefix):]
        remaining_expected = [c for c in ROMANIAN_ALPHABET if c not in expected_prefix]
        self.assertEqual(remaining_in_permuted, remaining_expected)

    def test_caesar_permuted_roundtrip(self):
        """Verify Task 1.2 encryption and decryption consistency."""
        test_message = "SECURITATEAINFORMATIEIÎNVĂȚĂMÂNT"
        keyword = "ALGORITM"
        for k in range(1, 31):
            cipher, _ = caesar_permuted_encrypt(test_message, k, keyword)
            recovered, _ = caesar_permuted_decrypt(cipher, k, keyword)
            self.assertEqual(recovered, test_message)


if __name__ == "__main__":
    unittest.main()
