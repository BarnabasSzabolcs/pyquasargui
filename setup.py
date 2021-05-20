import os.path
import pathlib
import re

import pkg_resources
from setuptools import setup, find_packages

# ref. https://github.com/andreyfedoseev/django-static-precompiler/blob/master/setup.py
with open("quasargui/__init__.py") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path, encoding="utf-8").read()


README = read('README.md')

with pathlib.Path('requirements.in').open() as requirements_in:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_in)
    ]

setup(
    name="quasargui",
    packages=find_packages(),
    package_data={'quasargui': ['assets/*']},
    version=version,
    author="Barney Szabolcs",
    author_email="szabolcs.barnabas@gmail.com",
    url="https://github.com/BarnabasSzabolcs/pyquasargui",
    description="Drop-in replacement GUI for Django testing.",
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    keywords=["Python GUI", "python gui", "python", "GUI"],
    python_requires=">=3.5",
    install_requires=install_requires,
)
