#include <iostream>
#include "openvdb-points-unity.h"

int main() {
    openvdbInitialize();
    openvdbUninitialize();
    std::cout << "Test Successful" << std::endl;
    return 0;
}
