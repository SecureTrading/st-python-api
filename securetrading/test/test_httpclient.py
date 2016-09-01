#!/usr/bin/env python
from __future__ import unicode_literals
import sys
import unittest
import securetrading
from securetrading import ConnectionError
from securetrading import SendReceiveError
from securetrading.test import abstract_test
import requests
from requests.exceptions import ConnectTimeout
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import RequestException
import platform
import time


class Test_httpclient_GenericHTTPClient(abstract_test.TestCase):

    client = securetrading.httpclient.GenericHTTPClient

    def setUp(self):
        config = securetrading.Config()
        self.http_client = self.client(config)

    def test__get_requests_lib(self):
        original_requests = requests

        class Mock(object):
            __version__ = "2.9.0"

        mock1 = Mock()
        mock2 = Mock()
        mock2.__version__ = "50.2.3"
        mock3 = Mock()
        mock3.__version__ = "2.8.9"
        mock4 = None

        tests = [(mock1, None),
                 (mock2, None),
                 (mock3, securetrading.SecureTradingError),
                 (mock4, securetrading.SecureTradingError),
                 ]

        for (mock_requests, exp_exception) in tests:
            try:
                sys.modules["requests"] = mock_requests
                func = securetrading.httpclient._get_requests_lib
                if exp_exception is None:
                    func()
                else:
                    self.assertRaises(exp_exception,
                                      func)
            finally:
                sys.modules["requests"] = original_requests

    def test__get_client(self):
        original_requests = securetrading.httpclient.requests
        config = securetrading.Config()
        request_reference = self.uni
        httpclient = securetrading.httpclient

        try:
            securetrading.httpclient.requests = True
            client = httpclient._get_client(request_reference, config)
            self.assertTrue(isinstance(client,
                                       httpclient.HTTPRequestsClient))

            securetrading.httpclient.requests = False
            self.assertRaises(securetrading.SecureTradingError,
                              httpclient._get_client,
                              request_reference,
                              config)
        finally:
            securetrading.httpclient.requests = original_requests

    def test__close(self):
        self.assertRaises(NotImplementedError, self.http_client._close)

    def test__receive(self):
        self.assertRaises(NotImplementedError, self.http_client._receive)

    def test__send(self):
        args = ("https://www.securetrading.com",
                {"request": "data"},
                "request_reference",
                )

        self.assertRaises(NotImplementedError, self.http_client._send, *args)

    def test__connect(self):
        test_urls = ["https://www.securetrading.com",
                     "http://www.securetading.com",
                     ]
        for url in test_urls:
            self.assertRaises(NotImplementedError,
                              self.http_client._connect, url)

    def test__get_headers(self, expected_agent_string=None):
        lib_version = "1.00"
        os = platform.platform()
        python_version = platform.python_version()

        if expected_agent_string is None:
            expected_agent_string = "Python-{0}".format(python_version)

        content_type = "application/json;charset=utf-8"
        tests = [("abc", "v1", {"Content-Type": content_type,
                                "Accept": "application/json",
                                "Accept-Encoding": "gzip",
                                "REQUESTREFERENCE": "abc",
                                "User-Agent": expected_agent_string,
                                "VERSIONINFO": "v1",
                                'Connection': 'close',
                                }
                  ),
                 ("123456789", "v2", {"Content-Type": content_type,
                                      "Accept": "application/json",
                                      "Accept-Encoding": "gzip",
                                      "REQUESTREFERENCE": "123456789",
                                      "User-Agent": expected_agent_string,
                                      "VERSIONINFO": "v2",
                                      'Connection': 'close',
                                      }
                  ),
                 ("abcd12345", "v3", {"Content-Type": content_type,
                                      "Accept": "application/json",
                                      "Accept-Encoding": "gzip",
                                      "REQUESTREFERENCE": "abcd12345",
                                      "User-Agent": expected_agent_string,
                                      "VERSIONINFO": "v3",
                                      'Connection': 'close',
                                      }
                  ),
                 (self.uni, "v4", {"Content-Type": content_type,
                                   "Accept": "application/json",
                                   "Accept-Encoding": "gzip",
                                   "REQUESTREFERENCE": self.uni,
                                   "User-Agent": expected_agent_string,
                                   "VERSIONINFO": "v4",
                                   'Connection': 'close',
                                   }
                  ),
                 ]
        tmp = securetrading.version_info
        try:
            for request_reference, version_info, expected in tests:
                securetrading.version_info = version_info
                actual = self.http_client._get_headers(request_reference)
                self.assertEqual(actual, expected)
        finally:
            # Rest for other tests
            securetrading.version_info = tmp

    @unittest.skip("Placeholder method")
    def test__verify_response(self):
        pass  # Code is overriden by some child classes

    def test__handle_invalid_response(self):
        tests = [(401, ConnectionError,
                  "6 HTTP code 401", ["HTTP code 401"], "6"),
                 (404, ConnectionError,
                  "8 HTTP code 404",
                  ["HTTP code 404"], "8"),
                 (500, ConnectionError,
                  "8 HTTP code 500",
                  ["HTTP code 500"], "8"
                  ),
                 (300, ConnectionError,
                  "8 HTTP code 300",
                  ["HTTP code 300"], "8",
                  ),
                 ]

        for code, exp_exception, exp_english, exp_data, exp_code in tests:
            self.check_st_exception(exp_exception, exp_data, exp_english,
                                    exp_code,
                                    self.http_client._handle_invalid_response,
                                    func_args=(code, "content"))

    def test__get_connection_time_out(self):
        tests = [(time.time(), 10, 5, False, "5"),
                 # The regular expressions due to changes in box times
                 (time.time(), 4, 5, False, "[34].\d+"),
                 (time.time()-2, 4, 5, False, "[12].\d+"),
                 (time.time()-2, 4, 3, False, "[12].\d+"),
                 ]

        config = securetrading.Config()

        for start_time, max_connection_time, connect_time_out, \
                expected_timed_out, expected_connection_time in tests:
            config.http_max_allowed_connection_time = max_connection_time
            config.http_connect_timeout = connect_time_out
            client = self.client(config)
            (timed_out, connection_time) = client._get_connection_time_out(
                start_time)
            self.assertEqual(timed_out, expected_timed_out)
            self.assertRegexpMatches("{0}".format(connection_time),
                                     expected_connection_time)

    def test__main(self):

        c2_exp_eng = "7 Connect Error"

        tests = [(None, None, (200, "Success"), None, None, None,
                  None, None, None, None, "Success"),
                 (Exception("Connect Error"), None, None, None, None,
                  None, ConnectionError, ["Connect Error"], c2_exp_eng,
                  "7", None,),
                 (None, Exception("Send Error"), None, None, None, None,
                  SendReceiveError, ["Send Error"], "4 Send Error", "4",
                  None),
                 (None, None, None, Exception("Receive Error"), None,
                  None, SendReceiveError,
                  ["Receive Error"], "4 Receive Error", "4", None,
                  ),
                 (None, None, (200, "Verification Error"), None,
                  Exception("Verify Error"), None, Exception, None,
                  "Verify Error", None, None,
                  ),
                 (None, None, (200, "Closing Error"), None, None,
                  Exception("Close Error"), Exception, None,
                  "Close Error", None, None,
                  ),
                 (Exception("Connect Error"), None, None, None, None,
                  Exception("Close"), ConnectionError, ["Connect Error"],
                  "7 Connect Error", "7", None,
                  # Connect Error takes precedence
                  ),
                 (None, Exception("Send Error"), None, None, None,
                  Exception("Close"), Exception, None, "Close", None,
                  None),  # The close Exception takes precedence
                 (None, None, None, Exception("Receive Error"), None,
                  Exception("Close"), Exception, None, "Close", None,
                  None),  # The close Exception takes precedence
                 (None, None, None, None, Exception("Verify Error"),
                  Exception("Close"), Exception, None, "Close", None,
                  None),  # The close Exception takes precedence
                 ]

        config = securetrading.Config()

        for connect_raises, send_raises, receive_response, receive_raises,\
                verify_raises, close_raises, exp_exception, exp_data,\
                exp_english, exp_code, exp_response in tests:
            mock_client = self.client(config)
            mock_client._connect = self.mock_method(exception=connect_raises)
            mock_client._send = self.mock_method(exception=send_raises)
            mock_client._receive = self.mock_method(result=receive_response,
                                                    exception=receive_raises)
            mock_client._verify_response =\
                self.mock_method(exception=verify_raises)
            mock_client._close = self.mock_method(exception=close_raises)

            # As we have mocked all of the methods, the args have no value
            main_args = ("https://www.securetrading.com",
                         {"request": "data"},
                         "request_reference",
                         "version_info")

            if exp_exception:
                self.check_st_exception(exp_exception, exp_data, exp_english,
                                        exp_code, mock_client._main,
                                        func_args=main_args)
            else:
                actual = mock_client._main(*main_args)
                self.assertEqual(actual, exp_response)


