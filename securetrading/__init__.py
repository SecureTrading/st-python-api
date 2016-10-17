# Secure Trading Python API
# Authors: Secure Trading Ltd
# Configuration variables

from __future__ import unicode_literals
from .requestobject import Request
from .requestobject import Requests
from .responseobject import Response
from .exceptions import SecureTradingError
from .exceptions import ApiError
from .exceptions import HttpError
from .exceptions import ConnectionError
from .exceptions import SendReceiveError
from .converter import Converter
from .config import Config
from .api import Api
from .phrasebook import PhraseBook

import securetrading.util
import pkgutil
import platform

dataFile = 'data/errormessages.json'
data = pkgutil.get_data('securetrading', dataFile).decode("utf-8")
error_messages = securetrading.util.json.loads(data)

dataFile = 'data/phrasebook.json'
data = pkgutil.get_data('securetrading', dataFile).decode("utf-8")
phrase_book = securetrading.util.json.loads(data)


__title__ = 'Secure Trading Python API'
__version__ = "1.0.8"
__author__ = 'Secure Trading Ltd'
__license__ = 'MIT'
__copyright__ = 'Copyright 2016 Secure Trading Ltd'

version_information = ["Python",
                       platform.python_version(),
                       securetrading.__version__,
                       platform.platform(),
                       ]
version_info = "::".join(version_information)
