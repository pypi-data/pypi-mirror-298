from setuptools import setup, find_packages

setup(
    name="pepe-toolbox",
    version="0.3.3",
    packages=find_packages(),
    install_requires=[
        "requests==2.32.3",
        "slack_sdk==3.32.0",
        "Pillow",
        "pdf2image",
        "tqdm"
    ],
    author="kinest1997",
    author_email="kinest1997@naver.com",
    description="korean pepe lover",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kinest1997",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
