#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
from securetrading.test import abstract_test
import securetrading
import securetrading.httpclient as st_httpclient
import json
import platform


class Test_Api(abstract_test.TestCase):

    def get_request(self, data={}):
        default = {"pan": "4111111111111111",
                   "expirydate": "12/2031",
                   "securitycode": "123",
                   "requesttypedescriptions": ["AUTH"],
                   "accounttypedescription": "ECOM",
                   "sitereference": "live2",
                   "paymenttypedescription": "VISA",
                   "currencyiso3a": "OMR",
                   "baseamount": "100",
                   }
        default.update(data)
        request = securetrading.Request()
        request.update(default)
        return request

    def get_config(self, data={}):
        config = securetrading.Config()
        for key in data:
            setattr(config, key, data[key])
        return config

    def test_process(self):
        sterror = securetrading.SecureTradingError
        apierror = securetrading.ApiError
        connecterror = securetrading.ConnectionError
        sendrecverror = securetrading.SendReceiveError

        versioninfo = "Python::{0}::1.0.8::{1}".format(
            platform.python_version(),
            platform.platform())
        request1 = self.get_securetrading_request({})
        request4 = self.get_securetrading_request({})
        default_config = self.get_config()
        config1 = self.get_config({"username": "test",
                                   "jsonversion": "2.00",
                                   "datacenterurl": "https://test.com",
                                   })

        french_config = self.get_config({"locale": "fr_fr",
                                         })

        german_config = self.get_config({"locale": "de_de",
                                         })

        request2 = self.get_securetrading_request(
            {"datacenterurl": "https://somewhere.com"})

        request1_str = '{{"requestreference":"{0}",\
"version":"1.00", "response":[{{"errorcode" : "0"}}]}}'
        request1_str2 = '{{"requestreference":"{0}",\
"version":"1.00", "response":[]}}'
        request1_dict = {"requestreference": request1["requestreference"],
                         "versioninfo": versioninfo}

        request2_str = '{{"requestreference": "{0}",\
"version": "1.00", "response": [{{"errorcode" : "0"}}]}}'

        lib_version = "python_1.0.8"
        msg = "{0} Maximum time reached whilst trying to connect to {1}\
".format(request2["requestreference"], request2["datacenterurl"])
        connection_error = connecterror("7", data=[msg])

        python_version = self.get_python_version()
        jsonMessage = ['No JSON object could be decoded']

        request3 = self.get_securetrading_request(
            {"requestreference": "requestreference"})

        request4_dict = {"requestreference": request4["requestreference"],
                         "versioninfo": versioninfo}

        request4_str = '{{"requestreference": "{0}",\
"version": "1.00", "response": [{{"errormessage": "GATEWAYERRMSG",\
"errorcode" : "99"}}]}}'

        if python_version >= 3:
            jsonMessage = ["Expecting value: line 1 column 21 (char 20)"]
        test_cases = [(request1, default_config,
                       request1_str.format(request1["requestreference"]),
                       None,
                       "https://webservices.securetrading.net/json/",
                       {"alias": "",
                        "libraryversion": lib_version,
                        "request": [request1_dict],
                        "version": "1.00"},
                       None, None,
                       {"requestreference": request1["requestreference"],
                        "version": "1.00",
                        "responses": [{"errormessage": "Ok",
                                       "errorcode": "0"
                                       }]}),
                      # config with new values instead of defaults
                      (request1, config1,
                       request1_str.format(request1["requestreference"]),
                       None, "https://test.com/json/",
                       {"alias": "test",
                        "libraryversion": lib_version,
                        "request": [request1_dict],
                        "version": "2.00"},
                       None, None,
                       {"requestreference": request1["requestreference"],
                        "version": "1.00",
                        "responses": [{"errormessage": "Ok",
                                       "errorcode": "0"},
                                      ]}),
                      # config with new values instead of defaults
                      (request1, config1,
                       request1_str2.format(request1["requestreference"]),
                       None, "https://test.com/json/",
                       {"alias": "test",
                        "libraryversion": lib_version,
                        "request": [request1_dict],
                        "version": "2.00"},
                       None, None,
                       {"requestreference": request1["requestreference"],
                        'version': '1.00',
                        "responses": []}),
                      # Invalid response example
                      (request2, config1,
                       request2_str.format(request2["requestreference"]),
                       None, "https://somewhere.com/json/",
                       {"alias": "test",
                        "libraryversion": lib_version,
                        "request": [{"requestreference":
                                     request2["requestreference"],
                                     "datacenterurl": "https://somewhere.com",
                                     "versioninfo": versioninfo,
                                     }],
                        "version": "2.00"},
                       None, None,
                       {'requestreference': request2["requestreference"],
                        'version': '1.00',
                        'responses': [{"errormessage": "Ok",
                                       "errorcode": "0"}]}),
                      # config with new values and request overrides
                      # datacenterurl
                      ([], default_config, None, None, None, None, None,
                       None,
                       {'requestreference': '',
                        'responses': [{'errorcode': '10',
                                       'errordata':
                                           ['Incorrect type of \
request specified'],
                                       'requesttypedescription': 'ERROR',
                                       'requestreference': '',
                                       'errormessage':
                                           'Incorrect usage of the \
Secure Trading API'},
                                      ]}
                       ),

                      ([], french_config, None, None, None, None, None,
                       None,
                       {'requestreference': '',
                        'responses': [{'errorcode': '10',
                                       'errordata':
                                           ['Incorrect type of \
request specified'],
                                       'requesttypedescription': 'ERROR',
                                       'requestreference': '',
                                       'errormessage':
                                           "Utilisation incorrecte de \
l'API Secure Trading"},
                                      ]}
                       ),  # French version of the config
                      ([], german_config, None, None, None, None, None,
                       None,
                       {'requestreference': '',
                        'responses': [{'errorcode': '10',
                                       'errordata':
                                           ['Incorrect type of \
request specified'],
                                       'requesttypedescription': 'ERROR',
                                       'requestreference': '',
                                       'errormessage':
                                           'Fehlerhafte Verwendung der Secure \
Trading API'},
                                      ]}
                       ),  # German version of the config

                      (request2, default_config, None, connecterror("7"), None,
                       None, None, None,
                       {"requestreference": request2["requestreference"],
                        "responses":
                            [{"requesttypedescription": "ERROR",
                              "requestreference": request2["requestreference"],
                              "errorcode": "7",
                              "errormessage": "An issue occured whilst trying to \
connect to Secure Trading servers",
                              "errordata": []},
                             ]}),
                      (request2, default_config, None,
                       sendrecverror("4", connection_error), None, None, None,
                       None,
                       {"requestreference": request2["requestreference"],
                        "responses":
                            [{"requesttypedescription": "ERROR",
                              "requestreference": request2["requestreference"],
                              'errorcode': "4",
                              'errormessage': 'Send error',
                              "errordata": ['7 {0} Maximum time reached whilst trying to \
connect to https://somewhere.com'.format(request2["requestreference"])]
                              }]
                        }
                       ),
                      (request1,
                       default_config,
                       '{"requestreference": \
"NEWREFERENCE-866-98", "version": "1.00", "response": [{"errorcode" : "0" }]}',
                       None,
                       "https://webservices.securetrading.net/json/",
                       {"alias": "",
                        "libraryversion": lib_version,
                        "request":
                        [{"requestreference": request1["requestreference"],
                          "versioninfo":versioninfo}],
                        "version": "1.00"},
                       None, None,
                       {"requestreference": request1["requestreference"],
                        "responses":
                            [{"requesttypedescription": "ERROR",
                              "requestreference": request1["requestreference"],
                              'errorcode': "9",
                              'errormessage': 'Unknown error. If this persists\
 please contact Secure Trading',
                              'errordata':
                                  ['Different request reference: sent ({0}) received\
 (NEWREFERENCE-866-98)'.format(request1["requestreference"])]}]}),
                      (request1,
                       default_config,
                       '{"requestreference":: \
"NEWREFERENCE-866-98", "version": "1.00", "response": []}',
                       None,
                       "https://webservices.securetrading.net/json/",
                       {"alias": "",
                        "libraryversion": lib_version,
                        "request":
                        [{"requestreference": request1["requestreference"],
                          "versioninfo":versioninfo}],
                        "version": "1.00"},
                       None, None,
                       {"requestreference": request1["requestreference"],
                        "responses":
                            [{"requesttypedescription": "ERROR",
                              "requestreference": request1["requestreference"],
                              'errorcode': "5",
                              'errormessage': 'Receive error',
                              'errordata': jsonMessage,
                              }
                             ]
                        }
                       ),
                      ({"requestreference": "myref"}, default_config,
                       request1_str.format("myref"),
                       None,
                       "https://webservices.securetrading.net/json/",
                       {"alias": "",
                        "libraryversion": lib_version,
                        "request": [{"requestreference": "myref",
                                     "versioninfo": versioninfo,
                                     }],
                        "version": "1.00"},
                       None, None,
                       {"requestreference": "myref",
                        "version": "1.00",
                        "responses": [{"errormessage": "Ok",
                                       "errorcode": "0"
                                       }]}),
                      (request4, default_config,
                       request4_str.format(request4["requestreference"]),
                       None,
                       "https://webservices.securetrading.net/json/",
                       {"alias": "",
                        "libraryversion": lib_version,
                        "request": [request4_dict],
                        "version": "1.00"},
                       None, None,
                       {"requestreference": request4["requestreference"],
                        "version": "1.00",
                        "responses": [{"errormessage": "GATEWAYERRMSG",
                                       "errorcode": "99"
                                       }]}),
                      ]

        http_main = st_httpclient.GenericHTTPClient._main
        try:
            for (request, config, http_result, http_raises,
                 http_url, http_json_dict, exp_raises, exp_message,
                 exp_result) in test_cases:
                st_httpclient.GenericHTTPClient._main = self.mock_method(
                    result=http_result,
                    exception=http_raises)
                api = securetrading.Api(config=config)
                if exp_raises is None:
                    actual = api.process(request)
                    if http_result is not None:
                        sent_to_mock = self.mock_receive
                        actual_url = sent_to_mock[0][0][1]
                        actual_json_dict = json.loads(sent_to_mock[0][0][2])
                        self.assertEqual(actual_url, http_url)
                        self.assertEqual(actual_json_dict, http_json_dict)
                    self.assertEqual(actual, exp_result)
                else:
                    self.assertRaisesRegexp(
                        exp_raises, exp_message, api.process,
                        request)
        finally:
            securetrading.httpclient.GenericHTTPClient._main = http_main

    def test__verify_request(self):
        request = securetrading.Request()
        tests = [({}, securetrading.SecureTradingError,
                  ["Incorrect type of request specified"],
                  "10 Incorrect type of request specified", "10"),
                 (request, None, None, None, None),
                 ]
        config = self.get_config()
        api = securetrading.Api(config)

        for request, exp_exception, exp_data, exp_eng, exp_code in tests:
            if exp_exception is None:
                api._verify_request(request)
            else:
                self.check_st_exception(exp_exception, exp_data, exp_eng,
                                        exp_code, api._verify_request,
                                        func_args=(request,))

    def test__verifyResult(self):
        tests = [({"requestreference": "Ahc6uwqq6"}, "Ahc6uwqq6", None, None,
                  None, None),
                 ({}, "Ahc6uwqq6", securetrading.SecureTradingError,
                  ['Different request reference: sent \
\(Ahc6uwqq6\) received \(None\)'],
                  "9 Different request reference: sent (Ahc6uwqq6) received \
(None)",
                  "9"),
                 ({"requestreference": "Arckthaau"}, "Ahc6uwqq6",
                  securetrading.SecureTradingError,
                  ['Different request reference: sent \(Ahc6uwqq6\) received\
 \(Arckthaau\)'],
                  "9 Different request reference: sent (Ahc6uwqq6) \
received (Arckthaau)",
                  "9"),
                 ]
        config = self.get_config()
        api = securetrading.Api(config)

        for result, ref, exp_exception, exp_data, exp_eng, exp_code in tests:
            verify_args = (result, ref)
            if exp_exception is None:
                api._verify_result(*verify_args)
            else:
                self.check_st_exception(exp_exception, exp_data, exp_eng,
                                        exp_code, api._verify_result,
                                        func_args=verify_args)

    def test__generateStError(self):
        sterror = securetrading.SecureTradingError
        apierror = securetrading.ApiError
        connecterror = securetrading.ConnectionError
        sendrecverror = securetrading.SendReceiveError

        tests = [({}, sterror("9", data=["Different request reference"]),
                  "Ahc6uwqq6",
                  {"requestreference": "Ahc6uwqq6",
                   "responses": [{"requestreference": "Ahc6uwqq6",
                                  "errorcode": "9",
                                  "errordata":
                                      ["Different request reference"],
                                  "requesttypedescription": "ERROR"}]}),
                 ({}, sterror("9", data=["Different Issue"]),
                  "Arckthaau",
                  {"requestreference": "Arckthaau",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Arckthaau",
                                  "errorcode": "9",
                                  "errordata": ["Different Issue"]}]}),
                 ({}, sterror("1", data=["Generic Issue"]),
                  "Armm51h6v",
                  {"requestreference": "Armm51h6v",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Armm51h6v",
                                  "errorcode": "1",
                                  "errordata": ["Generic Issue"]}]}),
                 ({}, sterror("2", data=["An Issue"]),
                  "Ahc6uwqq6",
                  {"requestreference": "Ahc6uwqq6",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Ahc6uwqq6",
                                  "errorcode": "2",
                                  "errordata": ["An Issue"]}]}),
                 ({}, sendrecverror("4", data=["Send Issue"]),
                  "Arckthaau",
                  {"requestreference": "Arckthaau",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Arckthaau",
                                  "errorcode": "4",
                                  "errordata": ["Send Issue"]}]}),
                 ({}, sendrecverror("5", data=["Receive Issue"]),
                  "Armm51h6v",
                  {"requestreference": "Armm51h6v",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Armm51h6v",
                                  "errorcode": "5",
                                  "errordata": ["Receive Issue"]}]}),

                 ({}, connecterror("7", data=["Connection Issue"]),
                  "Arckthaau",
                  {"requestreference": "Arckthaau",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Arckthaau",
                                  "errorcode": "7",
                                  "errordata": ["Connection Issue"]}]}),
                 ({}, connecterror("8", data=["Unexpected Connection Issue"]),
                  "Armm51h6v",
                  {"requestreference": "Armm51h6v",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Armm51h6v",
                                  "errorcode": "8",
                                  "errordata":
                                      ["Unexpected Connection Issue"]}]}),
                 ({"locale": "fr_fr"}, apierror("10", data=["Api Issue"]),
                  "Ahc6uwqq6",
                  {u'requestreference': u'Ahc6uwqq6',
                   u'responses': [{'errorcode': u'10',
                                   'requesttypedescription': u'ERROR',
                                   'requestreference': u'Ahc6uwqq6',
                                   'errordata': [u'Api Issue'],
                                   }
                                  ]}),
                 ]

        for configData, exception, request_reference, exp_update in tests:
            config = self.get_config(data=configData)
            api = securetrading.Api(config)

            actual = api._generate_st_error(exception, request_reference)
            exp_response = securetrading.Response()
            exp_response.update(exp_update)

            self.assertEqual(actual, exp_response)

    def test__generateError(self):
        tests = [(KeyError("A Key Error Occured"),
                  "Ahc6uwqq6",
                  {"requestreference": "Ahc6uwqq6",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Ahc6uwqq6",
                                  "errorcode": "9",
                                  "errordata": ["A Key Error Occured"]}]}),
                 (AssertionError("An Assertion Error Occured"),
                  "Arckthaau",
                  {"requestreference": "Arckthaau",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Arckthaau",
                                  "errorcode": "9",
                                  "errordata":
                                      ["An Assertion Error Occured"]}]}),
                 (ValueError("A Value Error Occured"),
                  "Armm51h6v",
                  {"requestreference": "Armm51h6v",
                   "responses": [{"requesttypedescription": "ERROR",
                                  "requestreference": "Armm51h6v",
                                  "errorcode": "9",
                                  "errordata":
                                      ["A Value Error Occured"]}]}),
                 ]

        for exception, request_reference, exp_update in tests:
            config = self.get_config()
            api = securetrading.Api(config)

            actual = api._generate_error(exception, request_reference)

            exp_response = securetrading.Response()
            exp_response.update(exp_update)

            self.assertEqual(actual, exp_response)

if __name__ == "__main__":
    unittest.main()
