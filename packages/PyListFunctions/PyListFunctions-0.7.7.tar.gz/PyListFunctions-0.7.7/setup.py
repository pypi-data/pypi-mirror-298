import os
import codecs
from setuptools import setup, find_packages

try:
    readme = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(str(readme)+str('\\ReadMe.rst'), encoding="utf-8") as rd:
        long_description = rd.read()
except:
    pass

VERSION = '0.7.7'
DESCRIPTION = 'some functions and classes for list（￣︶￣）↗　(and some other kinds of functions)'

setup(
    name="PyListFunctions",
    version=VERSION,
    author="BL_30G(BiliBili现名为:NPC-013)",
    author_email="2842621898@qq.com",
    url="https://space.bilibili.com/1654383134",
    description=DESCRIPTION,
    long_description=str(long_description),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'list', 'clean', 'functions', 'string', 'bool', 'class', 'type'],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14'
    ]
)
