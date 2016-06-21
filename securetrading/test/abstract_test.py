from __future__ import unicode_literals
import unittest
import securetrading
import platform
import pkgutil
import securetrading.util as util
import os


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self.uni = u"T\r\xc2\xa3S'T(|]><[\\xG %s %% \"+N\\\\&\\M\xc8.?\nTAB\t12}3\
4{56789,:;#END"
        self.utf8_uni = self.uni.encode("utf-8")
        self.byt_uni = self.uni.encode("latin-1")
        self.mock_receive = []

    def get_package_path(self):
        loader = pkgutil.get_loader('securetrading')
        if util._is_python_2():
            package_path = loader.filename
        else:
            package_path = os.path.split(loader.path)[0]
        return package_path

    def get_python_version(self):
        python_version = platform.python_version()
        python_version = int(python_version.split(".")[0])
        return python_version

    def mock_method(self, result=None, exception=None, multiple_calls=None):
        self.mock_receive = []

        def f(*args, **kwargs):
            self.mock_receive.append((args, kwargs))
            return result

        def f2(*args, **kwargs):
            self.mock_receive.append((args, kwargs))
            raise exception

        def f3(*args, **kwargs):
            self.mock_receive.append((args, kwargs))
            assert len(self.multi_call), "Not enough arguments provided"
            call = self.multi_call[0]
            self.multi_call = self.multi_call[1:]
            try:
                if isinstance(call, Exception) or isinstance(call(),
                                                             Exception):
                    raise call
            except TypeError:
                pass
            return call

        func = f
        if exception is not None:
            func = f2
        elif multiple_calls is not None:
            self.multi_call = multiple_calls
            func = f3
        return func

    def get_securetrading_request(self, request_dict):
        securetrading_request = securetrading.Request()
        securetrading_request.update(request_dict)
        return securetrading_request

    def get_securetrading_requests(self, request_list):
        securetrading_requests = securetrading.Requests()
        securetrading_requests["requests"] = request_list
        return securetrading_requests

    def get_securetrading_response(self, response_dict):
        securetrading_response = securetrading.Response()
        securetrading_response.update(response_dict)
        return securetrading_response

    def check_st_exception(self, exp_exception, exp_data, exp_english,
                           exp_code, function, func_args=(), func_kwargs={}):

        with self.assertRaises(exp_exception) as cm:
            function(*func_args, **func_kwargs)

        act_exception = cm.exception
        self.check_error(act_exception, exp_data, exp_code, exp_english)

    def check_error(self, error_obj, expected_data, expected_code,
                    expected_english):
        self.assertEqual(error_obj.__str__(), expected_english)
        if isinstance(error_obj, securetrading.SecureTradingError):
            self.assertEqual(len(error_obj.data), len(expected_data))
            for act, exp in zip(error_obj.data, expected_data):
                if exp == "":
                    # assertRegex on Python3 doesnt let you specifiy
                    # a blank string as the expected
                    self.assertEqual(act, exp)
                else:
                    self.assertRegexpMatches(act, exp)
            self.assertEqual(error_obj._english, expected_english)
            self.assertEqual(error_obj.code, expected_code)
