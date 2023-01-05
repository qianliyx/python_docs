class Student(object):
    def __init__(self, name: str = '', score: int = 0):
        self.name = name
        self.score = score
        
    def get_grade(self):
        if self.score > 80:
            return '优秀'
        else:
            return '良好'

        
        

import unittest

class TestABS(unittest.TestCase):
    
    def test_greater_80(self):
        a = Student('a',90)
        self.assertEqual(a.get_grade(),'优秀')
        
    def test_less_80(self):
        a = Student('a',70)
        self.assertEqual(a.get_grade(),'良好')

        
if __name__ == '__main__':
    unittest.main()