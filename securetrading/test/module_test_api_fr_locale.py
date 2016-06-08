#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
import sys
import module_test_api


class Module_Test_Api_Fr_Locale(module_test_api.Module_Test_Api):

    def __init__(self, *args, **kwargs):
        self.api_locale = "fr_fr"
        super(Module_Test_Api_Fr_Locale, self).__init__(*args, **kwargs)

    def test_auth(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_auth(error_msg=msg)

    def test_auth_from_token(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_auth_from_token(
            error_msg=msg)

    def test_auth_moto(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_auth_moto(error_msg=msg)

    def test_invalid_encoding_latin1(self):
        msg = "Une utilisation incorrecte de l'API Secure Trading"
        super(Module_Test_Api_Fr_Locale, self).test_invalid_encoding_latin1(
            error_msg=msg)

    def test_invalid_request_not_using_request_object(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale,
              self).test_invalid_request_not_using_request_object(
            error_msg=msg)

    def test_invalid_request_using_invalid_request_object(self):
        msg = "Une utilisation incorrecte de l'API Secure Trading"
        super(Module_Test_Api_Fr_Locale,
              self).test_invalid_request_using_invalid_request_object(
            error_msg=msg)

    def test_invalid_request_using_own_object(self):
        msg = "Une utilisation incorrecte de l'API Secure Trading"
        super(Module_Test_Api_Fr_Locale,
              self).test_invalid_request_using_own_object(error_msg=msg)

    def test_invalid_request_no_data(self):
        msg = "Type de demande non valide"
        super(Module_Test_Api_Fr_Locale,
              self).test_invalid_request_no_data(error_msg=msg)

    def test_invalid_request_invalid_credentials(self):
        msg = "Invalid credentials fournis"
        super(Module_Test_Api_Fr_Locale,
              self).test_invalid_request_invalid_credentials(error_msg=msg)

    def test_invalid_request_corrupt_cacerts_file(self):
        msg = "Un probl\u00e8me est survenu en essayant de se connecter"\
            " \u00e0 des serveurs Secure Trading"
        super(Module_Test_Api_Fr_Locale,
              self).test_invalid_request_corrupt_cacerts_file(error_msg=msg)

    def test_invalid_request_invalid_cacerts_file(self):
        msg = "Un probl\u00e8me est survenu en essayant de se connecter"\
            " \u00e0 des serveurs Secure Trading"
        super(Module_Test_Api_Fr_Locale,
              self).test_invalid_request_invalid_cacerts_file(error_msg=msg)

    def test_auth_decline(self):
        msg = "D\xe9clin"
        super(Module_Test_Api_Fr_Locale, self).test_auth_decline(error_msg=msg)

    def test_auth_sofort(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_auth_sofort(error_msg=msg)

    def test_auth_ach(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_auth_ach(error_msg=msg)

    def test_refund(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_refund(error_msg=msg)

    def test_refund_cft(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_refund_cft(error_msg=msg)

    def test_store(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_store(error_msg=msg)

    def test_cachetokenise(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_cachetokenise(
            error_msg=msg)

    def test_order(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_order(error_msg=msg)

    def test_orderdetails(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_orderdetails(error_msg=msg)

    def test_accountcheck(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_accountcheck(error_msg=msg)

    def test_threedquery(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_threedquery(error_msg=msg)

    def test_multi_threedquery_auth_enrolled(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale,
              self).test_multi_threedquery_auth_enrolled(error_msg=msg)

    def test_multi_threedquery_auth_notenrolled(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale,
              self).test_multi_threedquery_auth_notenrolled(error_msg=msg)

    def test_currencyrate(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_currencyrate(error_msg=msg)

    def test_riskdec(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_riskdec(error_msg=msg)

    def test_identitycheck(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_identitycheck(
            error_msg=msg)

    def test_transactionquery(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_transactionquery(
            error_msg=msg)

    def test_transactionupdate(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale, self).test_transactionupdate(
            error_msg=msg)

    def test_multi_accountcheck_subscription(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale,
              self).test_multi_accountcheck_subscription(error_msg=msg)

    def test_seperate_accountcheck_subscription(self):
        msg = "D'accord"
        super(Module_Test_Api_Fr_Locale,
              self).test_seperate_accountcheck_subscription(error_msg=msg)

if __name__ == "__main__":
    script_name = sys.argv[0]
    passed_args, unittest_args = module_test_api.get_args()
    Module_Test_Api_Fr_Locale.PASSED_ARGS = passed_args
    unittest.main(argv=[script_name] + unittest_args)
