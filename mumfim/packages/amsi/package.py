# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Amsi(CMakePackage):
    """AMSI the Adaptive Multiscale Simulation Infrastructure is used
       as a basic framework for doing massively parallel multiscale analysis"""

    homepage = "https://github.com/SCOREC/amsi"
    git      = "https://github.com/SCOREC/amsi.git"
    url      = "https://github.com/SCOREC/amsi/archive/refs/tags/v0.2.0.tar.gz"

    maintainers = ['jacobmerson']

    version('develop', branch='develop')
    version('0.2.0', sha256='5fdebdf230b5c8455b689d4fa2c242689e170f2296fc1c340518ffd3592d58f0')


    variant('verbosity', default='LOW', description='set the verbosity of the output',
            values=('OFF', 'LOW', 'MED', 'HIGH'), multi=False)
    variant('tests', default=False, description='builds the tests')
    variant('zoltan', default=False, description='build with zoltan support')

    depends_on('mpi')
    depends_on('petsc+mpi')
    depends_on('zoltan', when='+zoltan')
    depends_on('pumi')
    depends_on('pumi+zoltan', when='+zoltan')
    depends_on('model-traits@0.1.1:')
    depends_on('model-traits@main',when='@develop')
    # this is used to find petsc
    depends_on('pkg-config',type='build')
    #depends_on('catch2@2.11.3:', type='build', when='+tests')
    depends_on('cmake@3.14:',type='build')

    def cmake_args(self):
        args = [self.define("MPI_HOME",self.spec['mpi'].prefix),
                self.define("CMAKE_C_COMPILER", self.spec['mpi'].mpicc),
                self.define("CMAKE_CXX_COMPILER", self.spec['mpi'].mpicxx),
                self.define("CMAKE_Fortran_COMPILER", self.spec['mpi'].mpifc),
                #self.define("MPI_C_COMPILER", self.spec['mpi'].mpicc),
                #self.define("MPI_CXX_COMPILER", self.spec['mpi'].mpicxx),
                #self.define("MPI_Fortran_COMPILER", self.spec['mpi'].mpifc),
                self.define("BUILD_EXTERNAL", False),
                self.define_from_variant('ENABLE_VERBOSITY','verbosity'),
                self.define_from_variant('ENABLE_ZOLTAN','zoltan'),
                self.define_from_variant('BUILD_TESTS','tests'),
                self.define('PETSC_DIR',self.spec['petsc'].prefix),
                ]
        return args
