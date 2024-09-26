from setuptools import setup, find_packages

setup(
    name='vector_db_benchmark',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.18.0',
        'psutil>=5.7.0',
        'matplotlib>=3.2.0',
    ],
    author='Sushant Lenka',
    author_email='frostbitecryengine300@gmail.com',
    description='Benchmarking tool for vector databases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/frozenparadox/vector_db_benchmark', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='vector database benchmark milvus numpy',
    python_requires='>=3.6',
)
