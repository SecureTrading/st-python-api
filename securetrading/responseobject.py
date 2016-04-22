import securetrading.abstractstobject


class Response(securetrading.abstractstobject.AbstractStObject):
    """A response object containing the data returned by
Secure Trading."""

    def __init__(self):
        """Initialises the Secure Trading Response object.

        Usage:
           >>> import securetrading
           >>> response = securetrading.Response()
           >>> response.update(data)
        """
        super(Response, self).__init__()
