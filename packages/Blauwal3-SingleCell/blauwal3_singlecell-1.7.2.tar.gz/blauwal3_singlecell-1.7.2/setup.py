#!/usr/bin/env python3
import setuptools


if __name__ == '__main__':
    setuptools.setup(
        version='1.7.2',
        setup_requires=[
            'setuptools-scm',
            'setuptools',
        ],
        install_requires=[
            'Blauwal3>=3.38.0',
            'Blauwal3-bioinformatics',
            'fastdtw==0.3.2',
            'pandas>=0.23',
            'loompy>=2.0.10',
            'xlrd>=2.0.1',
            'openpyxl',
            'anndata>=0.6.21',
            'numpy',
            'scikit-learn',
        ],
        extras_require={
            'doc': ['sphinx', 'recommonmark', 'sphinx_rtd_theme', 'docutils'],
            'package': ['twine', 'wheel'],
            'test': [
                'coverage',
            ],
        },
    )
