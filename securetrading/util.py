from __future__ import unicode_literals

import logging
import os
import sys
import securetrading

logger = logging.getLogger("securetrading")
min_requests_version = (2, 9, 0)
min_requests_version_str = ".".join([str(f) for f in min_requests_version])

try:
    import json  # pylint: disable=unused-import
except ImportError:
    # Could use simplejson here if we wanted to.
    raise ImportError("Secure Trading API requires a JSON library")


def _is_python_2():
    return sys.version_info < (3, 0)


def _get_random(n, all_chars=list('0123456789abcdefghjkmnpqrtuvwxy'),
                urandom=os.urandom,
                ):
    length = len(all_chars)

    def ord_or_not(x):
        if _is_python_2():
            x = ord(x)
        return x

    return "".join([all_chars[ord_or_not(c) % length] for c in urandom(n)])


def _get_errormessage(error_code, error_message, phrasebook):
    english = securetrading.error_messages.get(error_code, error_message)
    return phrasebook.lookup(english)
