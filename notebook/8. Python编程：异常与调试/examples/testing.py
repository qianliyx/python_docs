import unittest

class TestABS(unittest.TestCase):
    
    def test_example1(self):
        self.assertEqual(abs(1),1)
        
    def test_example2(self):
        self.assertEqual(abs(-1),1)
        
    def test_example3(self):
        self.assertEqual(abs(0),0)
        
    def test_example4(self):
        a = '1'
        with self.assertRaises(TypeError):
            abs(a)
        
if __name__ == '__main__':
    unittest.main()