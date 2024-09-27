# setup.py

from setuptools import setup, find_packages

setup(
    name="fx_requi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'fx_requi=fx_requi:main',
        ],
    },
    author="Maxim",
    author_email="firi8228@gmail.com",
    description="Утилита для генерации requirements.txt на основе импортов в проекте",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)