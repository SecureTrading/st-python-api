import logging
import pprint
import securetrading


logging.basicConfig(filename='example.log', level=logging.INFO)

# Configure global settings
st_config = securetrading.Config()
st_config.username = "YOURUSERNAME"
st_config.password = "YOURPASSWORD"

# create the Api object with the config
st_api = securetrading.Api(st_config)

# Create the request dictionary.
AUTH_example = {"pan": "4111111111111111",
                "expirydate": "11/2031",
                "securitycode": "123",
                "requesttypedescription": "AUTH",
                "accounttypedescription": "ECOM",
                "sitereference": "YOURSITEREF",
                "paymenttypedescription": "VISA",
                "currencyiso3a": "GBP",
                "baseamount": "100",
                "billingfirstname": "first",
                }
st_request = securetrading.Request()
st_request.update(AUTH_example)

# Process the request or more requests
st_response = st_api.process(st_request)

# Process the response
action = st_response["responsedata"]["customeroutput"]
if action == "RESULT":
    print("Successful transaction - more information is available in the \
response object")

else:
    print("Something went wrong. Please fix and try again. ({0}) More \
information may be in the response object:".format(
            st_response["responsedata"]["errormessage"]))

pprint.pprint(st_response)
