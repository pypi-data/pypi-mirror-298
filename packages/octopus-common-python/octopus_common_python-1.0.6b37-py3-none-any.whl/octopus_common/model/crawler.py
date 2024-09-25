from abc import abstractmethod

from octopus_common.model.result_detail import ResultDetail


class Crawler:
    @abstractmethod
    def crawl(self, task) -> ResultDetail:
        pass
