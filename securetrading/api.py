from __future__ import unicode_literals
import securetrading
import securetrading.httpclient as httpclient
import securetrading.phrasebook as phrasebook


class Api(object):
    """Trust Payments Python API.

    This is the wrapper class that handles processing requests to
Trust Payments and returns the response.
    """

    def __init__(self, config):
        """Initialises the Trust Payments Python API.

        This method will initialise the Trust Payments Python API
that can submit requests to Trust Payments and handle
the response. The API is thread-safe, therefore it can
be used by multiple threads at the same time.

        Args:
           config:  A securetrading.SecureTradingConfig
object containing various settings.

        Usage:
           >>> import securetrading
           >>> st_api = securetrading.Api(st_config)
        """
        self.config = config
        self.phrasebook = phrasebook.PhraseBook(self.config)
        super(Api, self).__init__()

    def process(self, request):
        """Submits a request to be processed by Trust Payments.

        This method takes the details of the request and then connects
and sends the data to Trust Payments, waiting for a reply or timeout
before returning the response.

        Args:
           request: Either a securetrading.Request or a securetrading.Requests
object containing the details of the request.

        Returns:
           A securetrading.Response object containing all the response
details

        Usage:
           >>> response = st_api.process(request)
        """
        request_reference = ""
        try:
            if type(request) == dict:
                st_request = securetrading.Request()
                st_request.update(request)
                request = st_request

            self._verify_request(request)
            request_reference = request["requestreference"]
            info = "{0} Begin request".format(request_reference)
            securetrading.util.logger.info(info)
            http_client = httpclient._get_client(request_reference,
                                                 self.config)
            request.verify()
            url = request.get("datacenterurl", self.config.datacenterurl)
            url += request.get("datacenterpath", self.config.datacenterpath)
            converter = securetrading.Converter(self.config)
            request_data = converter._encode(request)
            response, response_headers = http_client._main(url,
                                                           request_data,
                                                           request_reference,
                                                           request)
            result = converter._decode(response, response_headers,
                                       request_reference)
            self._verify_result(result, request_reference)
        except securetrading.SecureTradingError as e:
            result = self._generate_st_error(e, request_reference)
        except Exception as e:
            result = self._generate_error(e, request_reference)
        info = "{0} Finished request".format(request_reference)

        get_error_message = securetrading.util._get_errormessage
        for response in result["responses"]:
            response["errormessage"] =\
                get_error_message(response["errorcode"],
                                  response.get("errormessage", ""),
                                  self.phrasebook)

        securetrading.util.logger.info(info)
        return result

    def _verify_request(self, request):
        if not isinstance(request, securetrading.Request):
            data = ["Incorrect type of request specified"]
            raise securetrading.SecureTradingError("10", data=data)

    def _verify_result(self, result, request_reference):
        if result.get("requestreference") != request_reference:
            msg = "Different request reference: sent ({0}) received ({1})"\
                .format(request_reference, result.get("requestreference"))
            data = [msg]
            raise securetrading.SecureTradingError("9", data=data)

    def _generate_error(self, e, request_reference):
        excep = "Trust Payments API had an unexpected error"
        securetrading.util.logger.exception(excep)
        data = ["{0}".format("\n".join(e.args))]
        error = securetrading.SecureTradingError("9", data=data)
        return self._generate_st_error(error, request_reference)

    def _generate_st_error(self, e, request_reference):
        response = securetrading.Response()
        response["requestreference"] = request_reference
        response_data = {}
        response_data.update({"errorcode": "{0}".format(e.code),
                              "errordata": e.data,
                              "requesttypedescription": "ERROR",
                              "requestreference": request_reference,
                              })
        response.setdefault("responses", [response_data])
        return response
