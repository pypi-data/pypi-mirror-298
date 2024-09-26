from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='termiline',
    version='1.0',
    packages=find_packages(),
    author="Keyyzan",
    description="A Python library that allows you to center horizontally and vertically (or both) and align right strings in the terminal.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    python_requires='>=3.6',
    license='MIT',
    url='https://github.com/yourusername/termiline',  # Add a URL to your project if applicable
)