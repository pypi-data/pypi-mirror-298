from setuptools import setup, find_packages

setup(
    name="generate_barcode",
    version="0.2.0",
    author="DeepTutorials",
    author_email="deeptutorilas.sellpass@gmail.com",
    description="Ein Modul zur Generierung von allen Barcode-Versionen",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/deeptutorials/generate-barcode",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Pillow>=8.0.0",
        "python-barcode>=0.13.1",
    ],
)
