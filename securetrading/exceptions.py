from __future__ import unicode_literals
import securetrading.util
# Exception class


class SecureTradingError(Exception):
    """The generic class for Secure Trading errors."""

    def __init__(self, code, data=None):
        """Initialises a SecureTradingError.

        This will initialise the SecureTradingError and set the code plus any
 additional information.

        Args:
           code: [string] The error code to map.
           data: (optional [list]) The additional information about the error
                 or Exception that was originally raised.

        Usage:
           >>> import securetrading
           >>> error = securetrading.SecureTradingError(1)
        """
        if data is None:
            data = []
        elif isinstance(data, Exception):
            data = ["{0}".format(data)]
        assert isinstance(data, list), "list object required for data"

        self.code = code
        self.data = data
        english = "{0}".format(code)
        extra = "\n".join(data)
        self._english = english
        if extra:
            self._english = self._english + " " + extra
        super(SecureTradingError, self).__init__(english)

    def __unicode__(self):
        return self._english

    if not securetrading.util._is_python_2():
        def __str__(self):
            return self.__unicode__()
    else:
        def __str__(self):
            # Below python 3 unicode exceptions are not supported.
            return unicode(self).encode('utf-8')


class ApiError(SecureTradingError):
    """An error for when the API doesn't get called correctly.

    Usage:
       >>> import securetrading
       >>> error = securetrading.ApiError(10)
    """


class HttpError(SecureTradingError):
    """A generic class for all HTTP errors.

    Usage:
       >>> import securetrading
       >>> error = securetrading.HttpError(1)
    """
    pass


class ConnectionError(HttpError):
    """An error to handle connection issues.

    Usage:
       >>> import securetrading
       >>> error = securetrading.ConnectionError(6, 401, "Unathorized")
    """

    def __init__(self, code=None, http_status_code=None, data=None):
        """Initialises a ConnectionError.

        This will initialise a ConnectionError and set the code, the
HTTP status code and any additional information to be passed on.

        Args:
           code: [int] The error code to map to.
           http_status_code: [int] The HTTP status code.
           data: (optional [list]) a list of additional information about
           the error or the Exception that was originally raised.
        """
        errorMessage = http_status_code
        if data is None:
            data = []
        if http_status_code is not None:
            apache_code = "HTTP code {0}".format(http_status_code)
            data.extend([apache_code])
        super(ConnectionError, self).__init__(code, data=data)


class SendReceiveError(HttpError):
    """An error to handle issues sending to or receiving from Secure Trading.

    Usage:
       >>> import securetrading
       >>> error = securetrading.SendReceiveError(4)
    """
