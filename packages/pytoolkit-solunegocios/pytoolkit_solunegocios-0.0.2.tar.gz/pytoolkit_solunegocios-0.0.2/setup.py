# setup.py

from setuptools import setup, find_packages

setup(
    name="pytoolkit-solunegocios",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "msal",  # Microsoft Authentication Library
        "requests"  # Para hacer peticiones HTTP
    ],
    author="Cristian Pavez",
    author_email="cpavezm@soluciones.cl",
    description="",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
