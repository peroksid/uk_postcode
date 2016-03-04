#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, Command


def read(path, lines=False):
    with open(path) as f:
        if lines:
            return f.readlines()
        else:
            return f.read()


class Gen(Command):
    description = "Generates code for validation and parsing"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from subprocess import check_call
        self.announce('here')
        check_call("pep8 code_generator", shell=True)
        check_call("pyflakes code_generator", shell=True)
        check_call("python -m code_generator", shell=True)
        check_call("pep8 uk_postcode", shell=True)
        check_call("pyflakes uk_postcode", shell=True)
        

config = {
    'description': 'Library and CLI for validating and splitting UK postal code',
    'author': 'Alexander Pugachev',
    'url': '',
    'download_url': '',
    'author_email': 'alexander.pugachev@gmail.com',
    'version': '0.0.1',
    'tests_require': read('requirements/install.txt'),
    'test_suite': 'tests',
    'packages': ['uk_postcode'],
    'scripts': ['bin/uk_postcode'],
    'name': 'uk_postcode',
    'cmdclass': {'gen': Gen}
}

setup(**config)
