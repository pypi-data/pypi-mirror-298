

from typing import Optional

from mantlebio.core.session.helpers import MantleSessionResponse
from requests import Response


def create_test_reponse(status_code: int, content: Optional[bytes] = None, url: Optional[str] = None)-> MantleSessionResponse:
    '''
    Create a test response object

    Args:
        status_code: status code of the response
        content: content of the response

    Returns:
        Response object
    '''
    response = Response()
    response.status_code = status_code
    response._content = content
    response.url = url or ""

    return MantleSessionResponse(response)