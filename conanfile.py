from conans import ConanFile, CMake, tools
import os


class LibpngConan(ConanFile):
    name = "libpng"
    description = "Keep it short"
    topics = ("conan", "libname", "logging")
    url = "https://github.com/TheMHMoritz3/conan-libpng"
    homepage = "http://www.libpng.org/"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    # Remove following lines if the target lib does not use CMake
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    version = "1.2.54"
    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _downloads_subfolder = "source_subfolder"
    _source_subfolder = "source_subfolder/lpng1254"
    _build_subfolder = "build_subfolder"

    requires = (
        "zlib/1.2.11"
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get("https://sourceforge.net/projects/libpng/files/libpng12/older-releases/1.2.54/lpng1254.zip", destination=self._downloads_subfolder)
#         tools.replace_in_file(self._source_subfolder+"/CMakeLists.txt", "project(libpng C)",
#                               '''project(libpng C)
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup()''')

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # If so, you can just remove the lines below
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
