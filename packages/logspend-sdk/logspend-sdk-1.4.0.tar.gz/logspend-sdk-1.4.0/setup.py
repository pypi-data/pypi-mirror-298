from setuptools import setup, find_packages

setup(
    name="logspend-sdk",
    version="1.4.0",
    packages=find_packages(),
    install_requires=[
        "httpx==0.25.0",
        "langchain>=0.1.0",
    ],
    author="Victor Chima",
    author_email="hello@logspend.com",
    description="SDK for sending LLM application logs to LogSpend",
    keywords="logging LLM LogSpend SDK",
)
