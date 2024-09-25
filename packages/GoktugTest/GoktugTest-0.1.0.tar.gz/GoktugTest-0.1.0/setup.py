import os
from setuptools import setup, find_packages

def read_readme():
    if os.path.exists("README.md"):
        with open("README.md", encoding="utf-8") as f:
            return f.read()
    return ""

setup(
    name="GoktugTest",
    version="0.1.0",
    author="Göktuğ",
    author_email="goktugonal76@gmail.com",
    description="A simple package to greet users",
    long_description=read_readme(),  # Use the safe function
    long_description_content_type="text/markdown",
    #url="https://github.com/GoktugSuvorun/GoktugTest.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "pandas",
    ],
)
