# -*- coding: utf-8 -*-
"""
@File        : setup.py
@Author      : yu wen yang
@Time        : 2022/4/28 2:43 下午
@Description :
"""
import setuptools
install_requires = ['Django >= 3.2', 'PyMySQL>=1.0.2']
setuptools.setup(
    name="django-simple-org-mysql",
    version="0.3.3",
    author="yuwenyang",
    author_email="ywyhpnn@126.com",
    description="组织架构",
    long_description="组织架构",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=[
        "django_simple_departments", "django_simple_departments.*", "manage.py"
    ]),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[],
    python_requires=">=3",
)

