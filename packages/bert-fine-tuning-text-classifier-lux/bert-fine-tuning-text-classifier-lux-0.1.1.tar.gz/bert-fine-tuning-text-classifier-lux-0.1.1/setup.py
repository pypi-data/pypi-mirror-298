from setuptools import setup, find_packages

# Read the content of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bert-fine-tuning-text-classifier-lux", 
    version="0.1.1",  # version
    author="Mehrdad ALMASI, Demival VASQUES FILHO, Gabor Mihaly TOTH",
    author_email="mehrdad.al.2023@gmail.com, demival.vasques@uni.lu, gabor.toth@uni.lu",
    description="A library that leverages pre-trained BERT models for multilingual text classification (French, German, English, Luxembourgish) with easy-to-use fine-tuning capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mehrdadalmasi2020/bert-fine-tuning-text-classifier-lux", 
    packages=find_packages(),
    install_requires=[
        "transformers>=4.0.0",
        "torch>=1.7.0",
        "pandas>=1.1.0",
        "scikit-learn>=0.24.0",
        "numpy>=1.19.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
