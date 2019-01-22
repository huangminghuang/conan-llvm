import platform, os
from conans.client.run_environment import RunEnvironment

from conans import ConanFile, CMake, tools

class MongocxxdriverTestConan(ConanFile):
    settings = "os", "compiler", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_BUILD_TYPE"]="Release"
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

        
    def test(self):
        os.chdir('bin')
        self.run(".%sexample" % os.sep)
