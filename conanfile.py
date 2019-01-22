from conans import ConanFile, CMake, tools
import os

class MongocxxdriverConan(ConanFile):
    name = "llvm"
    version = "4.0"
    description = "llvm"
    topics = ("conan", "llvm")
    author = "Huang-Ming Huang <huangh@objectcomputing.com>"
    license = "MIT"
    exports = ["LICENSE"]
    settings = "os", "compiler", "arch"
    
    generators = "cmake"
    no_copy_source = True
            
    def source(self):
        self.run("git clone --depth 1 --single-branch --branch release_40 https://github.com/llvm-mirror/llvm.git")
       
        tools.replace_in_file("llvm/CMakeLists.txt", 'C CXX ASM)','''C CXX ASM)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        tools.replace_in_file("llvm/include/llvm/ExecutionEngine/Orc/OrcRemoteTargetClient.h", "Expected<std::vector<char>>", "Expected<std::vector<uint8_t>>")
        
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_BUILD_TYPE"]="Release"
        cmake.configure(source_dir=os.path.join(self.source_folder,"llvm"))
        return cmake

    def build(self):
        self._configure_cmake().build()

    def package(self):
        self.copy(pattern="LICENSE.TXT", dst="licenses", src="llvm")
        CMake(self).install()

    def package_info(self):
        pass
