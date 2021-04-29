from http import HTTPStatus

from flask import request

success_response = {"success": True}


def get_int_from_request(key):
    value_str = request.args.get(key, default=None)
    if value_str is None:
        return None

    try:
        return int(value_str)
    except:
        return None


def generate_success(return_values, status=HTTPStatus.OK):
    response = success_response

    for key in return_values:
        response[key] = return_values[key]

    return response, status


def generate_error(error_title: str, http_status_code: int, error_details=None):
    return {
               "errors": [
                   {
                       "title": error_title,
                       "status": http_status_code,
                   }
               ],
               "success": False
           }, http_status_code

