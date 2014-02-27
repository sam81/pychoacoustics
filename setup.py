#! /usr/bin/env python
from distutils.core import setup
import glob
setup(
    name="pychoacoustics",
    version="0.2.68",
    url="https://bitbucket.org/samuele_c/pychoacoustics",
    author="Samuele Carcagno",
    author_email="sam.carcagno@google.com;",
    description="Python application for running psychoacoustics experiments",
    long_description=\
    """
    pychoacoustics is an application and platform for designing
    and running auditory psychophysics experiments. It provides an easy
    to use graphical user interface with a set of builtin experiments,
    and a set of facilities for data collection. pychoacoustics also
    provides facilities to create your own custom experiments, although
    some Python programming knowledge is necessary.
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
    license="GPL v3",
    requires=['PyQt (>=4.8.4)', 'numpy (>=1.6.1)', 'scipy (>=0.10.1)'],
    packages=["pychoacoustics", "pychoacoustics.default_experiments"],
    scripts = ["pychoacoustics.pyw"],
    package_dir={"pychoacoustics": "pychoacoustics"},
    package_data={'pychoacoustics': ["qrc_resources.py", "doc/_build/latex/*.pdf", "doc/_build/html/*.*",
                                          "doc/_build/html/_modules/*", "doc/_build/html/_sources/*",
                                          "doc/_build/html/_static/*", "doc/_build/html/_images/*",
                                     "doc/_build/html/_templates/*"],},

    
    data_files = [('share/applications', ['pychoacoustics.desktop']),
                  ('share/icons', ['icons/Machovka_Headphones.svg']),
                  ]

    )


