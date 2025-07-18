import unittest
from osal.tts import TTS

class TestTTS(unittest.TestCase):
    def test_speak(self):
        tts = TTS()
        # This is a dummy test
        self.assertIsNotNone(tts)

if __name__ == '__main__':
    unittest.main()