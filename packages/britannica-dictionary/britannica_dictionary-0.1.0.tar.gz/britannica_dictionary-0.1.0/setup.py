from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="britannica-dictionary",
    version="0.1.0",
    author="Esualew Chekol",
    author_email="esubalewchekol6@gmail.com",
    description="A Python package to crawl Britannica Dictionary for word entries, definitions, and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Esubaalew/Dictionary",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
