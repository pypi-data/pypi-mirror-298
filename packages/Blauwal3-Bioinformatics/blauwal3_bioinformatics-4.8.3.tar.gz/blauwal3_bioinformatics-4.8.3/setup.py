#!/usr/bin/env python
from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        version='4.8.3',  # 使用固定版本号
        setup_requires=[
            'setuptools>=40.0',  # 只需要 setuptools 的最低版本要求
        ],
        install_requires=[
            'Blauwal3>=3.38.0',
            'Blauwal3-widget-base',
            'scipy>=1.5.0',
            'pyclipper>=1.2.0',
            'point-annotator~=2.0',
            'requests',
            'requests-cache>=0.8.0',
            'resdk>=20.0.0',
            'genesis-pyapi',
            'single_sample_gsea>=0.2.0',
            'numpy',
            'serverfiles',
        ],
        extras_require={
            'doc': [
                'sphinx',
                'recommonmark',
                'sphinx_rtd_theme',
                'docutils<0.17',
            ],
            'test': [
                'flake8',
                'flake8-comprehensions',
                'flake8-black',
                'pep8-naming',
                'isort',
                'pre-commit',
                'pytest',
                'coverage',
                'codecov',
            ],
        },
        packages=find_packages(),
        include_package_data=True,
    )
