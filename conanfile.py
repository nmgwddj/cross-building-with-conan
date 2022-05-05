from conans import ConanFile
from conan.tools.cmake import CMake, cmake_layout


class NebaseConan(ConanFile):
    name = "cross-building-with-conan"
    author = "Dylan <2894220@gmail.com>"
    description = "An example of a C++ app cross building with Conan"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "*"

    def requirements(self):
        self.requires("jsoncpp/1.9.5")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
