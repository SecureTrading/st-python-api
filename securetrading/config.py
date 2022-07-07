from __future__ import unicode_literals
import locale
from securetrading import util
import securetrading


class Config(object):
    """The Trust Payments configuration object.

    This Object stores the settings that the
API will use."""

    __slots__ = ["_username", "_jsonversion", "_http_receive_timeout",
                 "_http_max_retries", "_http_retry_sleep", "_username",
                 "_password", "_datacenterurl", "_datacenterpath",
                 "_http_max_allowed_connection_time",
                 "_http_connect_timeout",
                 "_http_response_headers",
                 "_http_proxy", "_ssl_certificate_file",
                 "_libraryversion",
                 "_locale",
                 "_acceptcustomeroutput",
                 ]

    def __init__(self):
        """Initialises the configuration object.

        This will initialise the configuration object and set the
default values that can then be overridden.

        Usage:
           >>> import securetrading
           >>> config = securetrading.Config()
           >>> config.username = "webserviceuser@merchant.com"
           >>> config.password = "P455w0rd!"
        """
        self._jsonversion = "1.00"
        self._http_connect_timeout = 10
        self._http_receive_timeout = 60
        self._http_max_retries = 6
        self._http_retry_sleep = 0.5
        self._http_max_allowed_connection_time = 10
        self._http_response_headers = []
        self._username = ""
        self._password = ""
        self._datacenterurl = "https://webservices.securetrading.net"
        self._datacenterpath = "/json/"
        self._http_proxy = None
        self._ssl_certificate_file = None
        self._libraryversion = securetrading.__version__
        self._locale = "en_gb"
        self._acceptcustomeroutput = None

    @property
    def locale(self):
        """The locale for the API messages.

        This property holds the locale for the message and errors
that will be returned by the API.

        Args:
           value: (optional [string]) The locale for the API to use
for language translation. The list of available locales
is obtained from python's locale module which accesses
the POSIX locale database.
e.g. values = [s for s in locale.locale_alias.keys()]

        Raises:
           AssertionError: If the value is not a valid locale
as specified in locale.locale_alias.keys()

        Returns:
           The current locale setting.

        Usage:
           >>> config.locale = "en_gb"
           or
           >>> locale = config.locale
        """
        return self._locale

    @locale.setter
    def locale(self, value):
        msg = "Please specifiy a valid locale according to,\
 the locale module"
        values = [s for s in locale.locale_alias.keys()]
        if util._is_python_2():
            values = [s.decode("latin1") for s in values]
        assert value in values, msg
        self._locale = value

    @property
    def libraryversion(self):
        """The libraryversion of the API.

        Returns:
           The stored API libraryversion.

        Usage:
           >>> libraryversion = config.libraryversion
        """
        return self._libraryversion

    @property
    def ssl_certificate_file(self):
        """The SSL Certificate file location.

        This property holds the SSL Certificate file location that
is to be used by the Trust Payments API.

        Args:
           value: (optional [string]) The location of the certificate file.

        Returns:
           The stored SSL Certificate file location.

        Usage:
           >>> config.ssl_certificate_file = "location/of/file.pem"
           or
           >>> certicate_location = config.ssl_certificate_file
        """
        return self._ssl_certificate_file

    @ssl_certificate_file.setter
    def ssl_certificate_file(self, value):
        self._ssl_certificate_file = value

    @property
    def http_proxy(self):
        """The HTTP proxy data for the API.

        This property holds the HTTP proxy data that the API will
use to connect to Trust Payments.

        Args:
           value: (optional [dict]) A dictionary with the key "https".

        Raises:
           AssertionError: If the value is not a dictionary.

        Returns:
           The HTTP proxy data.

        Usage:
           >>> config.http_proxy = {'https':'https://IP:PORT'}
           or
           >>> http_proxy = config.http_proxy
        """
        return self._http_proxy

    @http_proxy.setter
    def http_proxy(self, value):
        msg = "A dict is required with https only \
e.g: {'https':'https://IP:PORT'}"
        isDict = isinstance(value, dict)
        assert (isDict and list(value.keys()) == ["https"]), msg
        self._http_proxy = value

    @property
    def http_max_allowed_connection_time(self):
        """The maximum allowed HTTP connect timeout for the API.

        This property holds the http_max_allowed_connection_time,
which is the maximum time in seconds allowed for HTTP
connections that connect to Trust Payments.

        Args:
           value: (optional [int or float]) The numeric value in seconds.

        Raises:
           AssertionError: If the value is not either a float or an int.

        Returns:
           The maximum allowed HTTP connect timeout.

        Usage:
           >>> config.http_max_allowed_connection_time = 10
           or
           >>> http_max_time = config.http_max_allowed_connection_time
        """
        return self._http_max_allowed_connection_time

    @http_max_allowed_connection_time.setter
    def http_max_allowed_connection_time(self, value):
        msg = "An int or float is required for the timeout"
        assert isinstance(value, (float, int)), msg
        self._http_max_allowed_connection_time = value

    @property
    def datacenterurl(self):
        """The Trust Payments data center URL.

        This property holds the data center URL that the API will
use to connect to Trust Payments.

        Args:
           value: (optional [string]) The URL of the data center.

        Returns:
           The Trust Payments data center URL.

        Usage:
          >>> config.datacenterurl = "https://webservices.securetrading.net"
          or
          >>> datacenterurl = config.datacenterurl

        """
        return self._datacenterurl

    @datacenterurl.setter
    def datacenterurl(self, value):
        self._datacenterurl = value

    @property
    def datacenterpath(self):
        """The Trust Payments data center path.

        This property holds the data center path that the API will
use to connect to Trust Payments.

        Args:
           value: (optional [string]) The path of the data center.

        Returns:
           The Trust Payments data center path.

        Usage:
          >>> config.datacenterpath = "/json/"
          or
          >>> datacenterpath = config.datacenterpath

        """
        return self._datacenterpath

    @datacenterpath.setter
    def datacenterpath(self, value):
        self._datacenterpath = value

    @property
    def jsonversion(self):
        """The Trust Payments JSON interface version.

        This property holds the JSON interface version and will
be passed to Trust Payments.

        Args:
           value: (optional [string]) The version value to use.
           See further documentation for all allowed values.

        Returns:
           The Trust Payments JSON interface version used.

        Usage:
           >>> config.jsonversion = "1.00"
           or
           >>> jsonversion = config.jsonversion
        """
        return self._jsonversion

    @jsonversion.setter
    def jsonversion(self, value):
        self._jsonversion = value

    @property
    def http_connect_timeout(self):
        """The HTTP connection timeout for the API.

        This property holds the timeout for a single HTTP connection
when connecting to Trust Payments.

        Args:
           value: (optional [int or float]) The numeric value in seconds.

        Raises:
           AssertionError: If the value is not either a float or an int.

        Returns:
           The HTTP connect timeout.

        Usage:
           >>> config.http_connect_timeout = 10
           or
           >>> http_connect_timeout = config.http_connect_timeout
        """
        return self._http_connect_timeout

    @http_connect_timeout.setter
    def http_connect_timeout(self, value):
        msg = "An int or float is required for the timeout"
        assert isinstance(value, (float, int)), msg
        self._http_connect_timeout = value

    @property
    def http_receive_timeout(self):
        """The HTTP receive timeout of the API.

        This property holds the HTTP receive timeout. HTTP connections
to Trust Payments must respond within this limit.

        Args:
           value: (optional [int or float]) The numeric value in seconds.

        Raises:
           AssertionError: If the value is not either a float or an int.

        Returns:
           The HTTP receive timeout.

        Usage:
           >>> config.http_receive_timeout = 60
           or
           >>> http_receive_timeout = config.http_receive_timeout
        """
        return self._http_receive_timeout

    @http_receive_timeout.setter
    def http_receive_timeout(self, value):
        msg = "An int or float is required for the timeout"
        assert isinstance(value, (float, int)), msg
        self._http_receive_timeout = value

    @property
    def http_max_retries(self):
        """The maximum number of HTTP retries.

        This property holds the maximum number of HTTP retries the
API will perform.

        Args:
           value: (optional [int]) The maximum number retries.

        Raises:
           AssertionError: If the value is not an int.

        Returns:
           The maximum number of HTTP retries.

        Usage:
           >>> config.http_max_retries = 6
           or
           >>> http_max_retries = config.http_max_retries
        """
        return self._http_max_retries

    @http_max_retries.setter
    def http_max_retries(self, value):
        msg = "An int is required for maximum number of retries"
        assert isinstance(value, int), msg
        self._http_max_retries = value

    @property
    def http_retry_sleep(self):
        """The HTTP retry sleep time for the API.

        This property holds the HTTP retry sleep time that the API
will use to sleep between connection attempts to Trust Payments.

        Args:
           value: (optional [int or float]) The numeric value in seconds.

        Raises:
           AssertionError: If the value is not either a float or an int.

        Returns:
           The HTTP retry sleep time.

        Usage:
           >>> config.http_retry_sleep = 0.5
           or
           >>> http_retry_sleep = config.http_retry_sleep
        """
        return self._http_retry_sleep

    @http_retry_sleep.setter
    def http_retry_sleep(self, value):
        msg = "An int or float is required for the sleep period"
        assert isinstance(value, (float, int)), msg
        self._http_retry_sleep = value

    @property
    def http_response_headers(self):
        """A list of which HTTP response headers should be returned by the API.

        This property holds which HTTP response headers should be returned
from Trust Payments on the Response object. If no headers are requested the
Response object will not contain the headers key

        Args:
           value: (optional [list]) A list of response headers which want to be
made available on the Response object.

        Returns:
           The HTTP response headers in a dict set on the key 'headers' on the
Response object.

        Usage:
           >>> config.http_response_headers = ["Content-type"]
           >>> api = securetrading.Api(config)
           >>> response = api.process(request)
           >>> headers = response["headers"]
        """
        return self._http_response_headers

    @http_response_headers.setter
    def http_response_headers(self, values):
        msg = "A list of strings are required to flag whether the header is \
returned"
        assert isinstance(values, list), msg
        lowered_values = []
        str_typ = str
        if util._is_python_2():
            str_typ = basestring
        for value in values:
            assert isinstance(value, str_typ), msg
            lowered_values.append(value.lower())
        self._http_response_headers = lowered_values

    @property
    def username(self):
        """The WebServices user's username used to connect.

        This property is used to hold your WebServices user's
username that will be used to connect to Trust Payments

        Args:
           value: (optional [string]) WebServices user's username.

        Returns:
           The username value.

        Usage:
           >>> config.username = "webserviceuser@merchant.com"
           or
           >>> username = config.username
        """
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        """The WebServices user's password used to connect.

        This property is used to hold your WebServices user's
password that will be used to connect to Trust Payments.

        Args:
           value: (optional [string]) WebServices user's password.

        Returns:
           The password value.

        Usage:
           >>> config.password = "P455w0rd!"
           or
           >>> password = config.password
        """
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def acceptcustomeroutput(self):
        """Allowed acceptcustomeroutput version.

        This property holds the version of the desired customer output
result.
This feature might be useful in case of multi requests like:
RISCDEC + THREEDQUERY + AUTH + SUBSCRIPTION
"Main" response item will be populated with "customeroutput" field and
it might help to figure out whether response is successful or not.

        Args:
           value: (optional [string]) The acceptcustomeroutput is used
to pass desired version of the "customeroutput" feature.
None is default value, customeroutput is not returned in the API response.
"1.00" is old / deprecated version of the customeroutput result. Added for
backward compatibility.
"2.00" is used to populate "authorization" response item with "customeroutput"
information.

        Raises:
           AssertionError: If the value is not a valid accept
customer output value

        Returns:
           The current accept customer output setting.

        Usage:
           >>> config.acceptcustomeroutput = "2.00"
           or
           >>> acceptcustomeroutput = config.acceptcustomeroutput
        """
        return self._acceptcustomeroutput

    @acceptcustomeroutput.setter
    def acceptcustomeroutput(self, value):
        valid_values = [None, "1.00", "2.00"]
        error_values = ", ".join([
            str(valid_value) for valid_value in valid_values
        ])
        msg = "Invalid accept customer output value. \
Available options: %s" % error_values
        assert value in valid_values, msg
        self._acceptcustomeroutput = value
