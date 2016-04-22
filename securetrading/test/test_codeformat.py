#!/usr/bin/env python
from __future__ import unicode_literals
import sys
import unittest
from securetrading.test import abstract_test
import glob
import os
import pkgutil
import securetrading.util as util

try:
    import pep8
except ImportError:
    pep8 = None


class Test_CodeFormat(abstract_test.TestCase):

    def get_files(self, directory):
        return glob.glob(os.path.join(directory, "*.py"))

    def test_pep8_conformance(self):
        if pep8 is not None:
            ignore_error_codes = []

            loader = pkgutil.get_loader('securetrading')
            if util._is_python_2():
                base_path = loader.filename
            else:
                base_path = os.path.split(loader.path)[0]

            test_cases = ["",
                          "test",
                          ]

            for directory in test_cases:
                path = os.path.join(base_path, directory)
                if os.path.exists(path):
                    files = self.get_files(path)
                    """Test that we conform to PEP8."""

                    results = []
                    # Need to check if pep8 is installed before running
                    for f in sorted(files):
                        pep8_style = pep8.StyleGuide(quiet=True,
                                                     ignore=ignore_error_codes)
                        result = pep8_style.check_files([f])
                        if result.total_errors != 0:
                            results.append("Found code style errors (and warnings)\
     Run 'pep8 --show-source {0}'.".format(f))

                    self.assertEqual(0, len(results),
                                     "results {0}".format(results))
        else:
            print("PEP8 module is not installed skipping test.")

if __name__ == '__main__':
    unittest.main()
