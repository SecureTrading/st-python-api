from __future__ import unicode_literals
from securetrading.abstractstobject import AbstractStObject
import securetrading.util
import binascii
import base64


class Request(AbstractStObject):
    """A single request object.

    The single request object allows you to specify one
request to be processed at a time. See the
documentation for the usable keys.
"""

    def __init__(self, extra_headers=None):
        """Initialises the Secure Trading Request object.

        This method will initialise the Secure Trading Request
object and set the default values for some of
the fields to send.

        Usage:
           >>> import securetrading
           >>> request = securetrading.Request()
           >>> request.update(data)
        """
        super(Request, self).__init__()
        self.extra_headers = extra_headers
        requestreference = securetrading.util._get_random(8)
        self["requestreference"] = "A{0}".format(requestreference)
        self["versioninfo"] = securetrading.version_info

    def _set_cachetoken(self, cachetoken):
        try:
            met = getattr(base64, "decodebytes", None)
            if met is None:
                met = base64.decodestring
            json_cachetoken = met(cachetoken.encode("ascii"))
            data = securetrading.util.json.loads(
                json_cachetoken.decode("utf-8")
                )
            cachetoken = data["cachetoken"]
        except (ValueError, binascii.Error, KeyError):
            # Using original cachetoken value
            pass
        debug = "{0} cachetoken being set as {1}".format(
            self.get("requestreference"), cachetoken)
        securetrading.util.logger.debug(debug)
        self.__setitem__("cachetoken", cachetoken, use_set_method=False)

    @staticmethod
    def _validate_datacenterurl(value):
        msg = "'datacenterurl' should not be set in the Request object. Use \
Config instead."
        assert not value, msg

    @staticmethod
    def _validate_datacenterpath(value):
        msg = "'datacenterpath' should not be set in the Request object. Use \
Config instead."
        assert not value, msg


class Requests(Request):
    """This wraps single requests into one object.

    The Requests object allows you process multiple requests at the same
time. e.g. an AUTH and SUBSCRIPTION at the same time.
For more details see further documentation."""

    def verify(self):
        """This method verifies the Requests object.

        Raises:
           ApiError: If certain keys are missing or fields are in
the incorrect location within the object.
        """
        if "requests" not in self:
            data = "missing key requests"
            raise securetrading.ApiError("10", data=[data])
        for request in self.get("requests", []):
            if request.extra_headers:
                data = "The property 'extra_headers' must be specifed in the \
outer 'securetrading.Requests' object"
                raise securetrading.ApiError("10", data=[data])

    def _validate_requests(self, requests):
        for request in requests:
            msg = "Invalid requests specified"
            assert isinstance(request, Request), msg
