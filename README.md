## Package Status

| Bintray | Windows | Linux & macOS |
|:--------:|:---------:|:-----------------:|
|[![Download](https://api.bintray.com/packages/huangminghuang/conan/llvm%3Ahuangminghuang/images/download.svg) ](https://bintray.com/huangminghuang/conan/llvm%3Ahuangminghuang/_latestVersion)|[![Build status](https://ci.appveyor.com/api/projects/status/github/huangminghuang/conan-llvm?svg=true)](https://ci.appveyor.com/project/huangminghuang/conan-llvm)|[![Build Status](https://travis-ci.com/huangminghuang/conan-llvm.svg?branch=master)](https://travis-ci.com/huangminghuang/conan-llvm)|


## Basic setup

    $ conan remote add huang https://api.bintray.com/conan/huangminghuang/conan 
    $ conan install llvm/4.0.0@huangminghuang/stable
    
## Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    llvm/4.0.0@huangminghuang/stable
    
    [generators]
    cmake_paths

Complete the installation of requirements for your project running:

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.cmake* with all the 
paths and variables that you need to link with your dependencies.

## CMake setup

This recipe does not support the conan *package_info*, you can only use the cmake config provided by LLVM.

*CMakeLists.txt*

    set(CMAKE_CXX_STANDARD 11)
    find_package(LLVM REQUIRED)
    include_directories(${LLVM_INCLUDE_DIRS})
    add_definitions(${LLVM_DEFINITIONS})

    # Now build our tools
    add_executable(example example.cpp)

    # Find the libraries that correspond to the LLVM components
    # that we wish to use
    llvm_map_components_to_libnames(llvm_libs support core irreader mcjit)

    # Link against LLVM libraries
    target_link_libraries(example ${llvm_libs})
 

The *conan_paths.cmake* can be specified as a toolchain file when invoking cmake:

```bash
$ mkdir build && cd build
$ conan install ..
$ cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -DCMAKE_BUILD_TYPE=Release
$ cmake --build .
```