class Test_httpclient_HTTPRequestsClient(Test_httpclient_GenericHTTPClient):

    client = securetrading.httpclient.HTTPRequestsClient

    @unittest.skip("Placeholder method")
    def test__close(self):
        pass  # Code is overriden to be ignored

    @unittest.skip("Placeholder method")
    def test__connect(self):
        pass  # Code is overriden to be ignored

    def test__get_headers(self, expected_agent_string=None):
        python_version = platform.python_version()
        requests_user_agent = requests.utils.default_user_agent()
        if expected_agent_string is None:
            expected_agent_string = "Python\
-{0}:{1}".format(python_version, requests_user_agent)
        super(Test_httpclient_HTTPRequestsClient,
              self
              ).test__get_headers(expected_agent_string=expected_agent_string)

    def test__send(self):

        c1_exp_data = ["request_reference Maximum time reached whilst \
trying to connect to https://www.securetrading.com"]
        c1_exp_msg = "7 request_reference Maximum time reached whilst \
trying to connect to https://www.securetrading.com"

        c2_exp_data = c1_exp_data
        c2_exp_msg = c1_exp_msg

        c3_exp_data = c1_exp_data
        c3_exp_msg = c1_exp_msg

        c7_exp_data = ["request_reference Maximum number of attempts reached \
whilst trying to connect to https://www.securetrading.com"]
        c7_exp_msg = "7 request_reference Maximum number of attempts reached \
whilst trying to connect to https://www.securetrading.com"

        c8_exp_data = ["request_reference Maximum number of attempts reached \
whilst trying to connect to https://www.securetrading.com"]
        c8_exp_msg = c7_exp_msg

        c9_exp_data = ["request_reference Maximum number of attempts reached \
whilst trying to connect to https://www.securetrading.com"]
        c9_exp_msg = c7_exp_msg

        c14_exp_msg = "8 Some other error"

        c15_exp_msg = "8 Some other error"

        c16_exp_msg = c1_exp_msg

        c17_exp_msg = c7_exp_msg

        tests = [(-1, 50, [None], ConnectionError, c1_exp_data,
                  c1_exp_msg, "7", None),
                 (0, 50, [ConnectTimeout], ConnectionError, c2_exp_data,
                  c2_exp_msg, "7", None),
                 (1, 50, [ConnectTimeout] * 100, ConnectionError, c3_exp_data,
                  c3_exp_msg, "7", None),
                 (50, 50, ["Successful response"], None, None, None, None,
                  "Successful response"),
                 (50, 50, [ConnectTimeout, "Successful response"], None, None,
                  None, None, "Successful response"),
                 (50, 50, [ConnectTimeout, ConnectTimeout,
                           "Successful response"], None, None, None, None,
                  "Successful response"),
                 (50, -1, [None], ConnectionError, c7_exp_data, c7_exp_msg,
                  "7", None),
                 (50, 0, [ConnectTimeout], ConnectionError, c8_exp_data,
                  c8_exp_msg, "7", None),
                 (50, 1, [ConnectTimeout] * 2, ConnectionError, c9_exp_data,
                  c9_exp_msg, "7", None),
                 (50, 0, ["Successful response"], None, None, None, None,
                  "Successful response"),
                 (50, 1, ["Successful response"], None, None, None, None,
                  "Successful response"),
                 (50, 2, [ConnectTimeout, "Successful response"],
                  None, None, None, None, "Successful response"),
                 (50, 50, [ConnectTimeout, RequestsConnectionError,
                           "Successful response"],
                  None, None, None, None, "Successful response"),
                 (50, 50, [Exception("Some other error")], ConnectionError,
                  ["Some other error"], c14_exp_msg, "8", None),
                 (50, 50, [ConnectTimeout, RequestsConnectionError,
                           Exception("Some other error")],
                  ConnectionError, ["Some other error"], c15_exp_msg,
                  "8", None),
                 (50, 50, [RequestException], ConnectionError, [""],
                  "7", "7", None),
                 (50, 50, [ConnectTimeout, RequestsConnectionError,
                           RequestException], ConnectionError, [""],
                  "7", "7", None),
                 ]
        original_request = requests.request
        try:
            for max_timeout, max_retry, request_responses, \
                    exp_exception, exp_data, exp_english, exp_code, \
                    exp_response in tests:
                config = securetrading.Config()
                config.http_max_allowed_connection_time = max_timeout
                config.http_max_retries = max_retry
                mock_client = securetrading.httpclient.\
                    HTTPRequestsClient(config)
                requests.request = self.mock_method(
                    multiple_calls=request_responses)
                # As we have mocked the requests.request,
                # the args have no value
                send_args = ("https://www.securetrading.com",
                             {"requestreference": "data"},
                             "request_reference",
                             )
                if exp_exception:
                    self.check_st_exception(exp_exception, exp_data,
                                            exp_english, exp_code,
                                            mock_client._send,
                                            func_args=send_args)
                else:
                    mock_client._send(*send_args)
                    self.assertEqual(mock_client.response, exp_response)
        finally:
            requests.request = original_request

    def test_handle_exception(self):
        tests = [(RequestException(), [''], "7", "7"),
                 (ConnectTimeout(), [''], "7", "7"),
                 (RequestsConnectionError(), [''], "7", "7"),
                 (Exception("Any other exception"),
                  ["Any other exception"],
                  "8 Any other exception", "8"
                  ),
                 ]

        for exception, exp_data, exp_english, exp_code in tests:
            self.check_st_exception(ConnectionError,
                                    exp_data, exp_english, exp_code,
                                    self.http_client._handle_exception,
                                    func_args=(exception,))

    def test__receive(self):
        tests = [(b"Text", 200, None, None, None, None, (200, "Text")),
                 (b"Different Text", 200, None, None, None, None,
                  (200, "Different Text")
                  ),
                 (self.byt_uni, 200, None, None, None, None,
                  (200, self.uni)),
                 (b"Invalid", 500, ConnectionError,
                  ["HTTP code 500"],
                  "8 HTTP code 500",
                  "8", None
                  ),
                 (b"Invalid", 404, ConnectionError,
                  ["HTTP code 404"],
                  "8 HTTP code 404",
                  "8", None
                  ),
                 ]

        for text, status_code, exp_exception, exp_data, exp_english,\
                exp_code, exp_response in tests:
            response = requests.Response()
            response._content = text
            response.status_code = status_code
            self.http_client.response = response

            if exp_exception:
                self.check_st_exception(exp_exception, exp_data, exp_english,
                                        exp_code, self.http_client._receive)
            else:
                actual = self.http_client._receive()
                self.assertEqual(actual, exp_response)

if __name__ == "__main__":
    unittest.main()
