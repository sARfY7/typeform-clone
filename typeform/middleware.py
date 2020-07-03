from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import traceback
import inspect
from itertools import islice
import json, requests
from datetime import datetime
from django.conf import settings
import os


class ErrorCapturingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        error_event = create_error_event_dict(request, exception)
        error_event_json = json.dumps(error_event)

        headers = {"X-API-KEY": getattr(settings, "X_API_KEY", None)}
        r = requests.post(
            "http://localhost:8000/store/", data=error_event_json, headers=headers,
        )
        print("response_text:", r.text)
        print("response_status_code:", r.status_code)
        return None


def create_error_event_dict(request, exception):
    error_event = {
        "cookies": request.COOKIES,
        "absolute_uri": request.build_absolute_uri(),
        "error_path": request.path,
        "host": request.get_host(),
        "port": request.get_port(),
        "raw_uri": request.get_raw_uri(),
        "browser_info": request.headers["User-Agent"],
        "request_ip": visitor_ip_address(request),
        "request_method": request.method,
        "request_user": str(request.user),
        "request_header": dict(request.headers),
        "exception_name": type(exception).__name__,
        "exception_message": str(exception),
        "timestamp": str(datetime.now()),
        "middleware_path": os.getcwd(),
        "traceback": get_traceback_frames(exception.__traceback__),
    }
    return error_event


def get_traceback_frames(traceback_object):
    traceback_stack = traceback.walk_tb(traceback_object)
    traceback_frames = []
    for tb in traceback_stack:
        line_no = tb[0].f_lineno
        file_name = tb[0].f_code.co_filename
        local_vars = tb[0].f_locals
        function_name = tb[0].f_code.co_name
        with open(file_name) as lines:
            traceback_frame = []
            end_line = line_no + 5
            if line_no < 4:
                start_line = 0
                for idx, line in enumerate(islice(lines, start_line, end_line)):
                    traceback_frame.append((idx, line))
            else:
                start_line = line_no - 5
                for idx, line in enumerate(islice(lines, start_line, end_line)):
                    traceback_frame.append((idx + line_no - 4, line))

            frame = {
                "frame": traceback_frame,
                "error_line": line_no,
                "error_file": file_name,
                "local_variables": dict_of_objects_to_dict_of_strings(local_vars),
                "function_name": function_name,
            }
            traceback_frames.append(frame)
    return traceback_frames


def dict_of_objects_to_dict_of_strings(object):
    for key, value in object.items():
        object[key] = str(value)

    return object


def visitor_ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
