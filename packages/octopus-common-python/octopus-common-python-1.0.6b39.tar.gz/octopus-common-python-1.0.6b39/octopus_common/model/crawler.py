from abc import abstractmethod

from octopus_common.model.result_detail import ResultDetail


class Crawler:

    @abstractmethod
    def crawl(self, task) -> ResultDetail:
        pass


class BaseCrawler(Crawler):

    def crawl(self, task) -> ResultDetail:
        self.init(task)

        response = self.request(task)

        return self.parse(task, response)

    @abstractmethod
    def init(self, task):
        pass

    @abstractmethod
    def request(self, task):
        pass

    @abstractmethod
    def parse(self, task, response):
        pass
