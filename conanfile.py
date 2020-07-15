from conans import ConanFile, CMake, tools
import os
from macholib import mach_o, MachO
import subprocess
import shutil

class OpenvdbpointsunityConan(ConanFile):
    name = "OpenVDBPointsUnity"
    version = "0.0.1"
    license = "MIT"
    author = "Rochester - RCL"
    description = "<Description of Openvdbpointsunity here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    requires = ("OpenVDB/7.0.0@rcldsl/stable",)
    default_options = "shared=False"
    generators = "cmake", "cmake_find_package"
    keep_imports = True

    def source(self):
        # TODO deal with versioning later
        self.run(
            "git clone https://github.com/rochester-rcl/openvdb-points-unity.git openvdb-points-unity"
        )
        tools.replace_in_file(
            "{}/openvdb-points-unity/CMakeLists.txt".format(self.source_folder),
            "PROJECT(openvdb-points-unity)",
            """PROJECT(openvdb-points-unity)
                include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                if (APPLE)
                    conan_basic_setup(KEEP_RPATHS)
                else()
                    conan_basic_setup()
                endif()
            """,
        )

    def build(self):
        cmake = CMake(self)
        cmake.definitions["OPENVDB_ROOT"] = self.deps_cpp_info["OpenVDB"].rootpath
        cmake.definitions["OPENVDB_MODULE_DIR"] = "{}/lib".format(
            self.deps_cpp_info["OpenVDB"].rootpath
        )
        cmake.configure(
            source_folder="{}/openvdb-points-unity".format(self.source_folder)
        )
        cmake.build(target="install")

    # TODO will make this more organized once prototyping is done
    def package(self):
        dependencies = [os.path.basename(dep) for dep in self.get_dependencies()]
        if self.settings.os == "Macos":
            self.fix_rpaths()
        for dependency in dependencies:
            self.copy(dependency, src="lib", dst="lib")
        # Fix rpaths on OSX
        self.copy(
            "*.h",
            dst="include",
            src="{}/openvdb-points-unity/src".format(self.source_folder),
        )
        self.copy(
            "*.h",
            dst="include/vendor",
            src="{}/openvdb-points-unity/src/vendor".format(self.source_folder),
        )
        self.copy(
            "*.cpp",
            dst="include/vendor",
            src="{}/openvdb-points-unity/src/vendor".format(self.source_folder),
        )
        self.copy("libopenvdb-points-unity*", src="lib", dst="lib", keep_path=False)

    def deploy(self):
        self.copy("*.dylib", dst="OpenVDBPointsUnity", keep_path=False)
        self.copy("*.so", dst="OpenVDBPointsUnity", keep_path=False)
        self.copy("*.a", dst="OpenVDBPointsUnity", keep_path=False)
        self.copy("*.dll", dst="OpenVDBPointsUnity", keep_path=False)
        src_lib = "OpenVDBPointsUnity/libopenvdb-points-unity.dylib"
        dst_lib = "OpenVDBPointsUnity/libopenvdb-points-unity.bundle"
        cwd = os.getcwd()
        src = os.path.join(cwd, src_lib)
        dst = os.path.join(cwd, dst_lib)
        # Unity won't load a dylib https://answers.unity.com/questions/23615/how-to-make-unity-find-dylib-files.html
        shutil.copy(src, dst)


    def fix_rpaths(self):
        library = "{}/lib/libopenvdb-points-unity.dylib".format(self.build_folder)
        files = list(self.get_dependencies())
        files.append(library)
        basenames = [os.path.basename(f) for f in files] + list(self.list_linked_rpaths(library))
        for f in files:
            for b in basenames:
                cmd = ["install_name_tool", "-change", b, "@loader_path/{}".format(os.path.basename(b)), f]
                subprocess.call(cmd)

    def list_linked_rpaths(self, library):
        return self.list_linked_dependencies(library, True)

    @staticmethod
    def list_linked_dependencies(library, rpaths_only=False):
        def get_dependencies(library_path, rpaths_only):
            m = MachO.MachO(library_path)
            deps = []
            rpaths = []
            for header in m.headers:
                for load_command, dylib_command, data in header.commands:
                    if load_command.cmd == mach_o.LC_LOAD_DYLIB:
                        dep = data.decode("ascii")
                        dep = dep.rstrip("\x00")
                        if "/" not in dep:
                            deps.append("{}/{}".format(os.path.dirname(library), dep))
                        if "@rpath/" in dep:
                            rpaths.append(dep)
                            deps.append("{}/{}".format(os.path.dirname(library), os.path.basename(dep)))
            if len(deps) > 0:
                children = [get_dependencies(dep, False) for dep in deps]
                rpath_children = [get_dependencies(dep, True) for dep in deps]
                all_deps = deps + [dep for child in children for dep in child]
                all_rpaths = rpaths + [rpath for child in rpath_children for rpath in child]
                if rpaths_only:
                    return set(all_rpaths)
                return set(all_deps)
            else:
                return []

        return get_dependencies(library, rpaths_only)

    def get_dependencies(self):
        library = "{}/lib/libopenvdb-points-unity.dylib".format(self.build_folder)
        dependencies = self.list_linked_dependencies(library)
        return dependencies

    def imports(self):
        if self.settings.os == "Macos":
            self.copy("*.dylib", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include", "include/vendor"]
        self.cpp_info.libs = ["openvdb-points-unity"]

