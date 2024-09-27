# setup.py
from setuptools import setup, find_packages

setup(
    name='aitools-schuanhe',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='schuanhe',
    author_email='schuanhe@qq.com',
    description='这是一个方便快捷使用ai的包',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)
