#!/usr/bin/env python
import unittest
import securetrading
from securetrading.test import abstract_test_stobjects


class Test_Response(abstract_test_stobjects.Abstract_Test_StObjects):

    def setUp(self):
        super(Test_Response, self).setUp()
        self.class_ = securetrading.Response


if __name__ == "__main__":
    unittest.main()
