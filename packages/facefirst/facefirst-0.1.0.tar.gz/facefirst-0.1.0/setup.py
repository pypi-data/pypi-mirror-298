# setup.py

from setuptools import setup, find_packages

setup(
    name='facefirst',
    version='0.1.0',
    author='shivajiwankhede',
    author_email='shivaji.wankhede@facefirst.com',
    description='A sample Python library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here (e.g., 'numpy', 'requests')
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

