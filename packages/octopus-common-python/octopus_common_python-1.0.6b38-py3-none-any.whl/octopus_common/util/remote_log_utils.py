import inspect

import requests

from octopus_common.constant.constants import INTEGRATION_HOST
from octopus_common.model.log_record import LogRecord
from octopus_common.util.envirement_utils import get_auth

REMOTE_LOG_PATH = "/tripLog/log"


def log(level, message, *tag_pairs):
    stack = inspect.stack()
    # [0]是当前方法, [1]是当前调用者, [2]是上一层调用者
    caller_frame = stack[2]
    filename = caller_frame.filename
    method_name = caller_frame.function
    line_number = caller_frame.lineno
    source = {
        "methodName": method_name,
        "filename": filename,
        "lineNumber": line_number,
        "nativeMethod": False
    }
    log_record = LogRecord(level, source, message, tag_pairs)
    requests.post(INTEGRATION_HOST + REMOTE_LOG_PATH,
                  json=log_record.__dict__,
                  auth=get_auth())


def info(message='', *tag_pairs):
    log(LogRecord.Level.I, message, *tag_pairs)


def warn(message='', *tag_pairs):
    log(LogRecord.Level.W, message, *tag_pairs)


def error(message='', *tag_pairs):
    log(LogRecord.Level.E, message, *tag_pairs)
