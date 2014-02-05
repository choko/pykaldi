#!/usr/bin/env python
# encoding: utf-8
# On Windows, you need to execute:
# set VS90COMNTOOLS=%VS100COMNTOOLS%
# python setup.py build_ext --compiler=msvc
from setuptools import setup
from sys import version_info as python_version
from os import path
from distutils.extension import Extension
from Cython.Distutils import build_ext
from subprocess import check_output

STATIC = True

install_requires = []
if python_version < (2, 7):
    new_27 = ['ordereddict', 'argparse']
    install_requires.extend(new_27)


ext_modules = []

# pykaldi library compilation (static|dynamic)
if STATIC:
    # STATIC TODO extract linking parameters from Makefile
    library_dirs, libraries = [], []
    extra_objects = ['../dec-wrap/dec-wrap.a', '../decoder/kaldi-decoder.a',
                     '../thread/kaldi-thread.a', '../lat/kaldi-lat.a',
                     '../hmm/kaldi-hmm.a', '../transform/kaldi-transform.a',
                     '../gmm/kaldi-gmm.a', '../fstext/kaldi-fstext.a',
                     '../tree/kaldi-tree.a', '../matrix/kaldi-matrix.a',
                     '../feat/kaldi-feat.a', '../util/kaldi-util.a',
                     '../base/kaldi-base.a', ]
# ATLASLIBS = /usr/lib/atlas-base/libatlas.so.3gf
# /usr/lib/atlas-base/libf77blas.so.3gf
# /usr/lib/atlas-base/libcblas.so.3gf
# /usr/lib/atlas-base/liblapack_atlas.so.3gf
    ATLASLIBS = ['/usr/lib/atlas-base/libatlas.so.3gf', '/usr/lib/atlas-base/libf77blas.so.3gf',
                 '/usr/lib/atlas-base/libcblas.so.3gf', '/usr/lib/atlas-base/liblapack_atlas.so.3gf']

    # ATLASLIBS = ['atlas', 'f77blas',
    #              'cblas', 'lapack_atlas']
    ATLASINC = '/ha/work/people/oplatek/kaldi/tools/ATLAS/include'
    libraries = ['fst']
    libraries.extend(ATLASLIBS)
    print libraries
    ext_modules.append(Extension('pykaldi.decoders',
                                 language='c++',
                                 include_dirs=['..', 'pyfst', ATLASINC],
                                 library_dirs=['/ha/work/people/oplatek/kaldi/tools/openfst/lib',
                                               '/usr/lib/atlas-base'],
                                 libraries=libraries,
                                 extra_objects=extra_objects,
                                 extra_compile_args=['-fPIC', '-DKALDI_DOUBLEPRECISION=0',
                                                     '-DHAVE_POSIX_MEMALIGN', '-Wno-sign-compare', '-Wno-unused-local-typedefs',
                                                     '-Winit-self', '-DHAVE_EXECINFO_H=1', '-DHAVE_CXXABI_H',
                                                     '-DHAVE_ATLAS'],
                                 sources=['pykaldi/decoders.pyx', ],
                                 ))
else:
    # DYNAMIC
    library_dirs = ['.', ]
    libraries = ['pykaldi', ]
    extra_objects = []
    ext_modules.append(Extension('pykaldi.decoders',
                                 language='c++',
                                 include_dirs=['..', 'pyfst', ],
                                 library_dirs=library_dirs,
                                 libraries=libraries,
                                 extra_objects=extra_objects,
                                 sources=['pykaldi/decoders.pyx', ],
                                 ))


long_description = open(path.join(path.dirname(__file__), 'README.rst')).read()

try:
    # In order to find out the pykaldi version from installed package at runtime use:
    # import pgk_resources as pkg; pkg.get_distribution('pykaldi')
    git_version = check_output(['git', 'rev-parse', 'HEAD'])
except:
    git_version = 'Unknown Git version'
    print git_version

setup(
    name='pykaldi',
    packages=['pykaldi', 'pykaldi.binutils'],
    package_data={'pykaldi': ['libpykaldi.so', 'test_shortest.txt']},
    include_package_data=True,
    cmdclass={'build_ext': build_ext},
    version='0.1-' + git_version,
    install_requires=install_requires,
    setup_requires=['cython>=0.19.1'],
    ext_modules=ext_modules,
    test_suite="nose.collector",
    tests_require=['nose>=1.0', 'pykaldi'],
    # entry_points={
    #     'console_scripts': [
    #         'live_demo=pykaldi.binutils.main',
    #     ],
    # },
    author='Ondrej Platek',
    author_email='ondrej.platek@seznam.cz',
    url='https://github.com/DSG-UFAL/pykaldi',
    license='Apache, Version 2.0',
    keywords='Kaldi speech recognition Python bindings',
    description='C++/Python wrapper for Kaldi decoders',
    long_description=long_description,
    classifiers='''
        Programming Language :: Python :: 2
        License :: OSI Approved :: Apache License, Version 2
        Operating System :: POSIX :: Linux
        Intended Audiance :: Speech Recognition scientist
        Intended Audiance :: Students
        Environment :: Console
        '''.strip().splitlines(),
)
