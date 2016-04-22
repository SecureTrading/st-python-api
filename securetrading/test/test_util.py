#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
import re
import securetrading
import securetrading.util as util
from securetrading.test import abstract_test
import sys


class Test_util(abstract_test.TestCase):

    def test__get_random(self):

        test_cases = [(10, "0123456789abcdefghjkmnpqrtuvwxy"),
                      (100, "0123456789abcdefghjkmnpqrtuvwxy"),
                      (100, "0123456789"),
                      (50, "abc"),
                      (50, "!\"$%^&*();:'@#~[{]}<,>./?\\|"),
                      (50, self.uni),
                      (10, list("0123456789abcdefghjkmnpqrtuvwxy")),
                      (50, list("abc")),
                      (50, list(self.uni)),
                      ]

        for length, all_chars in test_cases:
            results = set()
            check_unique = 100
            for i in range(check_unique):
                actual = util._get_random(length, all_chars=all_chars)
                regex = "[{0}]{{1}}".format(re.escape("".join(all_chars)),
                                            length)
                self.assertRegexpMatches(actual, regex,
                                         msg="Result {0} != {1}".
                                         format(actual, regex))
                results.add(actual)
            msg = "Not all generated results were unique {0} != {1}".\
                format(len(results), check_unique)
            self.assertEqual(len(results), check_unique, msg=msg)

    def test__is_python_2(self):
        if sys.version.startswith("2"):
            self.assertTrue(util._is_python_2())
        else:
            self.assertFalse(util._is_python_2())

    def test__get_errormesage(self):
        tests = [({}, '1', 'Generic error'),
                 ({}, '2', "Secure Trading API requires the 'requests' \
library"),
                 ({}, '4', 'Send error'),
                 ({}, '5', 'Receive error'),
                 ({}, '6', 'Invalid credentials provided'),
                 ({}, '7', 'An issue occured whilst trying to connect to \
Secure Trading servers'),
                 ({}, '8', 'Unexpected error connecting to Secure Trading servers. \
If the problem persists please contact support@securetrading.com'),
                 ({}, '9', 'Unknown error. If this persists please contact \
Secure Trading'),
                 ({"locale": "fr_fr"}, '1', 'erreur g\xe9n\xe9rique'),
                 ({"locale": "fr_fr"}, '9', "Erreur inconnue. Si cela persiste \
s'il vous pla\xeet contacter Secure Trading"),
                 ]

        for config_data, code, expected in tests:
            config = securetrading.Config()
            for key in config_data:
                setattr(config, key, config_data[key])
            phrasebook = securetrading.PhraseBook(config)
            actual = util._get_errormessage(code, phrasebook)
            self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
