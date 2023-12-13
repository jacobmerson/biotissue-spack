# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Mdspan(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git      = "git@github.com:kokkos/mdspan.git"
    url = "https://github.com/kokkos/mdspan/archive/refs/tags/mdspan-0.4.0.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions here.
    # version('1.2.4')
    version('0.4.0', sha256='7b89db3c7a9c206c8447499456fdea9c9c1b3a34f58fd0b4c4dd87176b3fe20b')
    version('0.3.0', sha256='275ac02b456a31a5b8c0cb773fca3fe59f6df8a441124dcc1e7a88ef8069f974')
    version('0.2.0', sha256='1ce8e2be0588aa6f2ba34c930b06b892182634d93034071c0157cb78fa294212')
    version('0.1.0', sha256='24c1e4be4870436c6c5e80d38870721b0b6252185b8288d00d8f3491dfba754b')
    
    variant("tests", default=False, description="Enable tests")
    variant("cxx_standard", default=17, description="C++ standard", values=(17,20,23))
    variant("cuda", default=False, description="Enable Cuda support")
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("concepts", default=False, description="Use concepts with mdspan.")

    depends_on("googletest", when="+tests")
    

    def cmake_args(self):
        args = [
            self.define_from_variant("MDSPAN_ENABLE_TESTS", False),
            self.define("MDSPAN_ENABLE_EXAMPLES", False),
            self.define("MDSPAN_ENABLE_BENCHMARKS", False),
            self.define("MDSPAN_ENABLE_COMP_BENCH", False),
            self.define_from_variant("MDSPAN_CXX_STANDARD", "cxx_standard"),
            self.define_from_variant("MDSPAN_ENABLE_CUDA", "cuda"),
            self.define_from_variant("MDSPAN_ENABLE_OPENMP", "openmp"),
            self.define("MDSPAN_USE_SYSTEM_GTEST", True),
            self.define_from_variant("MDSPAN_ENABLE_CONCEPTS","concepts"),
        ]
        return args
