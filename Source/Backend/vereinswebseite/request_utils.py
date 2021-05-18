from datetime import datetime
from http import HTTPStatus

from flask import request, current_app

success_response = {"success": True}


def get_int_from_request(key):
    """
    Reads an integer from the request arguments if possible.
    If no paramter with the specified key is available it returns None
    """
    value_str = request.args.get(key, default=None)
    if value_str is None:
        return None

    try:
        return int(value_str)
    except:
        return None


def parse_date(date_string: str) -> (bool, datetime):
    """
    Parses a date time string with the format YYYY-mm-dd
    :return: (True, date) when the parsing was successful
             (False, None) when the parsing was not successful
             (True, None) when date_string is None
    """
    if date_string is None:
        return True, None

    try:
        date = datetime.strptime(date_string, '%Y-%m-%d')
        return True, date
    except ValueError:
        return False, None


def generate_success(return_values, status=HTTPStatus.OK):
    """
    Generates a successful api response with the given key value pairs. API routes should
    use this function to generate their response message
    :param return_values: A dictionary of return values
    :param status: The HTTP status code
    :return:
    """
    response = success_response

    for key in return_values:
        response[key] = return_values[key]

    return response, status


def generate_error(error_title: str, http_status_code: int):
    """
    Generates an error api response with the given error title and status code. API routes should
    use this function to generate their response message
    :param error_title: A short and user friendly summary of the error
    :param http_status_code: The HTTP status code of the error (e.g. 404 or 403, ...)
    :return:
    """
    return {
               "errors": [
                   {
                       "title": error_title,
                       "status": int(http_status_code),
                   }
               ],
               "success": False
           }, int(http_status_code)


def get_server_root() -> str:
    """
    Returns the URL root where this server instance is hosted. This could be something like this:
    127.0.0.1:5000/
    127.0.0.1:5000/swe_server/
    domain.org/swe/
    ...
    """
    return current_app.config["SERVER_HOSTNAME"] + current_app.config["SERVER_PATH"]
