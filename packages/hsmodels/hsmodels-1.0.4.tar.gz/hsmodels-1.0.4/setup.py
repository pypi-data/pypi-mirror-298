from setuptools import setup, find_packages

README = 'Refer to the models section of https://hydroshare.github.io/hsclient/'# (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name='hsmodels',
    version='1.0.4',
    packages=find_packages(include=['hsmodels', 'hsmodels.*', 'hsmodels.schemas.*', 'hsmodels.schemas.rdf.*'],
                           exclude=("tests",)),
    install_requires=[
        'rdflib<6.0.0',
        'pydantic==2.7.*',
        'email-validator'
    ],
    url='https://github.com/hydroshare/hsmodels',
    license='MIT',
    author='Scott Black',
    author_email='sblack@cuahsi.org',
    description='Pydantic models for HydroShare metadata',
    python_requires='>=3.9',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],

)
