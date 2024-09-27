from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='splice-replace',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'splice-replace=splice_replace.splice_replace:main',
        ],
    },
    description='A utility to extract, process, and replace text in files based on line and column offsets.',
    author='Ryan Taylor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/saltlakeryan/splice-replace',  # Update with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
