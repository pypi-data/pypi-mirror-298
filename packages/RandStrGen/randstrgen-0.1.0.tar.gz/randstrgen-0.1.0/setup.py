# setup.py

from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README file
README = (HERE / "README.md").read_text()

setup(
    name='RandStrGen',  # Your chosen package name
    version='0.1.0',
    description='A simple and flexible random string generator',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Your Name',  # Replace with your name
    author_email='your_email@example.com',  # Replace with your email
    url='https://github.com/yourusername/RandStrGen',  # Replace with your repo URL
    license='MIT',
    packages=find_packages(),
    install_requires=[],  # Add dependencies here if any
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
