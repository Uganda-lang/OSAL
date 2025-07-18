import unittest
from osal.textgen import TextGenerator

class TestTextGenerator(unittest.TestCase):
    def test_generate(self):
        textgen = TextGenerator()
        # This is a dummy test
        self.assertIsNotNone(textgen)

if __name__ == '__main__':
    unittest.main()