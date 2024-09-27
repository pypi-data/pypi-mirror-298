#!/usr/bin/env python

from setuptools import setup


version = '1.0.0'


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='pyRXG',
    version=version,
    author='Xander Wilcke',
    author_email='w.x.wilcke@vu.nl',
    url='https://wxwilcke.gitlab.io/pyRXG',
    download_url='https://gitlab.com/wxwilcke/pyRXG/-/archive/' + version + '/pyRXG-' + version + '.tar.gz',
    description='Regular Expression Generator and Generaliser',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='GLP3',
    include_package_data=True,
    zip_safe=True,
    install_requires=['numpy'],
    keywords=['regex', 'regular expression', 'text processing', 'generator', 'clustering'],
    packages=['rxg'],
    python_requires='>=3.8',
    test_suite="tests",
)
