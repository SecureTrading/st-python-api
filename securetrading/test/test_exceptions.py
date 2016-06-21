#!/usr/bin/env python
import unittest
from securetrading.test import abstract_test
import securetrading.exceptions


class Test_exception_SecureTradingError(abstract_test.TestCase):

    error_class = securetrading.SecureTradingError

    def test_errors(self):
        tests = [("1", [], "", "1"),
                 ("1", ["TESTING"], ["TESTING"], "1 TESTING"),
                 ("99", ["TESTING", "HERE"], ["TESTING", "HERE"],
                  "99 TESTING\nHERE"),
                 ("99", Exception("TESTING ME"), ["TESTING ME"],
                  "99 TESTING ME"),
                 ]
        for code, data, expected_data, expected_english in tests:
            actual = self.error_class(code, data=data)
            self.check_error(actual, expected_data, code, expected_english)


class Test_exception_ApiError(Test_exception_SecureTradingError):

    error_class = securetrading.ApiError


class Test_exception_HttpError(Test_exception_SecureTradingError):

    error_class = securetrading.HttpError


class Test_exception_ConnectionError(Test_exception_HttpError):

    error_class = securetrading.ConnectionError


class Test_exception_SendReceiveError(Test_exception_HttpError):

    error_class = securetrading.SendReceiveError

if __name__ == "__main__":
    unittest.main()
