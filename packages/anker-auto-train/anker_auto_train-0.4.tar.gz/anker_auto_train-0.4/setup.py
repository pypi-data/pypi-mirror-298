from setuptools import setup, find_packages

setup(
    name="anker_auto_train",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author="taco",
    author_email="taco.wang@example.com",
    description="auto train for anker",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)