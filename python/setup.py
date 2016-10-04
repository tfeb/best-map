from setuptools import setup, find_packages

setup(name="bestmap",
      version="0.0",
      description="Compute the mapping between two arrays with the shortest distance",
      author="Tim Bradshaw",
      author_email="tim.bradshaw@metoffice.gov.uk",
      url="http://www.metoffice.gov.uk/",
      packages=find_packages("lib"),
      package_dir={"": "lib"},
      scripts=(),
      test_suite='nose.collector',
      install_requires=("numpy",),
      zip_safe=True)
