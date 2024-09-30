from setuptools import setup, find_packages

setup(
    name='pii_scanner',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'unstructured==0.15.5',
        'presidio-analyzer==2.2.32',
        # add other dependencies here
    ],
    tests_require=['unittest'],
    description='A library for scanning Personally Identifiable Information (PII).',
)
