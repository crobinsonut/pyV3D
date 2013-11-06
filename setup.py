import sys
import os
import setuptools
import shutil

try:
    from numpy.distutils.core import setup
    from numpy.distutils.misc_util import Configuration
except ImportError:
    print 'numpy was not found.  Aborting build'
    sys.exit(-1)

def win_setup(**kargs):
    #alter data to include DLLs
    kargs["package_data"]["pyV3D"].append("libgcc_s_dw2-1.dll")
    kargs["package_data"]["pyV3D"].append("msvcr90.dll")

    #copy DLL's into src/pyV3D
    #Pull msvcr90.dll from obscure Windows folder
    shutil.copyfile("c:/users/crrobin3/Desktop/Portable Python 2.7.5.1/app/msvcr90.dll", "src/pyV3D/msvcr90.dll")

    #Pull libgcc_s_dw2-1.dll from MinGW/bin installation
    shutil.copyfile("C:/users/crrobin3/minGW/bin/libgcc_s_dw2-1.dll", "src/pyV3D/libgcc_s_dw2-1.dll")

    #call setup
    setup(**kargs)

    #cleanup by removing DLL's from src/pyV3D
    os.remove("src/pyV3D/libgcc_s_dw2-1.dll")
    os.remove("src/pyV3D/msvcr90.dll")

srcs = [
    "src/pyV3D/_pyV3D.c",
    "src/pyV3D/wv.c"
]

config = Configuration(name="pyV3D")
config.add_extension("_pyV3D", sources=srcs)

USE_WIN_SETUP = True if sys.platform == "win32" else False

kwds = {'version': '0.4.1',
        'install_requires':['numpy', 'tornado', 'argparse'],
        'author': '',
        'author_email': '',
        'classifiers': ['Intended Audience :: Science/Research',
                        'Topic :: Scientific/Engineering'],
        'description': 'Python webGL based 3D viewer',
        'download_url': '',
        'include_package_data': True,
        'keywords': ['openmdao'],
        'license': 'Apache License, Version 2.0',
        'maintainer': 'Kenneth T. Moore',
        'maintainer_email': 'kenneth.t.moore-1@nasa.gov',
        'package_data': {
               'pyV3D': ['wvclient/*.html', 'wvclient/WebViewer/*.js', 'libgcc_s_dw2-1.dll', 'msvcr90.dll'],
               'pyV3D.test': ['*.stl', '*.bin']
        },
        'package_dir': {'': 'src'},
        'packages': ['pyV3D', 'pyV3D.test'],
        'url': 'https://github.com/OpenMDAO/pyV3D',
        'zip_safe': False,
        'entry_points': {
            'console_scripts': [
               "wvserver=pyV3D.wvserver:main"
            ]
         }
       }

kwds.update(config.todict())

if sys.argv[1] == "bdist_egg":
    if USE_WIN_SETUP:
        win_setup(**kwds)
else:
    setup(**kwds)

