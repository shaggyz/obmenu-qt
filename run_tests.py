#!/usr/bin/env python3

import unittest

if __name__ == "__main__":
    all_tests = unittest.TestLoader().discover('ob_menu_qt/tests', pattern='test_*.py')
    unittest.TextTestRunner().run(all_tests)
