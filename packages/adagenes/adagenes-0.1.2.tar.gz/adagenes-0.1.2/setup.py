import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="adagenes",
    version="0.1.2",
    author="Nadine S. Kurz",
    author_email="nadine.kurz@bioinf.med.uni-goettingen.de",
    description="Generic toolkit for processing DNA variation data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.gwdg.de/MedBioinf/mtb/adagenes",
    packages=setuptools.find_packages(),
    install_requires=['requests','liftover','plotly','openpyxl','matplotlib','scikit-learn','blosum','pandas','python-magic','dash','dash-bootstrap-components'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license_files = ('LICENSE.txt',)
)
