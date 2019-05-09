from conans import ConanFile, CMake, tools


class OpenvdbpointsunityConan(ConanFile):
    name = "OpenVDBPointsUnity"
    version = "0.0.1"
    license = "MIT"
    author = "Rochester - RCL"
    description = "<Description of Openvdbpointsunity here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    requires = ("OpenVDB/6.0.0@jromphf/stable",)
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        # TODO deal with versioning later
        self.run("git clone https://github.com/rochester-rcl/openvdb-points-unity.git openvdb-points-unity")
        tools.replace_in_file("{}/openvdb-points-unity/CMakeLists.txt".format(self.source_folder), "PROJECT(openvdb-points-unity)",
                              '''PROJECT(openvdb-points-unity)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="{}/openvdb-points-unity".format(self.source_folder))
        cmake.build()

    # TODO will make this more organized once prototyping is done
    def package(self):
        self.copy("*.h", dst="include", src="{}/openvdb-points-unity/src".format(self.source_folder))
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["openvdb-points-unity"]

