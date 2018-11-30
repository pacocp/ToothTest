import unittest
import os

class TestMetrics(unittest.TestCase):
    def test_dir(self):
        assert os.path.exists("ObserversEvaluations") == 0
