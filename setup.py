# 此代码仅供娱乐---林
from setuptools import setup, find_packages

setup(
    name='FontMap', #模块名
    version='1.1.5', #版本号
    description='A tool library for generating mapping dictionaries based on font files',#介绍
    long_description=open('README.MD', 'r', encoding='utf-8').read(),#包的详细描述，这里是从README.md文件中读取的内容。
    long_description_content_type='text/markdown',#指定long_description的文本格式，这里是Markdown格式
    author='HuiHui',#作者名
    author_email='2176189493@qq.com',#作者邮箱
    url='https://github.com/HuiHui-lin/FontMap',#模块github地址
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',#指定包需要的Python版本，这里是3.6及以上。
)
