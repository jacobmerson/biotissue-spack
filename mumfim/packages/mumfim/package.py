# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mumfim(CMakePackage):
    """Multiscale Modeling of Fibrous Materials"""

    homepage = "https://github.com/SCOREC/mumfim"
    git      = "https://github.com/SCOREC/mumfim.git"
    url      = "https://github.com/SCOREC/mumfim/archive/refs/tags/v0.4.0.tar.gz"

    maintainers = ['jacobmerson']

    version('develop', branch='develop')
    version('0.4.0', sha256='f36074ebdf23c58a552ac4ccfdfa2a38ea17e2d11f5e0b41af50791acf4b8572')


    variant('tests', default=False, description='builds the tests')
    variant('kokkos', default=True, description='build with kokkos support')
    variant('logrun', default=False, description='enable logging')
    variant('verbosity', default='LOW', description='set the verbosity of the output',
            values=('OFF', 'LOW', 'MED', 'HIGH'), multi=False)
    variant('micro_backend', default='sparskit', description='set the microscale backend',
            values=('sparskit','petsc'), multi=False)
    variant('adios2', default=False, description='build adios2 test runner')

    depends_on('mpi')
    depends_on('las@0.1.2:+pumi+petsc+sparskit')
    depends_on('las@develop+pumi+petsc+sparskit', when='@develop')

    depends_on('amsi@0.2.0:')
    depends_on('amsi@develop', when='@develop')
    depends_on('pumi@:2.2.7')

    depends_on('yaml-cpp@0.6.3:')
    depends_on('pkg-config', type='build')
    depends_on('kokkos')
    depends_on('kokkos-kernels')

    depends_on('catch2@2.11.3:2.99.99', type='build', when='+tests')

    depends_on('model-traits@0.1.1:')
    depends_on('model-traits@main',when='@develop')
    depends_on('cmake@3.14:',type='build')

    depends_on('adios2@2.8.0:',when='+adios2')

    def cmake_args(self):
        args = [self.define("MPI_HOME",self.spec['mpi'].prefix),
                self.define_from_variant("ENABLE_VERBOSITY",'verbosity'),
                self.define_from_variant("MICRO_BACKEND",'micro_backend'),
                self.define("CMAKE_CXX_STANDARD",11),
                self.define_from_variant("ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("LOGRUN", "logrun"),
                self.define_from_variant("BUILD_TESTS", "tests"),
                self.define_from_variant("MUMFIM_ENABLE_ADIOS2", "adios2"),
                self.define("BUILD_EXTERNAL", False)
               ]
        if "dev_path" in self.spec.variants:
            args.append(self.define("CMAKE_EXPORT_COMPILE_COMMANDS",True))
        return args
