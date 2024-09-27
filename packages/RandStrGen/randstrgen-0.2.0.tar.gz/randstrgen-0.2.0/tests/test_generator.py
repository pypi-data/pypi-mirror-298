# tests/test_generator.py

import unittest
from randstrgen import generate_random_string, generate_random_strings

class TestRandStrGen(unittest.TestCase):
    def test_generate_random_string_default(self):
        s = generate_random_string(10)
        self.assertEqual(len(s), 10)
        self.assertTrue(all(c.isupper() or c.isdigit() for c in s))

    def test_generate_random_string_with_all_types(self):
        s = generate_random_string(
            length=12,
            char_types=['uppercase', 'lowercase', 'digits', 'symbols'],
            first_char_type='letter'
        )
        self.assertEqual(len(s), 12)
        self.assertTrue(s[0].isalpha())
        self.assertTrue(any(c.islower() for c in s))
        self.assertTrue(any(c.isupper() for c in s))
        self.assertTrue(any(c.isdigit() for c in s))
        self.assertTrue(any(c in string.punctuation for c in s))

    def test_generate_random_strings_batch(self):
        batch = generate_random_strings(5, 8)
        self.assertEqual(len(batch), 5)
        for s in batch:
            self.assertEqual(len(s), 8)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_random_string(0)

    def test_invalid_char_type(self):
        with self.assertRaises(ValueError):
            generate_random_string(10, char_types=['invalid_type'])

    def test_invalid_first_char_type(self):
        with self.assertRaises(ValueError):
            generate_random_string(10, first_char_type='invalid_type')

    def test_generate_random_string_first_char_type(self):
        s = generate_random_string(10, char_types=['digits', 'letters'], first_char_type='letter')
        self.assertTrue(s[0].isalpha())

if __name__ == '__main__':
    unittest.main()
