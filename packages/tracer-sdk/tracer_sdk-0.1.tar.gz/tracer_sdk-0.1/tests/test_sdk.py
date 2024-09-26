# tests/test_sdk.py

import unittest
from tracer.sdk import initiator

class TestAnkitSDK(unittest.TestCase):
    def test_ankit(self):
        self.assertEqual(initiator(), "Hello from Ankit SDK!")

if __name__ == '__main__':
    unittest.main()