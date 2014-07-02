# coding=utf-8
from setuptools import find_packages, setup

VERSION = __import__("logicaldelete").__version__

 
setup(
    name='django-logicaldelete',
    version=VERSION,
    author=u'Angel Velasquez, Agustín Cangiani',
    author_email='angvp@archlinux.org, cangiani@gmail.com',
    url='http://www.routeatlas.com',
    description=u' '.join(__import__('logicaldelete').__doc__.splitlines()).strip(),
    long_description=open("README.rst").read(),
    packages=find_packages(),
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
