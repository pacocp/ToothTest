import unittest

class OSTest(unittest.TestCase):
    def dir_test(self):
        assert os.path.exists("ObserversEvaluations") == 1
