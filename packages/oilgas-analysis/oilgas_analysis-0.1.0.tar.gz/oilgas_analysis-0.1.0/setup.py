from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oilgas_analysis",
    version="0.1.0",
    author="Shailesh Tripathi",
    author_email="tripathi_shailesh@ongc.co.in",
    description="A package for oil and gas well analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shailesh2790/oilgas_analysis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
    ],
)