from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pii_scanner',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'unstructured==0.15.5',
        'presidio-analyzer==2.2.32',
        # add other dependencies here
    ],
    tests_require=['unittest'],
    description='A library for scanning Personally Identifiable Information (PII).',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specifies that the README is in Markdown format
    author='Ankit Gupta',  # Replace with your name
    author_email='devankitgupta01@gmail.com',  # Replace with your email
    url='https://github.com/devankit01/pii_scanner',  # Replace with your GitHub repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # or whichever license you're using
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Specify the minimum Python version required
)
