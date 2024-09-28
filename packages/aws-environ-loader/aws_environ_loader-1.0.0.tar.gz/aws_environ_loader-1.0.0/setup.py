from setuptools import find_packages, setup

setup(
    name="aws_environ_loader",
    version="1.0.0",  # Initial version
    author="Jarklee",
    author_email="quantv@vikoisoft.com",
    description="A package that load environment variables from AWS or system environment variables",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/jarklee/aws_environ",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
    install_requires=[
        "boto3",
        "python-dotenv",
    ],
)
