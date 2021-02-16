# Feb 8, 2021

from setuptools import setup, find_packages
import io
from os import path
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    # print(long_description)
setup(
    name='scrapingtools',
    version="1.1.5",
    author='Yoshio Yamauchi 山内義生 == SPARKLE',
    author_email='sparkle.official.01@gmail.com',
    long_description_content_type="text/markdown",
    description="tools for anonymous web scraping with tor and multiprocessing",
    long_description=long_description,
    url="https://github.com/YoshioYamauchi/scrapingtools"
    license='MIT',
    platforms=['any'],
    keywords='pandas, finance, pandas datareader',
    packages=find_packages(include=["scrapingtools", "scrapingtools.*"]),
    python_requires=">=3.6",
    # install_requires=["stem>="]
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)


# python3 setup.py sdist
# twine upload dist/*
