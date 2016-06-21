from __future__ import unicode_literals
import securetrading
import time
import securetrading.util
import platform


def _get_requests_lib():
    try:
        import requests
        split_version = requests.__version__.split(".")
        requests_version = requests.__version__
    except ImportError as e:
        requests = None
        split_version = ["0", "0", "0"]
        requests_version = "Not found"

    requests_version = tuple(map(int, split_version))
    min_requests_version = securetrading.util.min_requests_version
    if requests_version < min_requests_version:
        data = ["Current requests version: {0}".format(requests_version)]
        raise securetrading.SecureTradingError("2", data=data)
    return requests

requests = _get_requests_lib()


def _get_client(request_reference, config):
    if requests:
        debug = "{0} Using the 'requests' library".format(request_reference)
        securetrading.util.logger.debug(debug)
        client = HTTPRequestsClient(config)
    else:
        msg = "No request library found"
        raise securetrading.SecureTradingError("2", data=[msg])
    return client


class GenericHTTPClient(object):

    def __init__(self, config):
        super(GenericHTTPClient, self).__init__()
        self.config = config
        self.connect_time_out = self.config.http_connect_timeout
        self.read_time_out = self.config.http_receive_timeout
        self.proxies = self.config.http_proxy

    def _close(self):
        raise NotImplementedError

    def _receive(self):
        raise NotImplementedError

    def _send(self, url, request_data, request_reference):
        raise NotImplementedError

    def _connect(self, url):
        raise NotImplementedError

    def _get_headers(self, request_reference):
        version_info = securetrading.version_info
        python_version = platform.python_version()
        user_agent = "Python-{0}".format(python_version)

        headers = {"Content-Type": "application/json;charset=utf-8",
                   "Accept": "application/json",
                   "Accept-Encoding": "gzip",
                   "User-Agent": user_agent,
                   "REQUESTREFERENCE": request_reference,
                   "VERSIONINFO": version_info,
                   "Connection": "close",
                   }
        return headers

    def _verify_response(self, status_code, response):
        pass

    def _handle_invalid_response(self, code, content):
        mapping = {401: "6",
                   }.get(code, "8")
        raise securetrading.ConnectionError(mapping, http_status_code=code)

    def _get_connection_time_out(self, start_time):
        connection_time = self.config.http_max_allowed_connection_time
        time_remaining = connection_time - (time.time() - start_time)
        connect_time_out = min([self.connect_time_out,
                                time_remaining,
                                ])
        return (time_remaining <= 0, connect_time_out)

    def _main(self, url, request_data, request_reference, request):
        info = "{0} Begin transport".format(request_reference)
        securetrading.util.logger.info(info)
        connect_start = time.time()
        try:
            self._connect(url)
        except Exception as e:
            debug = "{0} Connect error: {0}".format(request_reference, e)
            securetrading.util.logger.debug(debug, exc_info=True)
            raise securetrading.ConnectionError("7", data=e)
        conn_time_taken = time.time() - connect_start
        info = "{0} Connect time {1:.2f}".format(request_reference,
                                                 conn_time_taken)
        securetrading.util.logger.info(info)
        try:
            recv_start = time.time()
            try:
                self._send(url, request_data, request_reference)
                (status_code, response) = self._receive()
            except (securetrading.SecureTradingError) as e:
                securetrading.util.logger.debug(e, exc_info=True)
                raise
            except Exception as e:
                debug = "{0} Receiving error".format(request_reference)
                securetrading.util.logger.debug(debug, exc_info=True)
                raise securetrading.SendReceiveError("4", data=e)
            finally:
                recv_time_taken = time.time() - recv_start
                info = "{0} Receive time: {1:.2f}".format(request_reference,
                                                          recv_time_taken)
                securetrading.util.logger.info(info)
            try:
                self._verify_response(status_code, response)
            finally:
                recv_time_taken = time.time() - recv_start
                info = "{0} Finished transport: {1:.2f}".format(
                    request_reference, recv_time_taken)
                securetrading.util.logger.info(info)
        finally:
            self._close()
        return response


class HTTPRequestsClient(GenericHTTPClient):

    def _close(self):
        pass

    def _connect(self, url):
        pass

    def _get_headers(self, *args, **kwargs):
        headers = super(HTTPRequestsClient, self)._get_headers(*args, **kwargs)
        requests_user_agent = requests.utils.default_user_agent()
        user_agent = "{0}:{1}".format(headers["User-Agent"],
                                      requests_user_agent)
        headers["User-Agent"] = user_agent
        return headers

    def _send(self, url, request_data, request_reference):
        auth = requests.auth.HTTPBasicAuth(
            self.config.username, self.config.password)
        method = "POST"
        headers = self._get_headers(request_reference)
        final = False
        start_time = time.time()

        current_retry_count = 0
        while not final:
            msg = None
            (timed_out, connect_time_out) = self._get_connection_time_out(
                start_time)
            if timed_out:
                msg = "{0} Maximum time reached whilst trying to connect to \
{1}".format(request_reference, url)
            elif current_retry_count > self.config.http_max_retries:
                msg = "{0} Maximum number of attempts reached whilst trying \
to connect to {1}".format(request_reference, url)
            if msg is not None:
                raise securetrading.ConnectionError("7", data=[msg])
            try:
                msg = "{0} Connect to {1}".format(request_reference, url)
                securetrading.util.logger.debug(msg, exc_info=True)

                # Future - we should be implementing the Retry logic using a
                # HTTPAdapter:
                # http://docs.python-requests.org/en/latest/user/advanced/#t
                # ransport-adapters
                # as shown below. But currently the Adapters do not support
                # having both a count and timelimit on the retry logic. When
                # this is done we can go back and put this in.
                # import requests.packages.urllib3.util.retry
                # import requests.packages.urllib3

                # retry=requests.packages.urllib3.Retry(
                #   total=10,#self.config.httpMaxRetries,
                #   connect=10,#self.config.httpMaxRetries,
                #   read=0,
                #   backoff_factor=0.001,
                #   )
                # s = requests.Session()
                # a = requests.adapters.HTTPAdapter(max_retries=retry)
                # s.mount('https://', a)
                # The list of trusted CA's come from the request library.

                kwargs = {"method": method,
                          "url": url,
                          "data": request_data,
                          "auth": auth,
                          "headers": headers,
                          "verify": True,
                          "proxies": self.proxies,
                          "timeout": (connect_time_out,
                                      self.read_time_out),
                          }
                if self.config.ssl_certificate_file is not None:
                    kwargs["verify"] = self.config.ssl_certificate_file
                self.response = requests.request(**kwargs)
                final = True
            except (requests.exceptions.ConnectTimeout,
                    requests.exceptions.ConnectionError) as e:
                msg = "{0} Connection attempt {1} failed due to {2}, \
maximum allowed {3}".format(request_reference,
                            current_retry_count,
                            e,
                            self.config.http_max_retries)
                securetrading.util.logger.info(msg)
                current_retry_count += 1
                time.sleep(self.config.http_retry_sleep)
            except Exception as e:
                final = True
                self.response = None
                self._handle_exception(e)

    def _handle_exception(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            raise securetrading.ConnectionError("7", data=e)
        else:
            raise securetrading.ConnectionError("8", data=e)

    def _receive(self):
        text = self.response.text
        status_code = self.response.status_code
        if status_code != requests.codes.ok:
            self._handle_invalid_response(status_code, text)
        return status_code, text
