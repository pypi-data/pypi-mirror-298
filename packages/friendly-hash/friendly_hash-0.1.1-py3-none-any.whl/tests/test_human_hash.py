import os
import unittest
from friendly_hash.friendly_hash import get_friendly_hash, rename_file

class TestFriendlyHash(unittest.TestCase):
    
    def test_get_friendly_hash(self):
        hash = get_friendly_hash('2024-07-05-09-15-18.bag')
        self.assertEqual(hash, 'peaceful-week')  # assuming 'peaceful-week' is the correct hash
    
    def test_rename_file(self):
        filename = '2024-07-05-09-15-18.bag'
        target_filename = 'peaceful-week-2024-07-05-09-15-18.bag'
        friendly_hash = 'peaceful-week'
        open(filename, 'w').close()  # create an empty file
        
        try:
            new_filename = rename_file(filename, friendly_hash)
            self.assertTrue(os.path.exists(target_filename))
            self.assertFalse(os.path.exists(filename))
        finally:
            if os.path.exists(new_filename):
                os.remove(new_filename)
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == '__main__':
    unittest.main()
