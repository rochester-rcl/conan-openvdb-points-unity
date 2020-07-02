## Conan Recipe for [openvdb-points-unity](https://github.com/rochester-rcl/openvdb-points-unity) Plugin ##

### Installation

#### To Build Dependencies 

```bash
git clone https://github.com/rochester-rcl/conan-openvdb-points-unity.git
cd conan-openvdb-points-unity
git submodule init
dependencies/./build_all.sh
```
#### To Build Library

```bash
./build.sh
```

Or

```bash
conan source . -sf src 
conan install . -if build --build missing
conan build . -bf build -sf src
conan export-pkg . OpenVDBPointsUnity/0.0.1@rcldsl/stable -s build_type=Release -sf src -bf build
```

To test the library, run 
```bash
conan test test_package OpenVDBPointsUnity/0.0.1@rcldsl/stable
```

Once the library has been built, go to the directory of your choice and deploy the plugin

```bash
conan install OpenVDBPointsUnity/0.0.1@rcldsl/stable
```

This should result in the creation of a folder titled OpenVDBPointsUnity containing the library and its dependencies. This can be dropped into MyUnityProject/Assets/Plugins folder

