from setuptools import setup, find_packages

setup(
    name='splice-replace',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'splice-replace=splice_replace.splice_replace:main',
        ],
    },
    description='A utility to extract, process, and replace text in files.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/splice-replace',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
