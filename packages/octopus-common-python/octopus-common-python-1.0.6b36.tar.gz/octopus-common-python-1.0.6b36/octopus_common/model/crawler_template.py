import requests
from fake_useragent import UserAgent
from lxml import etree

from octopus_common.decorator.task_type import task_type
from octopus_common.model.crawler import Crawler
from octopus_common.model.result_detail import ResultDetail, DefaultResultDetail


@task_type(999999999)
class TemplateBaiduCrawler(Crawler):
    def crawl(self, task) -> ResultDetail:
        inited = init(task)

        response = request(inited, task)

        return parse(response)


def init(task):
    return {}


def request(inited, task):
    task_detail = task.get("taskDetail")
    ua = UserAgent()
    response = requests.get("https://www.baidu.com", headers={'User-Agent': ua.googlechrome})
    return response.text


def parse(response):
    page = etree.HTML(response)
    title = page.xpath("/html/head/title")[0].text
    return DefaultResultDetail("", title)


if __name__ == '__main__':
    local_result_detail = TemplateBaiduCrawler().crawl({})
    print(local_result_detail.__dict__)
