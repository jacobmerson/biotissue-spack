# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Biotissue(CMakePackage):
    """AMSI the Adaptive Multiscale Simulation Infrastructure is used
       as a basic framework for doing massively parallel multiscale analysis"""

    homepage = "https://github.com/wrtobin/biotissue"
    git      = "https://github.com/jacobmerson/biotissue.git"

    maintainers = ['jacobmerson']

    version('develop', branch='develop')
    version('reduce-registers', branch='reduce-registers')
    version('remove-simmetrix', branch='remove-simmetrix')


    variant('tests', default=False, description='builds the tests')
    variant('kokkos', default=True, description='build with kokkos support')
    variant('logrun', default=False, description='enable logging')
    variant('verbosity', default='LOW', description='set the verbosity of the output',
            values=('OFF', 'LOW', 'MED', 'HIGH'), multi=False)
    variant('micro_backend', default='sparskit', description='set the microscale backend',
            values=('sparskit','petsc'), multi=False)

    depends_on('mpi')
    depends_on('las+pumi+petsc+sparskit')

    depends_on('amsi@develop', when='@develop,reduce-registers')
    depends_on('amsi@remove-simmetrix', when='@remove-simmetrix')
    depends_on('pumi simmodsuite=full',when='@develop,reduce-registers')
    depends_on('pumi',when='@remove-simmetrix')

    depends_on('yaml-cpp@0.3.0',when='@develop,reduce-registers')
    depends_on('pkg-config', type='build')
    depends_on('kokkos')

    #depends_on('catch2@2.11.3:', type='build', when='@develop,reduce-registers +tests')
    depends_on('catch2@2.11.3:', type='build', when='+tests')

    depends_on('model-traits@0.1.1:', when='@remove-simmetrix')
    depends_on('cmake@3.14:',type='build')

    def cmake_args(self):
        try:
            self.compiler.cxx14_flag
        except UnsupportedCompilerFlag:
            InstallError('biotissue requires a C++14-compliant C++ compiler')

        args = [
                 self.define("CMAKE_CXX_COMPILER",self.spec['mpi'].mpicxx),
                 self.define("CMAKE_C_COMPILER",self.spec['mpi'].mpicc),
                 self.define("CMAKE_Fortran_COMPILER",self.spec['mpi'].mpif77),
                 self.define_from_variant("ENABLE_VERBOSITY",'verbosity'),
                 self.define_from_variant("MICRO_BACKEND",'micro_backend'),
                 self.define("CMAKE_CXX_STANDARD",11),
                 self.define_from_variant("ENABLE_KOKKOS", "kokkos"),
                 self.define_from_variant("LOGRUN", "logrun"),
                 self.define_from_variant("BUILD_TESTS", "tests"),
                 self.define("BUILD_EXTERNAL", False)
               ]
        return args
