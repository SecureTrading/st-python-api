#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
from securetrading.test import abstract_test
import securetrading


class Test_Config(abstract_test.TestCase):

    def test_http_proxy(self):
        config = securetrading.Config()
        self.assertEqual(None, config.http_proxy)
        exp_message = "A dict is required with https only e.g:\
 {'https':'https://IP:PORT'}"
        tests = [("HTTPPROXY", AssertionError),
                 (["1.3.4.3"], AssertionError),
                 ({"https": "https://1.1.1.1"}, None),
                 ({"http": "http://1.1.1.1"}, AssertionError),
                 ({"https": "https://1.1.1.1", "http": "http://1.1.1.1"},
                  AssertionError),
                 ]

        for proxy_value, exp_exception in tests:
            if exp_exception is None:
                config.http_proxy = proxy_value
                self.assertEqual(proxy_value, config.http_proxy)
            else:
                self.assertRaisesRegexp(exp_exception,
                                        exp_message,
                                        setattr,
                                        config,
                                        "http_proxy",
                                        proxy_value)

    def test_http_max_allowed_connection_time(self):
        config = securetrading.Config()
        self.assertEqual(10, config.http_max_allowed_connection_time)
        exp_message = "An int or float is required for the timeout"
        tests = [("30", AssertionError),
                 ([30], AssertionError),
                 ({"max": 30.10}, AssertionError),
                 (30, None),
                 (134.56, None),
                 ]

        for max_value, exp_exception in tests:
            if exp_exception is None:
                config.http_max_allowed_connection_time = max_value
                self.assertEqual(max_value,
                                 config.http_max_allowed_connection_time)
            else:
                self.assertRaisesRegexp(exp_exception,
                                        exp_message,
                                        setattr,
                                        config,
                                        "http_max_allowed_connection_time",
                                        max_value)

    def test_http_connect_timeout(self):
        config = securetrading.Config()
        self.assertEqual(10, config.http_connect_timeout)
        exp_message = "An int or float is required for the timeout"
        tests = [("40", AssertionError),
                 ([40], AssertionError),
                 ({"max": 40.10}, AssertionError),
                 (40, None),
                 (134.56, None),
                 ]

        for timeout_value, exp_exception in tests:
            if exp_exception is None:
                config.http_connect_timeout = timeout_value
                self.assertEqual(timeout_value, config.http_connect_timeout)
            else:
                self.assertRaisesRegexp(exp_exception,
                                        exp_message,
                                        setattr,
                                        config,
                                        "http_connect_timeout",
                                        timeout_value)

    def test_http_receive_timeout(self):
        config = securetrading.Config()
        self.assertEqual(60, config.http_receive_timeout)
        exp_message = "An int or float is required for the timeout"
        tests = [("10", AssertionError),
                 ([10], AssertionError),
                 ({"max": 10.10}, AssertionError),
                 (10, None),
                 (234.56, None),
                 ]

        for timeout_value, exp_exception in tests:
            if exp_exception is None:
                config.http_receive_timeout = timeout_value
                self.assertEqual(timeout_value, config.http_receive_timeout)
            else:
                self.assertRaisesRegexp(exp_exception,
                                        exp_message,
                                        setattr,
                                        config,
                                        "http_receive_timeout",
                                        timeout_value)

    def test_http_max_retries(self):
        config = securetrading.Config()
        self.assertEqual(6, config.http_max_retries)
        exp_message = "An int is required for maximum number of retries"
        tests = [("10", AssertionError),
                 ([10], AssertionError),
                 ({"max": 10.10}, AssertionError),
                 (10, None),
                 (234.56, AssertionError),
                 ]

        for max_value, exp_exception in tests:
            if exp_exception is None:
                config.http_max_retries = max_value
                self.assertEqual(max_value, config.http_max_retries)
            else:
                self.assertRaisesRegexp(exp_exception,
                                        exp_message,
                                        setattr,
                                        config,
                                        "http_max_retries",
                                        max_value)

    def test_http_retry_sleep(self):
        config = securetrading.Config()
        self.assertEqual(0.5, config.http_retry_sleep)
        exp_message = "An int or float is required for the sleep period"
        tests = [("10", AssertionError),
                 ([10], AssertionError),
                 ({"max": 10.10}, AssertionError),
                 (10, None),
                 (234.56, None),
                 ]

        for sleep_value, exp_exception in tests:
            if exp_exception is None:
                config.http_retry_sleep = sleep_value
                self.assertEqual(sleep_value, config.http_retry_sleep)
            else:
                self.assertRaisesRegexp(exp_exception,
                                        exp_message,
                                        setattr,
                                        config,
                                        "http_retry_sleep",
                                        sleep_value)

    def test_datacenterurl(self):
        config = securetrading.Config()
        self.assertEqual("https://webservices.securetrading.net",
                         config.datacenterurl)
        tests = [("2.45", "2.45"),
                 (8.65, 8.65),
                 ("http://some.address.com", "http://some.address.com"),
                 (3, 3),
                 ([3, "3", 2.5], [3, "3", 2.5]),
                 ({"value": 2}, {"value": 2}),
                 (None, None),
                 ("", ""),
                 ]

        for set_value, exp_value in tests:
            config.datacenterurl = set_value
            self.assertEqual(exp_value, config.datacenterurl)

    def test_jsonversion(self):
        config = securetrading.Config()
        self.assertEqual("1.00", config.jsonversion)
        tests = [("2.45", "2.45"),
                 (8.65, 8.65),
                 ("one", "one"),
                 (3, 3),
                 ([3, "3", 2.5], [3, "3", 2.5]),
                 ({"value": 2}, {"value": 2}),
                 (None, None),
                 ("", ""),
                 ]

        for set_value, exp_value in tests:
            config.jsonversion = set_value
            self.assertEqual(exp_value, config.jsonversion)

    def test_username(self):
        config = securetrading.Config()
        self.assertEqual("", config.username)
        tests = [("2.45", "2.45"),
                 (8.65, 8.65),
                 ("one", "one"),
                 (3, 3),
                 ([3, "3", 2.5], [3, "3", 2.5]),
                 ({"value": 2}, {"value": 2}),
                 (None, None),
                 ("", ""),
                 ]

        for set_value, exp_value in tests:
            config.username = set_value
            self.assertEqual(exp_value, config.username)

    def test_password(self):
        config = securetrading.Config()
        self.assertEqual("", config.password)
        tests = [("2.45", "2.45"),
                 (8.65, 8.65),
                 ("one", "one"),
                 (3, 3),
                 ([3, "3", 2.5], [3, "3", 2.5]),
                 ({"value": 2}, {"value": 2}),
                 (None, None),
                 ("", ""),
                 ]

        for set_value, exp_value in tests:
            config.password = set_value
            self.assertEqual(exp_value, config.password)

    def test_ssl_certificate_file(self):
        config = securetrading.Config()
        self.assertEqual(None, config.ssl_certificate_file)
        tests = [("2.45", "2.45"),
                 (8.65, 8.65),
                 ("one", "one"),
                 (3, 3),
                 ([3, "3", 2.5], [3, "3", 2.5]),
                 ({"value": 2}, {"value": 2}),
                 (None, None),
                 ("", ""),
                 ("/usr/local/certFile", "/usr/local/certFile"),
                 ]

        for set_value, exp_value in tests:
            config.ssl_certificate_file = set_value
            self.assertEqual(exp_value, config.ssl_certificate_file)

    def test_locale(self):
        config = securetrading.Config()
        self.assertEqual("en_gb", config.locale)
        tests = [("fr_fr", None, ""),
                 ("de_de", None, ""),
                 ("TESTING", Exception, "Please specifiy a valid locale according\
 to, the locale module"),
                 ]

        for locale, exp_exception, exp_message in tests:
            if exp_exception is None:
                config.locale = locale
                self.assertEqual(locale, config.locale)
            else:
                self.assertRaisesRegexp(exp_exception,
                                        exp_message,
                                        setattr,
                                        config,
                                        "locale",
                                        locale)

if __name__ == "__main__":
    unittest.main()
