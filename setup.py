#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()

requirements = [
    'Flask>=0.10',
    'Jinja2>=2.4',
    'PyYAML>=3.11',
    'fake-factory>=0.5.2',
    'pathlib==1.0.1'
]

setup(
    name='Mockdown',
    version='0.1.0-dev',
    description='HTML mockups simplified!',
    long_description=readme,
    author='Anand Chitipothu',
    author_email='anandology@gmail.com',
    url='https://github.com/anandology/mockdown',
    packages=[
        'mockdown',
    ],
    package_dir={'mockdown':
                 'mockdown'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='mockdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points='''
        [console_scripts]
        mockdown=mockdown:main
    '''
)
