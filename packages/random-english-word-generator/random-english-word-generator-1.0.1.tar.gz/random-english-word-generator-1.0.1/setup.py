from setuptools import setup, find_packages

setup(
    name='random-english-word-generator',  # Package name
    version='1.0.1',  # Package version
    packages=find_packages(),
    description='A Python package to generate random English words based on word length and count',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Random Generator AI',
    author_email='randomgenerate.ai@gmail.com',
    url='',  # Optional GitHub link
    install_requires=[
        'nltk'  # Add nltk as a required dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
