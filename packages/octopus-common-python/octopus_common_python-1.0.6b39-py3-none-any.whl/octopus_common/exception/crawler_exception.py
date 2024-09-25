from octopus_common.enums.error_code import ErrorCode

from octopus_common.model.result_detail import ResultDetail

from octopus_common.exception.biz_exception import BizException


class CrawlerException(BizException, ResultDetail):
    classType = "com.ctrip.fx.octopus.crawler.CrawlerException"

    def __init__(self, code: int = ErrorCode.BUSINESS_ERROR.code,
                 message: str = ErrorCode.BUSINESS_ERROR.message):
        self.errorCode = code
        self.message = message


class IpBlockException(BizException, ResultDetail):
    classType = "com.ctrip.fx.octopus.crawler.IPBlockException"

    def __init__(self, code: int = ErrorCode.IP_BLOCK_ERROR.code,
                 message: str = ErrorCode.IP_BLOCK_ERROR.message):
        self.errorCode = code
        self.message = message


class NoRetryException(BizException, ResultDetail):
    classType = "com.ctrip.fx.octopus.crawler.NoRetryException"

    def __init__(self):
        self.code = ErrorCode.NO_RETRY_ERROR.code
        self.message = ErrorCode.NO_RETRY_ERROR.message
