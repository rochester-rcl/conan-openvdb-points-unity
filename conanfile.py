from conans import ConanFile, CMake, tools
import os
from macholib import mach_o, MachO

class OpenvdbpointsunityConan(ConanFile):
    name = "OpenVDBPointsUnity"
    version = "0.0.1"
    license = "MIT"
    author = "Rochester - RCL"
    description = "<Description of Openvdbpointsunity here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    requires = ("OpenVDB/7.0.0@jromphf/stable",)
    default_options = "shared=False"
    generators = "cmake"
    keep_imports = True

    def source(self):
        # TODO deal with versioning later
        self.run("git clone https://github.com/rochester-rcl/openvdb-points-unity.git openvdb-points-unity")
        tools.replace_in_file("{}/openvdb-points-unity/CMakeLists.txt".format(self.source_folder),
                              "PROJECT(openvdb-points-unity)",
                              '''PROJECT(openvdb-points-unity)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["OPENVDB_ROOT"] = self.deps_cpp_info["OpenVDB"].rootpath
        cmake.definitions["OPENVDB_MODULE_DIR"] = "{}/lib".format(self.deps_cpp_info["OpenVDB"].rootpath)
        cmake.configure(source_folder="{}/openvdb-points-unity".format(self.source_folder))
        cmake.build(target="install")
        self.set_osx_rpaths()

    # TODO will make this more organized once prototyping is done
    def package(self):
        self.copy("*.h", dst="include", src="{}/openvdb-points-unity/src".format(self.source_folder))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def imports(self):
        if self.settings.os == 'Macos':
            self.copy("*.dylib", dst="lib", keep_path=False)
            self.set_osx_rpaths()
        if self.settings.os == 'Windows':
            self.copy("*.dll", dst="lib", keep_path=False)
        # need to figure out what windows and linux are (i.e. "Windows")

    @staticmethod
    def list_linked_dependencies(library):

        def get_dependencies(library_path):
            m = MachO.MachO(library_path)
            deps = []
            for header in m.headers:
                for load_command, dylib_command, data in header.commands:
                    if load_command.cmd == mach_o.LC_LOAD_DYLIB:
                        dep = data.decode('ascii')
                        dep = dep.rstrip('\x00')
                        if '/' not in dep:
                            deps.append(dep)
            return deps
        return get_dependencies(library)

    def set_osx_rpaths(self):
        library = "{}/lib/libopenvdb-points-unity.dylib".format(self.build_folder)


        for dirname, dirnames, filenames in os.walk("{}/lib".format(self.build_folder)):
            for filename in filenames:
                pass

    def get_osx_dependencies(self):
        print(self.cpp_info.lib_dirs)

    def package_info(self):
        self.cpp_info.libs = ["openvdb-points-unity"]
