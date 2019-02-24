import codecs
import re
import os
from setuptools import setup, find_packages

# read the version information from nnresample/__init__.py
# This code was taken from https://packaging.python.org/guides/single-sourcing-package-version/
here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(name='nnresample',
      version=find_version("nnresample", "__init__.py"),
      description='A resampling function based on placing the first null on Nyquist (Null-on-Nyquist Resample)',
      url='https://github.com/jthiem/nnresample',
      author='Joachim Thiemann',
      author_email='Joachim.Thiemann@gmail.com',
      license='CC-BY 3.0',
      packages=find_packages(include=['nnresample']),
      install_requires=[
          'scipy>=0.18.0,<2.0.0'  # NumPy is a dependancy of SciPy
      ]
      )
