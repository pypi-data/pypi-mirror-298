# -*- coding: utf-8 -*-

import re
import requests
import setuptools
from bs4 import BeautifulSoup

package_name = "AGKit"


def curr_version():
    # 从官网获取版本号
    url = f"https://pypi.org/project/{package_name}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        latest_version = soup.select_one(".release__version").text.strip()
        print(latest_version)
        return str(latest_version)
    else:
        return "0.0.1"


def get_version():
    # 从版本号字符串中提取三个数字并将它们转换为整数类型
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", curr_version())
    major = int(match.group(1))
    minor = int(match.group(2))
    patch = int(match.group(3))

    # 对三个数字进行加一操作
    patch += 1
    if patch > 9:
        patch = 0
        minor += 1
        if minor > 9:
            minor = 0
            major += 1
    new_version_str = f"{major}.{minor}.{patch}"
    print(new_version_str)
    return new_version_str


def upload():
    with open("README.md", "r", encoding="utf8") as fh:
        long_description = fh.read()
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    setuptools.setup(
        name=package_name,
        version=get_version(),
        author="LiZhun",  # 作者名称
        author_email="914525405@qq.com", # 作者邮箱
        description="Python开发工具库", # 库描述
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=f"https://pypi.org/project/{package_name}/", # 库的官方地址
        packages=setuptools.find_packages(),
        data_files=["requirements.txt"], # yourtools库依赖的其他库
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=required,
    )


def write_now_version():
    print("当前版本：", get_version())
    with open("VERSION", "w") as version_f:
        version_f.write(get_version())


def main():
    try:
        upload()
        print("上传成功，当前版本：", curr_version())
    except Exception as e:
        raise Exception("上传包失败，异常信息：", e)


if __name__ == '__main__':
    main()

