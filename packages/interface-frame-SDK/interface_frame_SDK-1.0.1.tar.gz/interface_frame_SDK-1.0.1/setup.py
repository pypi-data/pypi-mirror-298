# -*- coding: UTF-8 -*-
# @Time : 2023/7/6
# @Author : chengwenping2

from setuptools import setup
import interface_frame


def readme():
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="interface_frame_SDK",
    version=interface_frame.__version__[0],
    description="接口自动化框架",
    long_description=readme(),
    keywords="自动化",
    packages=[
        "interface_frame",
        "interface_frame/log",
    ],
    package_data={
        "interface_frame": [
            "templates/*.*",
            "skeleton/*",
            "skeleton/*.*",
            "skeleton/**/*.*",
            "skeleton/**/**/*.*",
            "skeleton/**/**/**/*.*",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        # "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
        # 许可证信息
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT License",
    include_package_data=True,
    author="chengwenping",
    author_email="18108278175@163.cn",
    install_requires=[
        "jsonpath~=0.82",
        "PyMySQL~=1.0.3",
        "jmespath~=0.10.0",
        "Requests~=2.31.0",
        "setuptools~=56.0.0",
        "psutil~=5.9.5",
        "XMind~=1.2.0",
        "APScheduler~=3.10.1",
        "pyjson5~=1.6.2",
        "json5~=0.9.14",
        "Faker~=18.10.1",
        "Jinja2~=3.1.2",
        "psycopg2~=2.9.6",
        "termcolor~=2.3.0",
        "openpyxl~=3.1.2",
        "urllib3~=1.26.16",
        "beautifulsoup4~=4.12.2",
        "sshtunnel~=0.4.0",
    ],
    extras_require={
      'GUI': ["PyQt6~=6.2.0"]
    },
    zip_safe=False,
)
