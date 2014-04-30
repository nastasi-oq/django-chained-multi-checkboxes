#!/usr/bin/python
from setuptools import setup, find_packages

from chained_multi_checkboxes import __version__

github_url = 'https://github.com/nastasi-oq/django-chained-multi-checkboxes'
long_desc = open('README.md').read()

setup(
    name='django-chained-multi-checkboxes',
    version='.'.join(str(v) for v in __version__),
    description='Adds chained multi-checkboxes in Django admin',
    long_description=long_desc,
    url=github_url,
    author='Matteo Nastasi',
    author_email='nastasi@alternativeoutput.it',
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    license='Affero GPL v3 License',
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Affero GPL v3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    package_data={'chained_multi_checkboxes' : ['static/admin/js/*.js']},
)

