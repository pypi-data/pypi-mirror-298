from setuptools import setup, find_packages

setup(
    name="jynxzzz",
    version="0.4",
    description="A collection of custom functions for data analysis",
    author="Xingnan Zhou",
    author_email="zhouxingnan2016@gmail.com",
    packages=find_packages(),
    install_requires=[
        "torch>=1.0",
        "matplotlib>=3.0",
    ],
)
