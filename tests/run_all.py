#!/usr/bin/env python3

import unittest
import sys

sys.path.append('.')

if __name__ == '__main__':
    all_tests = unittest.TestLoader().discover('./tests', pattern='test_*.py')
    unittest.TextTestRunner().run(all_tests)
