from setuptools import find_packages, setup

setup(
    name="WSIPeruDB",
    version="0.3.2",
    packages=find_packages(),
    install_requires=[
        "ipython>=7.34.0",
        "requests>=2.32.3",
        "numpy>=1.26.4",
        "pandas>=2.1.4",
        "matplotlib>=3.7.1",
        "folium>=0.17.0",
        "branca>=0.7.2",
        "scikit-learn>=1.5.2",
        "plotly>=5.24.1",
        "ipywidgets>=7.7.1",
        "geopandas>=1.0.1",
        "openpyxl>=3.1.5",
        "statsmodels>=0.14.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    author="Carol Romero",
    author_email="romeroroldancarol@gmail.com",
    description="Water Stable Isotope Database in Peru",
    long_description="This package allows users to access the Water Stable Isotope Database in Peru. Provides an interactive map for exploring the spatial distribution of all the stations. Additionally, it offers features for technical validation and display temporal series for each station and department across Peru",
    url="https://github.com/karoru23/WSI-PeruDB",
)
