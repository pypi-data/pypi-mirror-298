from setuptools import find_packages, setup


setup(
    name="nlp_preprocess_toolkit_utils",  # Replace with your unique name
    version="0.2.1",
    description="A package for NLP preprocessing and word cloud generation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Rubansendhur",
    author_email="rubansendhur78409@gmail.com",
    url="https://github.com/rubansendhur/nlp_preprocess_toolkit",  # Update GitHub URL if necessary
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "wordcloud",
        "nltk",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
