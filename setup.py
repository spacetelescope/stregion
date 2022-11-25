import sys
import warnings

from setuptools import setup, Extension

# check if cython or pyrex is available.
pyrex_impls = 'Cython.Distutils.build_ext', 'Pyrex.Distutils.build_ext'
for pyrex_impl in pyrex_impls:
    try:
        # from (pyrex_impl) import build_ext
        build_ext = __import__(pyrex_impl, fromlist=['build_ext']).build_ext
        break
    except ImportError:
        pass
have_pyrex = 'build_ext' in globals()

if have_pyrex:
    cmdclass = {'build_ext': build_ext}
    PYREX_SOURCE = "src/_region_filter.pyx"
else:
    cmdclass = {}
    PYREX_SOURCE = "src/_region_filter.c"

# If you don't want to build filtering module (which requires a C compiler), set it to False
WITH_FILTER = True

arguments = dict()

if WITH_FILTER:
    try:
        import numpy
    except ImportError:
        warnings.warn(
            "numpy must be installed to build the filtering module.")
        sys.exit(1)

    try:
        numpy_include = numpy.get_include()
    except AttributeError:
        numpy_include = numpy.get_numpy_include()

    if len(cmdclass) > 0:
        arguments["cmdclass"] = cmdclass

    arguments["ext_modules"] = [
        Extension(
            "stregion._region_filter",
            [PYREX_SOURCE],
            include_dirs=[
                './src',
                numpy_include,
            ],
            libraries=[],
        )
    ]

setup(**arguments)
