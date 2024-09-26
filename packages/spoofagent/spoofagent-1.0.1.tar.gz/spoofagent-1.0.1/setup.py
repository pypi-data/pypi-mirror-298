from setuptools import setup, find_packages

setup(
    name='spoofagent',
    version='1.0.1',
    packages=find_packages(),
    description='A simple library to generate fake user agents.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='VampXD',
    author_email='bagasmuhammadriszki2@gmail.com',
    url='https://github.com/VampXDH/useragent-generator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)