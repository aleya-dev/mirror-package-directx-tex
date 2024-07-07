from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import rmdir
import os


required_conan_version = ">=2.0"


class DirectXTexConan(ConanFile):
    name = "directx-tex"
    version = "jun2024"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaConanBase"

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    requires = ["libpng/1.6.40@aleya/public",
                "libjpeg-turbo/3.0.1@aleya/public",
                "directx-math/feb2024b@aleya/public",
                "directx-headers/1.613.0@aleya/public"]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BUILD_TOOLS"] = False
        tc.variables["BUILD_SAMPLE"] = False
        tc.variables["BUILD_DX11"] = False
        tc.variables["BUILD_DX12"] = False
        tc.variables["BUILD_XBOX_EXTS_XBOXONE"] = False
        tc.variables["BUILD_XBOX_EXTS_SCARLETT"] = False
        tc.variables["ENABLE_LIBJPEG_SUPPORT"] = True
        tc.variables["ENABLE_LIBPNG_SUPPORT"] = True
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "directx-tex")

        self.cpp_info.components["libdirectx-tex"].libs = ["DirectXTex"]
        self.cpp_info.components["libdirectx-tex"].set_property("cmake_target_name", "Microsoft::DirectXTex")
        self.cpp_info.components["libdirectx-tex"].requires = \
            ["libpng::libpng", "libjpeg-turbo::jpeg8", "directx-headers::directx-headers", "directx-math::directxmath"]
