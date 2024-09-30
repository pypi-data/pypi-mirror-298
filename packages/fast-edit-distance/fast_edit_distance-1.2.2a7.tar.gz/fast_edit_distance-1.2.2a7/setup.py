from setuptools import setup
from Cython.Build import cythonize
import setuptools_scm

version = setuptools_scm.get_version()
setup(
    ext_modules=cythonize("src/fast_edit_distance.pyx"),
    version=version
)
