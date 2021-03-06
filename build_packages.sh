#/bin/bash
export CONAN_REFERENCE=llvm/4.0.1
export CONAN_USERNAME=huangminghuang
export CONAN_LOGIN_USERNAME=huangminghuang
export CONAN_CHANNEL=stable
export CONAN_UPLOAD=https://api.bintray.com/conan/huangminghuang/conan
export CONAN_ARCHS=x86_64
export CONAN_CMAKE_GENERATOR=Ninja
# export CONAN_PASSWORD=


for version in 6 7 8; do
  export CONAN_GCC_VERSIONS=$version
  export CONAN_DOCKER_IMAGE=conanio/gcc$version
  python ./build.py
done