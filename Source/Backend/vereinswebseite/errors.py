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
