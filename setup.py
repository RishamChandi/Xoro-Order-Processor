from setuptools import setup, find_packages

setup(
    name="wholefoods-to-xoro",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "openpyxl",
        "beautifulsoup4"
    ],
)