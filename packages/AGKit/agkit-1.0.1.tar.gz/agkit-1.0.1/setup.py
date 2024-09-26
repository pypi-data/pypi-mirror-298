# -*- coding: utf-8 -*-

import re
import requests
import setuptools
from bs4 import BeautifulSoup


class Uploader:
    def __init__(self, package_name, is_test):
        self.package_name = package_name
        self.is_test = is_test
        if is_test:
            self.url = f"https://test.pypi.org/project/{self.package_name}/"
        else:
            self.url = f"https://pypi.org/project/{self.package_name}/"

    def GetVersion(self):
        # 从官网获取版本号
        response = requests.get(self.url)
        if response.status_code == 200:
            print("获取官网信息成功")
            soup = BeautifulSoup(response.content, "html.parser")
            latest_version = soup.select_one(".release__version").text.strip()
            return str(latest_version)
        else:
            print("获取官网信息失败")
            return "1.0.0"

    def GetNewVersion(self):
        # 从版本号字符串中提取三个数字并将它们转换为整数类型
        version = self.GetVersion()
        print("旧版本号：" + version)
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", version)
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
        print("新版本号：" + new_version_str)
        return new_version_str

    def Start(self):
        with open("README.md", "r", encoding="utf8") as fh:
            long_description = fh.read()
        with open('requirements.txt') as f:
            required = f.read().splitlines()

        setuptools.setup(
            name=self.package_name,
            version=self.GetNewVersion(),
            author="LiZhun",  # 作者名称
            author_email="914525405@qq.com",  # 作者邮箱
            description="Python开发工具库",  # 库描述
            long_description=long_description,
            long_description_content_type="text/markdown",
            url=self.url,  # 库的官方地址
            packages=setuptools.find_packages(),
            data_files=["requirements.txt"],  # 库依赖的其他库
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
            python_requires='>=3.6',
            install_requires=required,
        )

if __name__ == '__main__':
    uploader = Uploader("AGKit", False)
    uploader.Start()
