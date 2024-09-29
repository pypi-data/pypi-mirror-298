from setuptools import setup, find_packages

setup(
    name="generate_pfandbon",
    version="0.1.0",
    author="DeeptTutorials",
    author_email="deeptutorials.sellpass@gmail.com",
    description="Ein Modul zur Generierung von Pfandbons mit allen Barcode-Versionen",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pfandbon-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Pillow>=8.0.0",
    ],
)
