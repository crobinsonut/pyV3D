import sys
import os
import setuptools
import shutil
import log

try:
    from numpy.distutils import log
    from numpy.distutils.core import setup
    from numpy.distutils.misc_util import Configuration, msvc_runtime_library
    from numpy.distutils.mingw32ccompiler import find_dll
except ImportError:
    print 'numpy was not found.  Aborting build'
    sys.exit(-1)

def find_libgcc_dll(dll_name):
    gcc_exe_file = find_gcc_exe()
    gcc_bin_dir = gcc_exe_file.rstrip("gcc.exe")
    
    libgcc_dll_file = os.path.join(gcc_bin_dir, dll_name)

    if os.path.isfile(libgcc_dll_file):
        return libgcc_dll_file

    return ""

def find_gcc_exe():
    def find_gcc_from_CC():
        return os.environ["CC"] if "CC" in os.environ else ""

    def find_gcc_from_path():
        c_compiler_name = "gcc"
        c_compiler_exe_name = "gcc" + '.exe'
        env_var_name = "path"

        paths = os.environ[env_var_name].split(';')
        
        for path in paths:
            c_compiler_exe_file = os.path.join(path, c_compiler_exe_name)
            if os.path.isfile(c_compiler_exe_file):
                return c_compiler_exe_file

        return ""

    return find_gcc_from_CC() or find_gcc_from_path()

def win_setup(**kargs):
    msvcr_name = msvc_runtime_library()
    msvcr_dll_name = msvcr_name + '.dll'

    log.info("Searching for %s to copy into build" % msvcr_dll_name)

    msvcr_dll_file = find_dll(msvcr_dll_name)
    
    if not msvcr_dll_file:
        print "Could not find %s to redistribute with egg. Aborting build." % msvcr_dll_name
        sys.exit(-1)

    log.info("Found %s. Copying from %s to %s" % msvcr_dll_name, msvcr_dll_file, "src/pyV3D/%s" % msvcr_dll_file)
    shutil.copyfile(msvcr_dll_file, "src/pyV3D/%s" % msvcr_dll_name)

    libgcc_name = "libgcc_s_dw2-1"
    libgcc_dll_name = libgcc_name + '.dll'
    libgcc_dll_file = find_libgcc_dll(libgcc_dll_name)

    if not libgcc_dll_file:
        print "Could not find %s to redistribute with egg. Aborting build."  % libgcc_dll_name
        sys.exit(-1)

    log.info("Found %s. Copying from %s to %s" % libgcc_dll_name, msvcr_dll_file, "src/pyV3D/%s" % libgcc_dll_file)
    shutil.copyfile(libgcc_dll_file, "src/pyV3D/libgcc_s_dw2-1.dll")

    #alter data to include DLLs
    kargs["package_data"]["pyV3D"].append(libgcc_dll_name)
    kargs["package_data"]["pyV3D"].append(msvcr_dll_name)

    try:
        #call setup
        setup(**kargs)
    except e:
        raise e
    finally:
        #cleanup by removing DLL's from src/pyV3D
        os.remove("src/pyV3D/%s" % libgcc_dll_name)
        os.remove("src/pyV3D/%s" % msvcr_dll_name)

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
               'pyV3D': ['wvclient/*.html', 'wvclient/WebViewer/*.js'],
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

