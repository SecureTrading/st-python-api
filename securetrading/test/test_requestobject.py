#!/usr/bin/env python
import unittest
import securetrading
from securetrading.test import abstract_test_stobjects
import six


class Test_Request(abstract_test_stobjects.Abstract_Test_StObjects):

    def setUp(self):
        super(Test_Request, self).setUp()
        self.class_ = securetrading.Request

    def test___init__(self):
        request = self.class_()
        six.assertRegex(self, request["requestreference"], "A[a-z0-9]+")
        self.assertEqual(securetrading.version_info, self.version_info)

    def test__set_cachetoken(self):
        exp1 = self.get_securetrading_request(
            {"datacenterurl": "https://webservices.securetrading.net",
             "datacenterpath": "/json/",
             "cachetoken":
                 "17-ae7e511172a07c2fb45db4c73388087e4d850777386a5d72029aaf895\
87f3cf0"})
        exp2 = self.get_securetrading_request(
            {"datacenterurl": "https://webservices.securetrading.net",
             "cachetoken": "17-6a0287dd04497ba8dab257acbd983741f55410b5c709463\
7d8c3f0fb57bd25ec"})
        exp3 = self.get_securetrading_request(
            {"cachetoken": "17-6a0287dd04497ba8dab257acbd983741f55410b5c709463\
7d8c3f0fb57bd25ec"})
        # Test below treats invalid base64 string as cachetoken
        exp4 = self.get_securetrading_request(
            {"cachetoken": "eyJkYXRhY2VudGVydXJsIjogImh0dHBzOi8vd2Vic2VydmljZX\
Muc2VjdXJldHJhZGluZy5uZXQiLCAiY2FjaGV0b2tlbiI6ICIxNy1hZTdlNTExMTcy"})

        tests = [('eyJkYXRhY2VudGVycGF0aCI6ICIvanNvbi8iLCAiZGF0YWNlbnRlcnVybCI\
6ICJodHRwczovL3dlYnNlcnZpY2VzLnNlY3VyZXRyYWRpbmcubmV0IiwgImNhY2hldG9rZW4iOiAiM\
TctYWU3ZTUxMTE3MmEwN2MyZmI0NWRiNGM3MzM4ODA4N2U0ZDg1MDc3NzM4NmE1ZDcyMDI5YWFmODk\
1ODdmM2NmMCJ9', exp1),
                 ('"eyJkYXRhY2VudGVydXJsIjogImh0dHBzOi8vd2Vic2VydmljZXMuc2VjdX\
JldHJhZGluZy5uZXQiLCAiY2FjaGV0b2tlbiI6ICIxNy02YTAyODdkZDA0NDk3YmE4ZGFiMjU3YWNi\
ZDk4Mzc0MWY1NTQxMGI1YzcwOTQ2MzdkOGMzZjBmYjU3YmQyNWVjIn0=', exp2),
                 ('17-6a0287dd04497ba8dab257acbd983741f55410b5c7094637d8c3f0fb\
57bd25ec', exp3),
                 ('eyJkYXRhY2VudGVydXJsIjogImh0dHBzOi8vd2Vic2VydmljZXMuc2VjdXJ\
ldHJhZGluZy5uZXQiLCAiY2FjaGV0b2tlbiI6ICIxNy1hZTdlNTExMTcy', exp4),
                 ]

        for cachetoken, expected in tests:
            request = self.class_()
            request._set_cachetoken(cachetoken)
            for obj in [expected, request]:
                del obj["requestreference"]  # Unique for every request object
            self.assertEqual(request, expected)


class Test_Requests(Test_Request):

    def setUp(self):
        super(Test_Requests, self).setUp()
        self.class_ = securetrading.Requests

    def test_verify(self):
        get_requests = self.get_securetrading_requests
        get_request = self.get_securetrading_request
        requests1 = get_requests([])

        requests2 = get_requests(
            [get_request({"a": "b"})])

        requests3 = get_requests(
            [get_request({"a": "b"}),
             get_request({"c": "d"})])
        datacenter_url_dict = {"datacenterurl": "url"}
        requests4 = get_requests(
            [get_request({"a": "b"}),
             get_request(datacenter_url_dict)])
        datacenter_path_dict = {"datacenterpath": "path"}
        requests5 = get_requests(
            [get_request({"a": "b"}),
             get_request(datacenter_path_dict)])

        tests = [(requests1, None, None, None, None),
                 (requests2, None, None, None, None),
                 (requests3, None, None, None, None),
                 (requests4, securetrading.ApiError,
                  "10", "10 The key 'datacenterurl' must be specifed \
in the outer 'securetrading.Requests' object",
                  ["The key 'datacenterurl' must be specifed in the \
outer 'securetrading.Requests' object"]),
                 (requests5, securetrading.ApiError,
                  "10", "10 The key 'datacenterpath' must be specifed \
in the outer 'securetrading.Requests' object",
                  ["The key 'datacenterpath' must be specifed in the \
outer 'securetrading.Requests' object"]),
                 ]

        for requests, exp_exception, exp_code, exp_english, exp_data in tests:
            if exp_exception is None:
                requests.verify()
            else:
                self.check_st_exception(exp_exception, exp_data, exp_english,
                                        exp_code, requests.verify)

    def test__validate_requests(self):
        get_requests = self.get_securetrading_requests
        get_request = self.get_securetrading_request
        tests = [([], None, None),
                 ([get_request({"a": "b"})], None, None),
                 ([{"a": "b"}], AssertionError, "Invalid requests specified")
                 ]

        for requests_list, exp_exception, exp_message in tests:
            if exp_exception is None:
                requests = get_requests(requests_list)
            else:
                six.assertRaisesRegex(self, exp_exception, exp_message,
                                      get_requests,
                                      requests_list)


if __name__ == "__main__":
    unittest.main()
