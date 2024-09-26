from requests.exceptions import HTTPError, RequestException


class RestRequestException(RequestException):
    """Rest request exception."""

    pass


class RestHTTPError(HTTPError):
    """Rest HTTP error."""

    pass


class RestAPIError(Exception):
    """Rest API error."""

    pass
