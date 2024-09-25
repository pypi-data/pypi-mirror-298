from octopus_common.enums.error_code import ErrorCode


class BizException(Exception):
    errorCode = ErrorCode.BUSINESS_ERROR.code
    message = ErrorCode.BUSINESS_ERROR.message

    def __init__(self, error_code: ErrorCode = ErrorCode.BUSINESS_ERROR):
        self.errorCode = error_code.code
        self.message = error_code.message
