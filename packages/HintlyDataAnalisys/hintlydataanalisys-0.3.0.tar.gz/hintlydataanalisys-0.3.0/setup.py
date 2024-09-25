from setuptools import setup, find_packages

setup(
    name="HintlyDataAnalisys",  # Nazwa twojej biblioteki
    version="0.3.0",
    author="Franciszek Chmielewski",
    author_email="ferko2610@gmail.com",
    description="Library for mathematical, financial and textual analysis",
    long_description=open("README.md").read(),  # Pobieranie opisu z pliku README
    long_description_content_type="text/markdown",
    keywords='mathematics analysis text data ai',  # Słowa kluczowe dla wyszukiwania
    url="",
    packages=find_packages(),  # Automatyczne znajdowanie pakietów
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
