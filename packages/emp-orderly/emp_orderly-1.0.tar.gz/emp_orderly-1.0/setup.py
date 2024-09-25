import os

from setuptools import setup

def get_version():
    return os.getenv("PACKAGE_VERSION", "0.0.0")


setup(
    name='emp-orderly',
    version=get_version(),
    python_requires='>=3.10, <3.13',
    install_requires=[
        'base58==2.1.1',
        "bokeh==3.4.1",
        'cryptography==42.0.5',
        'eth-rpc-py==0.1.8post6',
        'eth-typing==4.1.0',
        'eth-utils==4.1.0',
        'httpx==0.27.0',
        'pandas==2.2.2',
        'pydantic>=2.7.0',
        'python-dotenv==1.0.1',
        'requests==2.31.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    package_data={
        '': ['*.js'],  # Include all JavaScript files
    },
    include_package_data=True,  # Ensure package_data is included
)
