# setup.py

from setuptools import setup, find_packages

setup(
    name="dj_multihash",
    version="0.2",
    packages=find_packages(),
    install_requires=[],  # Ajoute ici les dépendances
    author="DJSTUDIO",
    description="library that combiens multiple technics of hash in only one function",
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
