from setuptools import setup, find_packages

setup(
    name='PyWomboAPI',
    version='0.1.0',
    author='CodeSyncio',
    description='An unofficial Python library for generating images using Wombo.ai',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://github.com/CodeSyncio/PyWomboAPI',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "requests",
        "lxml",
        "aiohttp",

    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
