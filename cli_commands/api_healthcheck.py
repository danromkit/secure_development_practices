import sys

import requests
from requests.models import Response
from requests.exceptions import ConnectionError


def api_healthcheck():
    try:
        response: Response = requests.get("http://0.0.0.0:6080/")
    except ConnectionError:
        sys.exit(1)
    if response.status_code == 405:
        sys.exit(0)


api_healthcheck()
