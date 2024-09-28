from setuptools import setup, find_packages

setup(
    name='PakEngTagger',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    description='A POS tagger for Pakistani English',
    long_description=open('README.txt').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

