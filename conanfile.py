from conans import ConanFile, CMake, tools
import os

class LLVMConan(ConanFile):
    name = "llvm"
    version = "4.0.1"
    description = "llvm"
    topics = ("conan", "llvm")
    author = "Huang-Ming Huang <huangh@objectcomputing.com>"
    license = "MIT"
    exports = ["LICENSE"]
    settings = "os", "compiler", "arch"

    generators = "cmake"
    no_copy_source = True
    build_requires = 'zlib/1.2.11@conan/stable'

    def source(self):
        self.run("git clone --depth 1 --single-branch --branch release_40 https://github.com/llvm-mirror/llvm.git")

        tools.replace_in_file("llvm/CMakeLists.txt", 'C CXX ASM)','''C CXX ASM)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        tools.replace_in_file("llvm/include/llvm/ExecutionEngine/Orc/OrcRemoteTargetClient.h", "Expected<std::vector<char>>", "Expected<std::vector<uint8_t>>")
        # link zlib statically to ensure package distributability
        tools.replace_in_file("llvm/lib/Support/CMakeLists.txt", 'set(system_libs ${system_libs} z)', 
                              '# set(system_libs ${system_libs} z)')
        tools.replace_in_file("llvm/lib/Support/CMakeLists.txt",'set_property(TARGET LLVMSupport PROPERTY LLVM_SYSTEM_LIBS "${system_libs}")', 
                              '''set_property(TARGET LLVMSupport PROPERTY LLVM_SYSTEM_LIBS "${{system_libs}}")
target_include_directories(LLVMSupport PRIVATE {0}/include)
target_link_libraries(LLVMSupport PRIVATE {0}/lib/libz.a)'''.format(self.deps_cpp_info['zlib'].rootpath))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_BUILD_TYPE"]="Release"
        cmake.definitions['LLVM_ENABLE_RTTI']="ON"
        cmake.definitions['LLVM_ENABLE_TERMINFO']="OFF"
        cmake.configure(source_dir=os.path.join(self.source_folder,"llvm"))
        return cmake

    def build(self):
        self._configure_cmake().build()

    def package(self):
        self.copy(pattern="LICENSE.TXT", dst="licenses", src="llvm")
        cmake = CMake(self)
        cmake.install()
        try:
            # For some reason, LLVMExports.cmake always contains the reference to libz.a. We already link it statically, remove it if it exists. 
            tools.replace_in_file("%s/lib/cmake/llvm/LLVMExports.cmake" % self.package_folder , ";%s/lib/libz.a" % self.deps_cpp_info['zlib'].rootpath, "")
        except:
            pass

    def package_info(self):
        pass

    def conan_info(self):
        self.info.settings.build_type = None
