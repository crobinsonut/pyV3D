import sys
import os
import setuptools
import shutil

try:
    from numpy.distutils.core import setup
    from numpy.distutils.misc_util import Configuration, msvc_runtime_library, get_build_architecture
except ImportError:
    print 'numpy was not found.  Aborting build'
    sys.exit(-1)

try:
    from numpy.distutils.mingw32ccompiler import find_dll
except:
    def find_dll(dll_name):

        arch = {'AMD64' : 'amd64',
                'Intel' : 'x86'}[get_build_architecture()]

        def _find_dll_in_winsxs(dll_name):
            # Walk through the WinSxS directory to find the dll.
            winsxs_path = os.path.join(os.environ['WINDIR'], 'winsxs')
            if not os.path.exists(winsxs_path):
                return None
            for root, dirs, files in os.walk(winsxs_path):
                if dll_name in files and arch in root:
                    return os.path.join(root, dll_name)
            return None

        def _find_dll_in_path(dll_name):
            # First, look in the Python directory, then scan PATH for
            # the given dll name.
            for path in [sys.prefix] + os.environ['PATH'].split(';'):
                filepath = os.path.join(path, dll_name)
                if os.path.exists(filepath):
                    return os.path.abspath(filepath)

        return _find_dll_in_winsxs(dll_name) or _find_dll_in_path(dll_name)

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

def build_win_egg(**kargs):
    msvcr_name = msvc_runtime_library()
    msvcr_dll_name = msvcr_name + '.dll'

    libgcc_name = "libgcc_s_dw2-1"
    libgcc_dll_name = libgcc_name + '.dll'

    pkg_dir = os.path.join("src", "pyV3D")
    msvcr_dst_dll_file = os.path.join(pkg_dir, msvcr_dll_name)
    libgcc_dst_dll_file = os.path.join(pkg_dir, libgcc_dll_name)

    print("Searching for %s to copy into %s" % (msvcr_dll_name, pkg_dir))

    msvcr_dll_file = find_dll(msvcr_dll_name)
    
    if not msvcr_dll_file:
        print "Could not find %s to redistribute with egg. Aborting build." % msvcr_dll_name
        sys.exit(-1)


    print("Copying %s -> %s" % (msvcr_dll_file, msvcr_dst_dll_file))

    shutil.copyfile(msvcr_dll_file, msvcr_dst_dll_file)

    print("Searching for %s to copy into %s" % (libgcc_dll_name, pkg_dir))

    libgcc_dll_file = find_libgcc_dll(libgcc_dll_name)

    if not libgcc_dll_file:
        print "Could not find %s to redistribute with egg. Aborting build."  % libgcc_dll_name
        sys.exit(-1)

    print("Copying %s -> %s" % (libgcc_dll_file, libgcc_dst_dll_file))

    shutil.copyfile(libgcc_dll_file, libgcc_dst_dll_file)

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
        print("Cleaning up %s" % pkg_dir)

        if os.path.isfile(libgcc_dst_dll_file):
            print("Removing %s" % libgcc_dst_dll_file)
            os.remove(libgcc_dst_dll_file)

        if os.path.isfile(msvcr_dst_dll_file):
            print("Removing %s" % msvcr_dst_dll_file)
            os.remove(msvcr_dst_dll_file)

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
        build_win_egg(**kwds)
else:
    setup(**kwds)

