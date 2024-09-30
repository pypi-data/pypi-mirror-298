from setuptools import setup, find_packages

setup(
    name="nlpflow",
    version="0.0.2",
    author="Konstantinos Giannopoulos",
    author_email="giannopoulosk.data@gmail.com",  
    description="A powerful toolkit for automating NLP workflows.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GiannopoulosK/NLPFlow",
    packages=find_packages(),
     install_requires=[
        'numpy>=1.23.0 ',             
        'spacy>=3.0.0',
        'scikit-learn>=1.0.0',
        'optuna>=4.0.0',
    ],
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha"
    ],
    python_requires='>=3.7',
)