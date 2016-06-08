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

    def __init__(self):
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
        requestreference = securetrading.util._get_random(8)
        self["requestreference"] = "A{0}".format(requestreference)
        self["versioninfo"] = securetrading.version_info

    def _set_cachetoken(self, cachetoken):
        try:
            json_cachetoken = base64.decodestring(cachetoken.encode("ascii"))
            data = securetrading.util.json.loads(
                json_cachetoken.decode("utf-8")
                )
            result = data
        except (ValueError, binascii.Error) as e:
            result = {"cachetoken": cachetoken}
        debug = "{0} cachetoken being set as {1}".format(
            self.get("requestreference"), result)
        securetrading.util.logger.debug(debug)
        for key, value in result.items():
            super(AbstractStObject, self).__setitem__(key, value)


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
            for key in ["datacenterurl"]:
                # Ensures we can only override the datacenterurl in one place
                if key in request:
                    data = "The key '{0}' must be specifed in the outer \
'securetrading.Requests' object".format(key)
                    raise securetrading.ApiError("10", data=[data])

    def _validate_requests(self, requests):
        for request in requests:
            msg = "Invalid requests specified"
            assert isinstance(request, Request), msg
