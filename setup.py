from distutils import util
import glob
import os
import pkg_resources
import re
import subprocess
import sys
import sysconfig
import platform

# We must use setuptools, not distutils, because we need to use the
# namespace_packages option for the "google" package.
from setuptools import setup, Extension, find_packages

from distutils.command.build_py import build_py as _build_py
from distutils.command.clean import clean as _clean
from distutils.spawn import find_executable

# Find the Protocol Compiler.
if "PROTOC" in os.environ and os.path.exists(os.environ["PROTOC"]):
    protoc = os.environ["PROTOC"]
elif os.path.exists("../src/protoc"):
    protoc = "../src/protoc"
elif os.path.exists("../src/protoc.exe"):
    protoc = "../src/protoc.exe"
elif os.path.exists("../vsprojects/Debug/protoc.exe"):
    protoc = "../vsprojects/Debug/protoc.exe"
elif os.path.exists("../vsprojects/Release/protoc.exe"):
    protoc = "../vsprojects/Release/protoc.exe"
else:
    protoc = find_executable("protoc")


def GetVersion():
    """Gets the version from google/protobuf/__init__.py

    Do not import google.protobuf.__init__ directly, because an installed
    protobuf library may be loaded instead."""

    global __version__
    __version__ = 0.1
    return __version__


def generate_proto(source, require=True):
    """Invokes the Protocol Compiler to generate a _pb2.py from the given
    .proto file.  Does nothing if the output already exists and is newer than
    the input."""

    if not require and not os.path.exists(source):
        return
    module_path = __module__

    output = source.replace(".proto", "_pb2.py")

    if not os.path.exists(output) or (
        os.path.exists(source) and os.path.getmtime(source) > os.path.getmtime(output)
    ):
        print("Generating %s..." % output)

        if not os.path.exists(source):
            sys.stderr.write("Can't find required file: %s\n" % source)
            sys.exit(-1)

        if protoc is None:
            sys.stderr.write(
                "protoc is not installed.  Please compile it "
                "or install the binary package.\n"
            )
            sys.exit(-1)

        protoc_command = [protoc, "-I ada/proto", "-I.", "--python_out=.", source]
        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)


class clean(_clean):
    def run(self):
        # Delete generated files in the code tree.
        for (dirpath, dirnames, filenames) in os.walk("."):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if filepath.endswith("_pb2.py") or filepath.endswith(".pyc"):
                    os.remove(filepath)
        # _clean is an old-style class, so super() doesn't work.
        _clean.run(self)


class build_py(_build_py):
    def run(self):
        # Generate necessary .proto file if it doesn't exist.
        generate_proto("src/proto/ada.proto", False)
        generate_proto("src/proto/graph.proto", False)

        # _build_py is an old-style class, so super() doesn't work.
        _build_py.run(self)


def get_option_from_sys_argv(option_str):
    if option_str in sys.argv:
        sys.argv.remove(option_str)
        return True
    return False


if __name__ == "__main__":
    ext_module_list = []
    warnings_as_errors = "--warnings_as_errors"
    if get_option_from_sys_argv("--cpp_implementation"):
        # Link libprotobuf.a and libprotobuf-lite.a statically with the
        # extension. Note that those libraries have to be compiled with
        # -fPIC for this to work.
        compile_static_ext = get_option_from_sys_argv("--compile_static_extension")
        libraries = ["protobuf"]

        extra_compile_args = []

        if sys.platform != "win32":
            extra_compile_args.append("-Wno-write-strings")
            extra_compile_args.append("-Wno-invalid-offsetof")
            extra_compile_args.append("-Wno-sign-compare")
            extra_compile_args.append("-Wno-unused-variable")
            extra_compile_args.append("-std=c++11")

        if sys.platform == "darwin":
            extra_compile_args.append("-Wno-shorten-64-to-32")
            extra_compile_args.append("-Wno-deprecated-register")

        # https://developer.apple.com/documentation/xcode_release_notes/xcode_10_release_notes
        # C++ projects must now migrate to libc++ and are recommended to set a
        # deployment target of macOS 10.9 or later, or iOS 7 or later.
        if sys.platform == "darwin":
            mac_target = sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET")
            if mac_target and (
                pkg_resources.parse_version(mac_target)
                < pkg_resources.parse_version("10.9.0")
            ):
                os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
                os.environ["_PYTHON_HOST_PLATFORM"] = re.sub(
                    r"macosx-[0-9]+\.[0-9]+-(.+)",
                    r"macosx-10.9-\1",
                    util.get_platform(),
                )

        # https://github.com/Theano/Theano/issues/4926
        if sys.platform == "win32":
            extra_compile_args.append("-D_hypot=hypot")

        # https://github.com/tpaviot/pythonocc-core/issues/48
        if sys.platform == "win32" and "64 bit" in sys.version:
            extra_compile_args.append("-DMS_WIN64")

        # MSVS default is dymanic
        if sys.platform == "win32":
            extra_compile_args.append("/MT")

        if "clang" in os.popen("$CC --version 2> /dev/null").read():
            extra_compile_args.append("-Wno-shorten-64-to-32")

        if warnings_as_errors in sys.argv:
            extra_compile_args.append("-Werror")
            sys.argv.remove(warnings_as_errors)

        os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "cpp"

    # Keep this list of dependencies in sync with tox.ini.
    install_requires = ["six>=1.9", "setuptools"]
    if sys.version_info <= (2, 7):
        install_requires.append("ordereddict")
        install_requires.append("unittest2")

    setup(
        name="ada",
        version=GetVersion(),
        description="Ada",
        long_description="Ada is a common way of injecting data into visual effects DCC's",
        url="ada.github.io",
        maintainer="dveight",
        maintainer_email="nagle.p@gmail.com",
        license="3-Clause BSD License",
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
        ],
        namespace_packages=["ada"],
        packages=find_packages(exclude=["import_test_package"]),
        cmdclass={"clean": clean, "build_py": build_py},
        install_requires=install_requires,
        ext_modules=ext_module_list,
        scripts=["scripts/ada", "scripts/graph_parser"],
    )
