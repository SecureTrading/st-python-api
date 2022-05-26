#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
import re
import securetrading
import securetrading.util as util
from securetrading.test import abstract_test
import sys
import six


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
                regex = "[{0}]{{{1}}}".format(re.escape("".join(all_chars)),
                                              length)
                six.assertRegex(self, actual, regex,
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
        tests = [({}, '1', 'GATEWAYERRMSG', 'Generic error'),
                 ({}, '2', 'GATEWAYERRMSG', "Trust Payments API requires the\
 'requests' library"),
                 ({}, '4', 'GATEWAYERRMSG', 'Send error'),
                 ({}, '5', 'GATEWAYERRMSG', 'Receive error'),
                 ({}, '6', 'GATEWAYERRMSG', 'Invalid credentials provided'),
                 ({}, '7', 'GATEWAYERRMSG', 'An issue occured whilst trying to\
 connect to Trust Payments servers'),
                 ({}, '8', 'GATEWAYERRMSG', 'Unexpected error connecting to\
 Trust Payments servers. If the problem persists please contact\
 support@trustpayments.com'),
                 ({}, '9', 'GATEWAYERRMSG', 'Unknown error. If this persists \
please contact Trust Payments'),
                 ({"locale": "fr_fr"}, '1', 'GATEWAYERRMSG',
                  'Erreur g\xe9n\xe9rique'),
                 ({"locale": "fr_fr"}, '9', 'GATEWAYERRMSG',
                  "Erreur inconnue. Si cela persiste veuillez contacter \
Trust Payments"),
                 ({"locale": "de_de"}, '1', 'GATEWAYERRMSG',
                  'Allgemeiner Fehler'),
                 ({"locale": "de_de"}, '9', 'GATEWAYERRMSG',
                  "Unbekannter Fehler. Wenn dieser weiterhin besteht, \
kontaktieren Sie bitte Trust Payments"),
                 ({}, '99', "GATEWAYERRMSG", 'GATEWAYERRMSG'),
                 ({"locale": "fr_fr"}, '99', 'GATEWAYERRMSG', 'GATEWAYERRMSG'),
                 ({"locale": "de_de"}, '99', 'GATEWAYERRMSG', 'GATEWAYERRMSG'),
                 ]

        for config_data, code, gateway_err_msg, expected in tests:
            config = securetrading.Config()
            for key in config_data:
                setattr(config, key, config_data[key])
            phrasebook = securetrading.PhraseBook(config)
            actual = util._get_errormessage(code, gateway_err_msg, phrasebook)
            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
