from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="postman_github_sync",
    version="0.1.0",
    author="Oluwaseyi Ajadi",
    author_email="oluwaseyinexus137@gmail.com",
    description="This script automates the process of setting up GitHub Actions workflows for Postman collections. It supports both GitHub repository integration and local workflow setup, allowing for flexible usage in various scenarios.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/BlazinArtemis/postman_to_github_actions",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
    install_requires=[
        'requests',
        'argparse'
    ],
    entry_points={
        "console_scripts": [
                                "postman_github_sync=postman_github_sync.main:main",
        ],
    },
)
