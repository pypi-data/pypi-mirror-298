import argparse
import importlib
import inspect
import os

from octopus_common.model import crawler_template


def main():
    parser = argparse.ArgumentParser(description='生成器')

    parser.add_argument('-c', '--crawler', help='指定爬虫名称', required=True)
    parser.add_argument('-id', '--task_id', help='指定任务 ID', required=True)

    args = parser.parse_args()
    create_crawler(args.crawler, args.task_id)


def to_camel_case(s: str) -> str:
    """将字符串转换为大驼峰格式"""
    return ''.join(word.capitalize() for word in s.split('_'))


def create_crawler(crawler_name: str, task_id: int):
    crawler_name = crawler_name + "_crawler"
    camel_case_name = to_camel_case(crawler_name)

    current_dir = os.getcwd()
    crawler_file_path = os.path.join(current_dir, f"{crawler_name.lower()}.py")

    # 读取模板文件内容
    module_file_path = inspect.getfile(crawler_template)
    with open(module_file_path, 'r', encoding='utf-8') as f:
        crawler_content = f.read()

    # 替换模板中的占位符
    crawler_content = (crawler_content
                       .replace("TemplateBaiduCrawler", camel_case_name)
                       .replace("990000001", str(task_id)))

    # 保存爬虫文件
    with open(crawler_file_path, 'w', encoding='utf-8') as f:
        f.write(crawler_content)

    print(f"爬虫 '{camel_case_name}' 已创建，文件路径: {crawler_file_path}")


if __name__ == '__main__':
    main()
