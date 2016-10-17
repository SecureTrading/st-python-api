#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
from securetrading.test import abstract_test
import securetrading
import json
import copy


class Test_Converter(abstract_test.TestCase):

    def get_converter(self, config_data=None):
        if config_data is None:
            config_data = {"username": "test@testing.com",
                           "password": "testingpassword",
                           "jsonversion": "1.00",
                           }

        config = securetrading.Config()

        config.username = config_data["username"]
        config.password = config_data["password"]
        config.jsonversion = config_data["jsonversion"]
        converter = securetrading.Converter(config)
        return converter

    def test__encode(self):
        lib_version = "python_1.0.8"
        requestblock = {"alias": "test@testing.com",
                        "version": "1.00",
                        "libraryversion": lib_version,
                        "request": [],
                        }

        auth_data = {"pan": "4111111111111111",
                     "expirydate": "12/2031",
                     "securitycode": "123",
                     "requesttypedescription": "AUTH",
                     "accounttypedescription": "ECOM",
                     "sitereference": "siteref123",
                     "paymenttypedescription": "VISA",
                     "currencyiso3a": "GBP",
                     "baseamount": "100",
                     }

        different_config_data = {"username": "diff@different.com",
                                 "password": "differentpassword",
                                 "jsonversion": "2.20",
                                 }

        currencyrate_data = {"requesttypedescription": "CURRENCYRATE",
                             "sitereference": "siteref123",
                             "accounttypedescription": "CURRENCYRATE",
                             "dcccurrencyiso3a": "USD",
                             "pan": "4111111111111111",
                             "dcctype": "DCC",
                             "dccbaseamount": "100",
                             }

        currencyrate_exp = {"alias": "diff@different.com",
                            "version": "2.20",
                            "libraryversion": lib_version,
                            "request": [currencyrate_data],
                            }

        request_auth = self.get_securetrading_request(auth_data)
        requests_auth_only = self.get_securetrading_requests([request_auth])
        auth_exp = copy.deepcopy(requestblock)
        auth_exp["request"].append(auth_data)

        accountcheck_data = copy.deepcopy(auth_data)
        accountcheck_data.update({"requesttypedescription": "ACCOUNTCHECK"})

        request_accountcheck = self.get_securetrading_request(
            accountcheck_data)
        requests_accountcheck_auth_seperate = self.get_securetrading_requests(
            [request_accountcheck, request_auth])

        accountcheck_auth_exp = copy.deepcopy(auth_exp)
        accountcheck_auth_exp["request"].insert(
            0, accountcheck_data)

        accountcheck_auth_multi_data = copy.deepcopy(auth_data)
        del accountcheck_auth_multi_data["requesttypedescription"]
        accountcheck_auth_multi_data.update(
            {"requesttypedescriptions": ["ACCOUNTCHECK", "AUTH"]})

        request_accountcheck_auth = self.get_securetrading_request(
            accountcheck_auth_multi_data)
        requests_accountcheck_auth_multi = self.get_securetrading_requests(
            [request_accountcheck_auth])

        accountcheck_auth_multi_exp = copy.deepcopy(requestblock)
        accountcheck_auth_multi_exp["request"] =\
            [accountcheck_auth_multi_data]

        request_currencyrate = self.get_securetrading_request(
            currencyrate_data)

        json_bad_english = "10 Unknown type of object (<type 'dict'>), \
encoding failed"
        json_bad_data = ["Unknown type of object \(<(type|class) 'dict'>\), \
encoding failed"]
        python_version = self.get_python_version()
        if python_version >= 3:
            json_bad_english = "10 Unknown type of object (<class 'dict'>), \
encoding failed"

        tests = [(None, request_auth, auth_exp, None, None, None, None),
                 (None, requests_auth_only, auth_exp, None, None, None, None),
                 (None, requests_accountcheck_auth_seperate,
                  accountcheck_auth_exp, None, None, None, None),
                 (None, requests_accountcheck_auth_multi,
                  accountcheck_auth_multi_exp, None, None, None, None),
                 (None, {"requestreference": "INVALIDOBJECT"}, None,
                  securetrading.SecureTradingError,
                  json_bad_english,
                  json_bad_data,
                  "10"),
                 (different_config_data, request_currencyrate,
                  currencyrate_exp, None, None, None, None),
                 ]

        for config_data, request_object, expected, \
                exp_exception, exp_english, exp_data, exp_code in tests:

            securetrading_converter = self.get_converter(
                config_data=config_data)

            if exp_exception is None:
                actual = json.loads(
                    securetrading_converter._encode(request_object))

                for request in expected["request"]:
                    # versioninfo is added by the request object itself
                    request["versioninfo"] = securetrading.version_info

                for request in actual["request"]:
                    # requestreference is unique everytime
                    del request["requestreference"]

                self.assertEqual(actual, expected)
            else:
                self.check_st_exception(exp_exception, exp_data, exp_english,
                                        exp_code, securetrading_converter.
                                        _encode,
                                        func_args=(request_object,))

    def test__decode(self):
        auth_json = """{"requestreference": "Ahc6uwqq6",
                                      "version": "1.00",
"response": [{"transactionstartedtimestamp": "2016-02-25 11:27:37",
              "livestatus": "1",
              "settleduedate": "2016-02-25",
              "errorcode": "0",
              "tid": "27882200",
              "merchantnumber": "11223344",
              "merchantcountryiso2a": "GB",
              "transactionreference": "17-2-81001",
              "merchantname": "Live Unittest Site <>&!_-=+@#:;,./?OK",
              "paymenttypedescription": "VISA",
              "baseamount": "100",
              "accounttypedescription": "ECOM",
              "acquirerresponsecode": "00",
              "requesttypedescription": "AUTH",
              "securityresponsesecuritycode": "2",
              "currencyiso3a": "GBP",
              "authcode": "14",
              "errormessage": "Ok",
              "securityresponsepostcode": "0",
              "maskedpan": "411111######1111",
              "securityresponseaddress": "0",
              "issuercountryiso2a": "ZZ",
              "settlestatus": "0"
              }],
                                      "secrand": "kpEEso8"
                                      }"""

        auth_exp = {"requestreference": "Ahc6uwqq6",
                    "version": "1.00",
                    "responses": [{"transactionstartedtimestamp":
                                   "2016-02-25 11:27:37",
                                   "livestatus": "1",
                                   "settleduedate": "2016-02-25",
                                   "errorcode": "0",
                                   "tid": "27882200",
                                   "merchantnumber": "11223344",
                                   "merchantcountryiso2a": "GB",
                                   "transactionreference": "17-2-81001",
                                   "merchantname":
                                   "Live Unittest Site <>&!_-=+@#:;,./?OK",
                                   "paymenttypedescription": "VISA",
                                   "baseamount": "100",
                                   "accounttypedescription": "ECOM",
                                   "acquirerresponsecode": "00",
                                   "requesttypedescription": "AUTH",
                                   "securityresponsesecuritycode": "2",
                                   "currencyiso3a": "GBP",
                                   "authcode": "14",
                                   "errormessage": "Ok",
                                   "securityresponsepostcode": "0",
                                   "maskedpan": "411111######1111",
                                   "securityresponseaddress": "0",
                                   "issuercountryiso2a": "ZZ",
                                   "settlestatus": "0"}],
                    }

        exp_response_auth = self.get_securetrading_response(auth_exp)

        accountcheck_auth_json = """{"requestreference": "Arckthaau",
              "version": "1.00",
"response": [{"transactionstartedtimestamp": "2016-02-25 12:00:39",
              "retrievalreferencenumber": "605612170001",
              "stan": "170001",
              "merchantzipcode": "MN119K",
              "livestatus": "1",
              "merchantcategorycode": "7995",
              "dccenabled": "0",
              "settleduedate": "2016-02-25",
              "errorcode": "0",
              "merchantnumber": "14725834",
              "merchantcountryiso2a": "GB",
              "merchantcity": "Manchester#",
              "transactionreference": "17-70-1",
              "merchantname": "Live Unittest Site <>&!_-=+@#:;,./?OK",
              "paymenttypedescription": "VISA",
              "baseamount": "100",
              "accounttypedescription": "ECOM",
              "acquirerresponsecode": "83",
              "requesttypedescription": "ACCOUNTCHECK",
              "acquirerresponsemessage":
"Not declined - Valid for all zero amount transactions",
              "securityresponsesecuritycode": "2",
              "chargedescription": "Account_CD",
              "currencyiso3a": "OMR",
              "authcode": "000423",
              "errormessage": "Ok",
              "securityresponsepostcode": "0",
              "maskedpan": "411111######1111",
              "securityresponseaddress": "0",
              "issuercountryiso2a": "ZZ",
              "settlestatus": "0"
              },
              {"transactionstartedtimestamp": "2016-02-25 12:00:39",
              "retrievalreferencenumber": "605612170002",
              "parenttransactionreference": "17-70-1",
              "acquirerresponsecode": "00",
              "merchantzipcode": "MN119K",
              "livestatus": "1",
              "merchantcategorycode": "7995",
              "dccenabled": "0",
              "settleduedate": "2016-02-25",
              "errorcode": "0",
              "merchantnumber": "14725834",
              "merchantcountryiso2a": "GB",
              "merchantcity": "Manchester#",
              "transactionreference": "17-70-2",
              "merchantname": "Live Unittest Site <>&!_-=+@#:;,./?OK",
              "paymenttypedescription": "VISA",
              "baseamount": "100",
              "accounttypedescription": "ECOM",
              "stan": "170002",
              "requesttypedescription": "AUTH",
              "acquirerresponsemessage": "Approved or completed Successfully",
              "securityresponsesecuritycode": "2",
              "chargedescription": "Account_CD",
              "currencyiso3a": "OMR",
              "authcode": "000424",
              "errormessage": "Ok",
              "securityresponsepostcode": "0",
              "maskedpan": "411111######1111",
              "securityresponseaddress": "0",
              "issuercountryiso2a": "ZZ",
              "settlestatus": "0"
              }
                           ],
              "secrand": "0xto2lBEx"
              }"""

        accountcheck_auth_exp = {"requestreference": "Arckthaau",
                                 "version": "1.00",
                                 "responses":
                                     [{"transactionstartedtimestamp":
                                       "2016-02-25 12:00:39",
                                       "retrievalreferencenumber":
                                       "605612170001",
                                       "stan": "170001",
                                       "merchantzipcode": "MN119K",
                                       "livestatus": "1",
                                       "merchantcategorycode": "7995",
                                       "dccenabled": "0",
                                       "settleduedate": "2016-02-25",
                                       "errorcode": "0",
                                       "merchantnumber": "14725834",
                                       "merchantcountryiso2a": "GB",
                                       "merchantcity": "Manchester#",
                                       "transactionreference": "17-70-1",
                                       "merchantname":
                                       "Live Unittest Site <>&!_-=+@#:;,./?OK",
                                       "paymenttypedescription": "VISA",
                                       "baseamount": "100",
                                       "accounttypedescription": "ECOM",
                                       "acquirerresponsecode": "83",
                                       "requesttypedescription":
                                       "ACCOUNTCHECK",
                                       "acquirerresponsemessage":
                                       "Not declined - Valid for all zero amount \
transactions",
                                       "securityresponsesecuritycode": "2",
                                       "chargedescription": "Account_CD",
                                       "currencyiso3a": "OMR",
                                       "authcode": "000423",
                                       "errormessage": "Ok",
                                       "securityresponsepostcode": "0",
                                       "maskedpan": "411111######1111",
                                       "securityresponseaddress": "0",
                                       "issuercountryiso2a": "ZZ",
                                       "settlestatus": "0"
                                       },
                                      {"transactionstartedtimestamp":
                                       "2016-02-25 12:00:39",
                                       "retrievalreferencenumber":
                                       "605612170002",
                                       "parenttransactionreference": "17-70-1",
                                       "acquirerresponsecode": "00",
                                       "merchantzipcode": "MN119K",
                                       "livestatus": "1",
                                       "merchantcategorycode": "7995",
                                       "dccenabled": "0",
                                       "settleduedate": "2016-02-25",
                                       "errorcode": "0",
                                       "merchantnumber": "14725834",
                                       "merchantcountryiso2a": "GB",
                                       "merchantcity": "Manchester#",
                                       "transactionreference": "17-70-2",
                                       "merchantname":
                                       "Live Unittest Site <>&!_-=+@#:;,./?OK",
                                       "paymenttypedescription": "VISA",
                                       "baseamount": "100",
                                       "accounttypedescription": "ECOM",
                                       "stan": "170002",
                                       "requesttypedescription": "AUTH",
                                       "acquirerresponsemessage":
                                       "Approved or completed Successfully",
                                       "securityresponsesecuritycode": "2",
                                       "chargedescription": "Account_CD",
                                       "currencyiso3a": "OMR",
                                       "authcode": "000424",
                                       "errormessage": "Ok",
                                       "securityresponsepostcode": "0",
                                       "maskedpan": "411111######1111",
                                       "securityresponseaddress": "0",
                                       "issuercountryiso2a": "ZZ",
                                       "settlestatus": "0"
                                       }
                                      ],
                                 }

        exp_response_accountcheck_auth =\
            self.get_securetrading_response(accountcheck_auth_exp)

        bad_requesttype_json =\
            """{"requestreference": "Armm51h6v",
"version": "1.00",
"response": [{"errorcode": "60018",
"requesttypedescription": "ERROR",
"transactionstartedtimestamp": "2016-02-25 14:06:09",
"errormessage": "Invalid requesttype",
"errordata": ["BADREQUEST"]
}
],
"secrand": "P35L"
}"""

        bad_requesttype_exp = {"requestreference": "Armm51h6v",
                               "version": "1.00",
                               "responses":
                                   [{"errorcode": "60018",
                                     "requesttypedescription": "ERROR",
                                     "transactionstartedtimestamp":
                                         "2016-02-25 14:06:09",
                                     "errormessage": "Invalid requesttype",
                                     "errordata": ["BADREQUEST"],
                                     }
                                    ],
                               }

        exp_response_bad_requesttype =\
            self.get_securetrading_response(bad_requesttype_exp)

        python_version = self.get_python_version()
        json_bad_english = "5 No JSON object could be decoded"
        json_bad_data = ["(No JSON object could be decoded)|\
(Expecting value: line 1 column 1 \(char 0\))"]
        if python_version >= 3:
            json_bad_english = "5 Expecting value: line 1 column 1 (char 0)"

        tests = [(auth_json, exp_response_auth, None, None, None, None),
                 (accountcheck_auth_json,
                  exp_response_accountcheck_auth, None, None, None, None),
                 ("BADJSONSTRING", None, securetrading.SendReceiveError,
                  json_bad_english,
                  json_bad_data,
                  "5"),
                 (bad_requesttype_json, exp_response_bad_requesttype, None,
                  None, None, None),
                 ]

        for (json_str, expected, exp_exception, exp_english, exp_data,
             exp_code) in tests:
            request_reference = "PASSEDINFORLOGGINGONLY"
            securetrading_converter = self.get_converter()

            if exp_exception is None:
                actual = securetrading_converter._decode(
                    json_str, request_reference)
                self.assertEqual(actual, expected)
            else:
                self.check_st_exception(exp_exception, exp_data, exp_english,
                                        exp_code, securetrading_converter.
                                        _decode,
                                        func_args=(json_str,
                                                   request_reference))

if __name__ == "__main__":
    unittest.main()
