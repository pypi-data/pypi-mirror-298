# setup.py
from setuptools import setup, find_packages

setup(
    name="dd-ph",                     # 包名称
    version="0.1",                 # 包版本
    packages=find_packages(),      # 自动找到并包含所有包
    install_requires=[],           # 依赖包列表，如有需求请添加
    author="zhouwei",            # 作者名称
    author_email="bnuzhouwei@qq.com",  # 作者邮箱
    description="Many useful helper function",  # 简短描述
    long_description=open('README.md').read(),           # 长描述，从 README 文件中读取
    long_description_content_type='text/markdown',       # 描述格式
    url="https://github.com/bnuzhouwei/py-dd-ph.git",           # 你的包的主页
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',       # Python 版本需求
)