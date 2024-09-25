# setup.py

from setuptools import setup, find_packages

setup(
    name='my-package-nizarium101',
    version='0.1.0',
    author='Nizar Chaouachi',
    author_email='nizar.chawechy.1618@gmail.com',
    description='A useful Python package',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
