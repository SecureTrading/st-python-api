from __future__ import unicode_literals
import securetrading
import securetrading.phrasebook as phrasebook


class Converter(object):

    def __init__(self, config):
        super(Converter, self).__init__()
        self.config = config
        self.phrasebook = phrasebook.PhraseBook(self.config)

    def _encode(self, request_object):
        request = []
        debug = "{0} Begin encoding".format(
            request_object["requestreference"])
        securetrading.util.logger.debug(debug)
        libraryversion = "python_{0}".format(securetrading.__version__)

        if isinstance(request_object, securetrading.Requests):
            debug = "{0} securetrading.Requests object detected".format(
                request_object["requestreference"])
            securetrading.util.logger.debug(debug)
            for request_obj in request_object["requests"]:
                request.append(request_obj)
        elif isinstance(request_object, securetrading.Request):
            debug = "{0} securetrading.Request object detected".format(
                request_object["requestreference"])
            securetrading.util.logger.debug(debug)
            request.append(request_object)
        else:
            data = ["Unknown type of object ({0}), encoding failed".format(
                    type(request_object))]
            raise securetrading.ApiError("10", data=data)

        st_structure = {"alias": self.config.username,
                        "version": self.config.jsonversion,
                        "request": request,
                        "libraryversion": libraryversion,
                        }

        try:
            result = securetrading.util.json.dumps(st_structure)
        except (UnicodeDecodeError, TypeError) as e:
            # This will raise if a latin-1 encoded string is passed in.
            data = ["All types should be specified in unicode"]
            raise securetrading.ApiError("10", data=data)
        debug = "{0} Finished encoding".format(
            request_object["requestreference"])
        securetrading.util.logger.debug(debug)
        return result

    def _decode(self, response, request_reference):
        try:
            result = securetrading.util.json.loads(response)
        except Exception as e:
            raise securetrading.SendReceiveError("5", data=e)
        debug = "{0} Begin decoding".format(request_reference)
        securetrading.util.logger.debug(debug)
        response_object = securetrading.Response()
        for k in ["requestreference", "version"]:
            response_object.update({k: result[k]})
        response_object["responses"] = result["response"]
        response_data = None
        debug = "{0} Finished decoding".format(request_reference)
        securetrading.util.logger.debug(debug)
        return response_object
