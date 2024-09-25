from setuptools import setup, find_packages

with open("README_pypi.md", "r") as f:
    description = f.read()

setup(
    name='view_df',
    version='0.2.7',
    packages=find_packages(),
    install_requires=[
    ],
    author="Arslaan Kola",
    author_email="kolaarslaan[at]gmail[dot]com",
    description="A Python module to display large pandas DataFrames with auto-adjusted column widths in a web browser with filtering capability.",
    long_description=description,
    long_description_content_type="text/markdown",
)