# setup.py
from setuptools import find_packages, setup

setup(
    name="codealchemy",
    version="1.1",
    packages=find_packages(),
    install_requires=[],
    author="GirishCodeAlchemy",
    author_email="girishcodealchemy@gmail.com",
    description="A package with decorators to capture execution time and create log groups for functions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/girishcodealchemy/codealchemy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
