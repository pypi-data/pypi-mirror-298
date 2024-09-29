from setuptools import setup, find_packages

setup(
    name='SPINEX_Anomaly',
    version='0.1',
    packages=find_packages(),
    description='A Python package for SPINEX Anomaly',
    url='https://arxiv.org/abs/2407.04760',
    long_description=open('Readme/README.md').read(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
    ],
    python_requires='>=3.6',
)
