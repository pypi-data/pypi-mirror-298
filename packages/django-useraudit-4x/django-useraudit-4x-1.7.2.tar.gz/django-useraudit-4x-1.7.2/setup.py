#!/usr/bin/env python

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

setup(
    name="django-useraudit-4x",
    version="1.7.2",
    description="Django user audit utilities like logging user log in, disabling access when password expires or user is inactive",
    long_description="Django user audit utilities like logging user log in, disabling access when password expires or user is inactive, this is a fork from django-useraudit, which is not maintained anymore",
    author="Enrique Gimenez",
    author_email="me@enrique.digital",
    url="https://github.com/codesjedi/django-useraudit",
    download_url="https://github.com/codesjedi/django-useraudit/releases",
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    zip_safe=True,
    packages=[
        "useraudit",
        "useraudit.migrations",
    ],
    include_package_date=True,
)
