from octopus_common.exception.biz_exception import BizException
from octopus_common.enums.error_code import ErrorCode


class ResultDetail:

    def __init__(self, class_type):
        if class_type is not None:
            self.classType = class_type


class DefaultResultDetail(ResultDetail):

    def __init__(self, params: str, result: str):
        super().__init__(None)
        self.params = params
        self.result = result


class ArrayListResultDetail(ResultDetail):

    def __init__(self):
        super().__init__(None)
        self.__list = ["com.ctrip.fx.octopus.model.ResultArrayList", []]

    def add(self, item):
        self.__list[1].append(item.__dict__)

    def add_all(self, items: list):
        for item in items:
            self.add(item)

    def get(self, index):
        return self.__list[1][index]

    def remove(self, index):
        self.__list[1].pop(index)

    def size(self):
        return len(self.__list[1])

    def is_empty(self):
        return len(self.__list[1]) == 0

    def clear(self):
        self.__list[1].clear()

    @property
    def __dict__(self):
        if not self.is_empty():
            item = self.__list[1][0]
            if "<" not in self.__list[0] and ">" not in self.__list[0] and "classType" in item:
                self.__list[0] = self.__list[0] + "<{0}>".format(item["classType"])
        return self.__list


class DefaultDBPersistenceResultDetail(ResultDetail):
    def __init__(self, ds_type: str, replace: bool, result: list):
        if ds_type is None or result is None:
            raise BizException(ErrorCode.DEFAULT_DB_PERSISTENCE_RESULT_DETAIL_ERROR)
        super().__init__("com.ctrip.fx.octopus.model.DefaultDBPersistenceResultDetail")
        self.dsType = ds_type
        self.replace = replace
        self.result = result
