from __future__ import unicode_literals
import securetrading


class AbstractStObject(dict):
    """The default Object class inherited by all Secure Trading Objects."""

    def __init__(self, request_reference=None):
        super(AbstractStObject, self).__init__()

    def verify(self):
        """This should be overwritten by the child class
if required."""
        pass

    def update(self, data):
        """Updates the Secure Trading Object with data.

This update method will set the data onto the Secure Trading Object and
will also automatically call validation on some of the values inserted.

        Args:
           data: A dictionary of values to insert.

        Raises:
           This method will raise a securetrading.ApiError during the
automatic validation, if the value is invalid.
        """
        for key in data:
            self.__setitem__(key, data[key])

    def __setitem__(self, key, value):
        debug = "{0} Setting {1}".format(self.get("requestreference"), key)
        securetrading.util.logger.debug(debug)
        validate_method = "_validate_{0}".format(key)
        if hasattr(self, validate_method):
            getattr(self, validate_method)(value)
        set_method = "_set_{0}".format(key)
        if hasattr(self, set_method):
            getattr(self, set_method)(value)
        else:
            super(AbstractStObject, self).__setitem__(key, value)
