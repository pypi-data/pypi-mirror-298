# setup.py

from setuptools import setup, find_packages

setup(
    name="dj_multihash",
    version="0.52",
    packages=find_packages(),
    install_requires=[],  # Ajoute ici les dépendances
    author="DJSTUDIO",
    description="DJ-MultiHash by DJOPRO_YT",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="",  # Lien vers le dépôt
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
