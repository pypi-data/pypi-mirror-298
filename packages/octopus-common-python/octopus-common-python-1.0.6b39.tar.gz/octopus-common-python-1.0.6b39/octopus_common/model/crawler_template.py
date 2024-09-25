import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from octopus_common.decorator.task_type import task_type
from octopus_common.model import crawler
from octopus_common.model.result_detail import DefaultResultDetail


@task_type(990000001)
class TemplateBaiduCrawler(crawler.BaseCrawler):

    def init(self, task):
        pass

    def request(self, task):
        ua = UserAgent()
        return requests.get("https://www.baidu.com", headers={'User-Agent': ua.googlechrome}).text

    def parse(self, task, response):
        title = BeautifulSoup(response, "html.parser").find("title").string
        return DefaultResultDetail(task, title)


if __name__ == '__main__':
    test_task = {}
    local_result_detail = TemplateBaiduCrawler().crawl(test_task)
    print(local_result_detail.__dict__)
