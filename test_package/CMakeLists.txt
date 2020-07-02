cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
add_executable(testPackage main.cpp)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DOPENVDB_ABI_VERSION_NUMBER=7")
target_link_libraries(testPackage ${CONAN_LIBS})
