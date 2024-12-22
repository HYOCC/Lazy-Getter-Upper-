import unittest 
from home import create_find_location,create_map, create_map_window

class test(unittest.TestCase):
    def test_functions(self):
        self.assertEqual(create_find_location, '2A') 
        
    
    
if __name__ == '__main__':
    unittest.main() 