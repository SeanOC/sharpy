import unittest

class BasicTest(unittest.TestCase):
    
    def test_simple(self):
        import sharpy
        print "test"
        assert True