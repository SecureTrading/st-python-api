#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
import securetrading
from securetrading.test import abstract_test
import time
import hashlib
import os
import argparse
import sys


def get_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--sitereference", action="store", required=True,
                             dest="sitereference",
                             help="Specify sitereference")
    args_parser.add_argument("--username", action="store", required=True,
                             dest="username",
                             help="Specify webservices username.")
    args_parser.add_argument("--password", action="store", required=True,
                             dest="password",
                             help="Specify webservices password.")
    args_parser.add_argument("--overridecacerts", action="store",
                             dest="overridecacerts", default=None,
                             help="Overrides built-in cacerts.")
    args_parser.add_argument("--transfersleeptime", action="store",
                             dest="transfersleeptime", default=300, type=int,
                             help="Sets the sleep time for parent transactions\
 to be fully processed in seconds. Default: %(default)d")

    (passed_args, unittest_args) = args_parser.parse_known_args()
    return passed_args, unittest_args


class Module_Test_Api(abstract_test.TestCase):

    PARENT_RESPONSES = None
    UNI = "T\r\xc2\xa3S'T(|]><[\\xG %s %% \"+N\
\\\\&\\M\xc8.?\nTAB\t12}34{56789,:;#END"

    def __init__(self, *args, **kwargs):
        super(Module_Test_Api, self).__init__(*args, **kwargs)
        self.sitereference = passed_args.sitereference
        # Please contact Secure Trading support to set up a test site
        # The following options are required.
        # A currency rate account for USD Visa
        # test account with the following:
        # GBP ECOM VISA
        # GBP MOTO VISA
        # dcc USD ECOM VISA
        # GBP ECOM PAYPAL
        # EUR ECOM SOFORT
        # USD ECOM ACH
        # Fraud Control
        # Identity Check
        # GBP CFT VISA
        # GBP RECUR VISA
        # The site also needs a webservices user set up via MySt.

        username = passed_args.username
        password = passed_args.password
        ssl_cert_file = passed_args.overridecacerts
        base_path = self.get_package_path()

        # st_api valid credentials
        st_config = securetrading.Config()
        st_config.username = username
        st_config.password = password
        st_config.ssl_certificate_file = ssl_cert_file

        # st_api2 is intentionally using bad credentials.
        st_config2 = securetrading.Config()
        st_config2.username = "UNKNOWN"
        st_config2.password = "PASS"
        st_config2.ssl_certificate_file = ssl_cert_file

        # st_api3 is intentionally using a corrupt cacerts file.
        st_config3 = securetrading.Config()
        st_config3.username = username
        st_config3.password = password
        st_config3.ssl_certificate_file = os.path.join(base_path,
                                                       "test/badcacert.pem")

        # st_api4 is intentionally using a cacerts file that is not our ca.
        st_config4 = securetrading.Config()
        st_config4.username = username
        st_config4.password = password
        st_config4.ssl_certificate_file = os.path.join(base_path,
                                                       "test/testcacert.pem")

        # st_api valid credentials fr setup
        st_config_fr = securetrading.Config()
        st_config_fr.username = username
        st_config_fr.password = password
        st_config_fr.ssl_certificate_file = ssl_cert_file
        st_config_fr.locale = "fr_fr"

        # st_api valid credentials de setup
        st_config_de = securetrading.Config()
        st_config_de.username = username
        st_config_de.password = password
        st_config_de.ssl_certificate_file = ssl_cert_file
        st_config_de.locale = "de_de"

        # initialise all the st_api objects with their respective config
        self.st_api = securetrading.Api(st_config)
        self.st_api2 = securetrading.Api(st_config2)
        self.st_api3 = securetrading.Api(st_config3)
        self.st_api4 = securetrading.Api(st_config4)
        self.st_api_fr = securetrading.Api(st_config_fr)
        self.st_api_de = securetrading.Api(st_config_de)

        if self.PARENT_RESPONSES is None:
            # Singleton so that it doenst get set always
            Module_Test_Api.PARENT_RESPONSES = self.set_up_parents()
            # Sleeping to allow parent transactions to be fully processed
            transfersleeptime = passed_args.transfersleeptime
            print("Sleeping for {0:d} seconds to allow parent transactions to be\
 fully processed".format(transfersleeptime))
            time.sleep(transfersleeptime)

    def set_up_parents(self):
        parent_responses = {}

        parents_required = [("order",
                             "ORDER",
                             {}),
                            ("pending_auth",
                             "AUTH",
                             {"pan": "4111111111111111",
                              "expirymonth": "11",
                              "expiryyear": "2031",
                              "securitycode": "123",
                              "paymenttypedescription": "VISA"
                              }),
                            ("settled_auth",
                             "AUTH",
                             {"settlestatus": "100",
                              "paymenttypedescription": "PAYPAL"}),
                            ("cachetoken",
                             "CACHETOKENISE",
                             {"pan": "4111111111111111",
                              "expirymonth": "11",
                              "expiryyear": "2031",
                              "securitycode": "123",
                              "paymenttypedescription": "VISA"
                              }),
                            ]

        for parent_key, requesttypdescription, updates in parents_required:
            if parent_key == "settled_auth":
                p_ref = parent_responses["order"]["transactionreference"]
                updates["parenttransactionreference"] = p_ref
                paypaltoken = parent_responses["order"]["paypaltoken"]
                updates["paypaltoken"] = paypaltoken
                payerid = self.get_paypalpayerid(paypaltoken)
                updates["paypalpayerid"] = payerid

            data = self.get_request_values(requesttypdescription,
                                           updates)
            single_data = self.process_single(data)["responses"][0]
            parent_responses[parent_key] = single_data

        return parent_responses

    def get_paypalpayerid(self, token):
        return hashlib.md5(token.encode("ascii")).hexdigest()[:10]+"pid"

    def _process_request(self, request_obj):
        return self.st_api.process(request_obj)

    def _get_st_request(self, data):
        st_request = securetrading.Request()
        st_request.update(data)
        return st_request

    def process_single(self, request_dict):
        st_request = self._get_st_request(request_dict)
        return self._process_request(st_request)

    def process_multiple(self, requests):
        st_requests = securetrading.Requests()
        st_requests["requests"] = []
        for request in requests:
            st_request = self._get_st_request(request)
            st_requests["requests"].append(st_request)

        return self._process_request(st_requests)

    def get_request_values(self, requesttypedescription, extra_updates={}):
        base_values = {"sitereference": self.sitereference,
                       }

        values = {"AUTH": {"accounttypedescription": "ECOM",
                           "currencyiso3a": "GBP",
                           "baseamount": "100",
                           "customerfirstname": self.UNI,
                           },
                  "STORE": {"accounttypedescription": "CARDSTORE",
                            },
                  "ORDER": {"accounttypedescription": "ECOM",
                            "paymenttypedescription": "PAYPAL",
                            "billingfirstname": self.UNI,
                            "customerfirstname": "Tester",
                            "customerlastname": "Jones",
                            "customerpremise": "1234",
                            "customertown": "Bangor",
                            "customercountryiso2a": "GB",
                            "paypalemail": "test@example.com",
                            "paypaladdressoverride": "1",
                            "returnurl": "www.example.com/return",
                            "cancelurl": "www.example.com/cancel",
                            "currencyiso3a": "GBP",
                            "baseamount": "100",
                            },
                  "ACCOUNTCHECK": {"accounttypedescription": "ECOM",
                                   "currencyiso3a": "GBP",
                                   "baseamount": "0",
                                   "customerfirstname": self.UNI,
                                   },
                  "THREEDQUERY": {"accounttypedescription": "ECOM",
                                  "currencyiso3a": "GBP",
                                  "termurl": "https://www.termurl.com",
                                  "baseamount": "100",
                                  "customerfirstname": self.UNI,
                                  },
                  "CURRENCYRATE": {"accounttypedescription": "ECOM",
                                   "dcccurrencyiso3a": "USD",
                                   "dccbaseamount": "100",
                                   "dcctype": "DCC",
                                   "customerfirstname": self.UNI,
                                   },
                  "RISKDEC": {"accounttypedescription": "FRAUDCONTROL",
                              "currencyiso3a": "GBP",
                              "baseamount": "100",
                              "customerfirstname": self.UNI,
                              },
                  "IDSTANDARD": {"accounttypedescription": "IDENTITYCHECK",
                                 "customercountryiso2a": "GB",
                                 "customerfirstname": "John",
                                 "customerlastname": "Doe",
                                 "customerpremise": "1",
                                 "customerpostcode": "AB12 3CD",
                                 },
                  "SUBSCRIPTION": {"subscriptionunit": "DAY",
                                   "subscriptiontype": "INSTALLMENT",
                                   "subscriptionfrequency": "1",
                                   "subscriptionfinalnumber": "1",
                                   "subscriptionnumber": "1",
                                   }
                  }
        base_values["requesttypedescriptions"] = [requesttypedescription]
        base_values.update(values.get(requesttypedescription, {}))
        base_values.update(extra_updates)
        base_values.update({"field_that_wont_be_passed": "HERE"})
        return base_values

    def validate(self, actuals, expecteds):
        python_version = self.get_python_version()

        if isinstance(expecteds, dict):
            for key in expecteds.keys():
                self.validate(actuals[key], expecteds[key])
        elif isinstance(expecteds, list):
            for actual, expected in zip(actuals, expecteds):
                self.validate(actual, expected)
        elif (python_version == 3 and isinstance(expecteds, str) or
              (python_version == 2 and isinstance(expecteds, basestring))):
            self.assertEqual(actuals, expecteds)

    def test_auth(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "acquirerresponsecode": "00",
                         }
        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_auth_decline_fr(self):
        extra_updates = {"pan": "4242424242424242",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }
        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_request = self._get_st_request(data)
        st_response = self.st_api_fr.process(st_request)

        exp_resp_data = {"errorcode": "70000",
                         "errormessage": "Refuser",
                         "authcode": "DECLINED",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_auth_decline_de(self):
        extra_updates = {"pan": "4242424242424242",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_request = self._get_st_request(data)
        st_response = self.st_api_de.process(st_request)

        exp_resp_data = {"errorcode": "70000",
                         "errormessage": "ablehnen",
                         "authcode": "DECLINED",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_auth_from_token(self):
        token = self.PARENT_RESPONSES["cachetoken"]["cachetoken"]
        extra_updates = {"cachetoken": token,
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "acquirerresponsecode": "00",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_auth_moto(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         "accounttypedescription": "MOTO",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "acquirerresponsecode": "00",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_invalid_encoding_latin1(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         "accounttypedescription": "MOTO",
                         "customerfirstname": u"\xa3".encode("latin1"),
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "10",
                         "errormessage": "Incorrect usage of the\
 Secure Trading API",
                         "errordata":
                         ["All types should be specified in unicode"],
                         "requesttypedescription": "ERROR",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_invalid_request_not_using_request_object(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.st_api.process(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "acquirerresponsecode": "00",
                         }
        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_invalid_request_using_invalid_request_object(self):
        data = []

        st_response = self.st_api.process(data)
        exp_resp_data = {"errorcode": "10",
                         "errormessage": "Incorrect usage of the\
 Secure Trading API",
                         "requesttypedescription": "ERROR",
                         }
        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_invalid_request_using_own_object(self):
        class myObj(dict):
            def verify(self):
                pass

        data = myObj()
        data.update({"requestreference": "REFERENCE"})
        st_response = self.st_api.process(data)
        exp_resp_data = {"errorcode": "10",
                         "errormessage": "Incorrect usage of the\
 Secure Trading API",
                         "requesttypedescription": "ERROR",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_invalid_request_no_data(self):
        data = {}

        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "60018",
                         "errormessage": "Invalid requesttype",
                         "errordata": ["None"],
                         "requesttypedescription": "ERROR",
                         }
        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_invalid_request_invalid_credentials(self):
        extra_updates = {"pan": "4000000000000812",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_request = self._get_st_request(data)
        st_response = self.st_api2.process(st_request)

        exp_resp_data = {"errorcode": "6",
                         "errormessage": "Invalid credentials provided",
                         "errordata": [],
                         "requesttypedescription": "ERROR",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

# This test generates an warning message to appear. It looks
# like is an issue with the underlying requests library
# https://github.com/kennethreitz/requests/issues/1882#ref-commit-5c20437
    def test_invalid_request_corrupt_cacerts_file(self):
        extra_updates = {"pan": "4000000000000812",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_request = self._get_st_request(data)
        st_response = self.st_api3.process(st_request)

        exp_resp_data = {"errorcode": "7",
                         "errormessage": "An issue occured whilst trying to\
 connect to Secure Trading servers",
                         "errordata": [],
                         "requesttypedescription": "ERROR",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_invalid_request_invalid_cacerts_file(self):
        extra_updates = {"pan": "4000000000000812",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_request = self._get_st_request(data)
        st_response = self.st_api4.process(st_request)

        exp_resp_data = {"errorcode": "7",
                         "errormessage": "An issue occured whilst\
 trying to connect to Secure Trading servers",
                         "errordata": [],
                         "requesttypedescription": "ERROR",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_auth_decline(self):
        extra_updates = {"pan": "4000000000000812",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "70000",
                         "errormessage": "Decline",
                         "authcode": "DECLINED",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_auth_sofort(self):
        extra_updates = {"bankid": "987654321",
                         "bankname": "FORTIS",
                         "currencyiso3a": "EUR",
                         "paymenttypedescription": "SOFORT",
                         "billingcountryiso2a": "DE",
                         "billingfirstname": "FIRSTNAME",
                         "billinglastname": "last1",
                         "billingpostcode": "AB45 6CB",
                         "billingpremise": "789",
                         "billingstreet": "Street",
                         "billingtown": "Town",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "settlestatus": "10",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_auth_ach(self):
        extra_updates = {"achaba": "987654321",
                         "achaccountnumber": "123456781",
                         "achchecknumber": "123456",
                         "achtype": "SAVINGS",
                         "paymenttypedescription": "ACH",
                         "currencyiso3a": "USD",
                         "billingcountryiso2a": "DE",
                         "billingfirstname": "FIRSTNAME",
                         "billinglastname": "last1",
                         "billingpostcode": "AB45 6CB",
                         "billingpremise": "789",
                         "billingstreet": "Street",
                         "billingtown": "Town",
                         }

        data = self.get_request_values("AUTH", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "acquirerresponsecode": "A01",
                         "acquirerresponsemessage": "APPROVED",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_refund(self):
        p_ref = self.PARENT_RESPONSES["settled_auth"]["transactionreference"]
        extra_updates = {"parenttransactionreference": p_ref,
                         }

        data = self.get_request_values("REFUND", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_refund_cft(self):
        extra_updates = {"accounttypedescription": "CFT",
                         "pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "baseamount": "500",
                         "currencyiso3a": "GBP",
                         }

        data = self.get_request_values("REFUND", extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "authcode": "TEST REFUND ACCEPTED",
                         "acquirerresponsecode": "00",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_store(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("STORE", extra_updates=extra_updates)
        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_cachetokenise(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("CACHETOKENISE",
                                       extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_order(self):
        data = self.get_request_values("ORDER")

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_orderdetails(self):
        p_ref = self.PARENT_RESPONSES["order"]["transactionreference"]
        extra_updates = {"parenttransactionreference": p_ref,
                         }

        data = self.get_request_values("ORDERDETAILS",
                                       extra_updates=extra_updates)

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "paypaladdressstatus": "Confirmed",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_accountcheck(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("ACCOUNTCHECK",
                                       extra_updates=extra_updates)
        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_threedquery(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("THREEDQUERY",
                                       extra_updates=extra_updates)
        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_multi_threedquery_auth_enrolled(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         "requesttypedescriptions": ["THREEDQUERY", "AUTH"],
                         }

        data = self.get_request_values("THREEDQUERY",
                                       extra_updates=extra_updates)
        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]

        self.validate(st_response["responses"], exp_raw_resp)

    def test_multi_threedquery_auth_notenrolled(self):
        extra_updates = {"pan": "4000000000000721",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         "requesttypedescriptions": ["THREEDQUERY", "AUTH"],
                         }

        data = self.get_request_values("THREEDQUERY",
                                       extra_updates=extra_updates)
        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "acquirerresponsecode": "00",
                         }

        exp_raw_resp = [{"errorcode": "0",
                         "errormessage": "Ok",
                         },
                        exp_resp_data,
                        ]

        self.validate(st_response["responses"], exp_raw_resp)

    def test_currencyrate(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         }

        data = self.get_request_values("CURRENCYRATE",
                                       extra_updates=extra_updates)
        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_riskdec(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         }

        data = self.get_request_values("RISKDEC", extra_updates=extra_updates)
        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_identitycheck(self):
        data = self.get_request_values("IDSTANDARD")

        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_transactionquery(self):
        p_ref = self.PARENT_RESPONSES["pending_auth"]["transactionreference"]
        data = {"requesttypedescriptions": ["TRANSACTIONQUERY"],
                "filter": {"transactionreference": [{"value": p_ref}],
                           }
                }

        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "records": [{"requesttypedescription": "AUTH",
                                      "transactionreference": p_ref,
                                      "interface": "PASS-JSON-JSON",
                                      "acquirerresponsecode": "00",
                                      }]
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_transactionupdate(self):
        p_ref = self.PARENT_RESPONSES["pending_auth"]["transactionreference"]
        data = {"requesttypedescriptions": ["TRANSACTIONUPDATE"],
                "filter": {"transactionreference": [{"value": p_ref}],
                           },
                "updates": {"settlebaseamount": "50",
                            },
                }

        st_response = self.process_single(data)
        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         }

        exp_raw_resp = [exp_resp_data]
        self.validate(st_response["responses"], exp_raw_resp)

    def test_multi_accountcheck_subscription(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         "baseamount": "100",
                         "requesttypedescriptions": ["ACCOUNTCHECK",
                                                     "SUBSCRIPTION"]
                         }

        data = self.get_request_values("ACCOUNTCHECK",
                                       extra_updates=extra_updates)
        data = self.get_request_values("SUBSCRIPTION",
                                       extra_updates=data)

        st_response = self.process_single(data)

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "requesttypedescription": "ACCOUNTCHECK"
                         }

        exp_raw_resp = [exp_resp_data,
                        {"errorcode": "0",
                         "errormessage": "Ok",
                         "requesttypedescription": "SUBSCRIPTION"
                         }]

        self.validate(st_response["responses"], exp_raw_resp)

    def test_seperate_accountcheck_subscription(self):
        extra_updates = {"pan": "4111111111111111",
                         "expirymonth": "11",
                         "expiryyear": "2031",
                         "securitycode": "123",
                         "paymenttypedescription": "VISA",
                         "baseamount": "100",
                         }

        ac_data = self.get_request_values("ACCOUNTCHECK",
                                          extra_updates=extra_updates)

        ac_data["requesttypedescription"] = ac_data.pop(
            "requesttypedescriptions")[0]

        sub_data = self.get_request_values("SUBSCRIPTION")
        sub_data["requesttypedescription"] = sub_data.pop(
            "requesttypedescriptions")[0]

        st_response = self.process_multiple([ac_data, sub_data])

        exp_resp_data = {"errorcode": "0",
                         "errormessage": "Ok",
                         "requesttypedescription": "ACCOUNTCHECK"
                         }

        exp_raw_resp = [exp_resp_data,
                        {"errorcode": "0",
                         "errormessage": "Ok",
                         "requesttypedescription": "SUBSCRIPTION"
                         }]

        self.validate(st_response["responses"], exp_raw_resp)


if __name__ == "__main__":
    script_name = sys.argv[0]
    passed_args, unittest_args = get_args()
    unittest.main(argv=[script_name] + unittest_args)
