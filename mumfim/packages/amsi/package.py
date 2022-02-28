# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Amsi(CMakePackage):
    """AMSI the Adaptive Multiscale Simulation Infrastructure is used
       as a basic framework for doing massively parallel multiscale analysis"""

    homepage = "https://github.com/wrtobin/amsi"
    git      = "https://github.com/jacobmerson/amsi.git"

    maintainers = ['jacobmerson']

    version('develop', branch='develop')
    version('remove-simmetrix', branch='remove-simmetrix')


    variant('verbosity', default='LOW', description='set the verbosity of the output',
            values=('OFF', 'LOW', 'MED', 'HIGH'), multi=False)
    variant('tests', default=False, description='builds the tests')
    variant('zoltan', default=False, description='build with zoltan support')

    depends_on('mpi')
    depends_on('petsc+mpi')
    depends_on('zoltan', when='+zoltan')
    depends_on('pumi')
    depends_on('pumi simmodsuite=full',when="@develop")
    depends_on('pumi+zoltan', when='+zoltan')
    depends_on('model-traits@0.1.1:', when='@remove-simmetrix')
    # this is used to find petsc
    depends_on('pkg-config',type='build')
    #depends_on('catch2@2.11.3:', type='build', when='+tests')
    depends_on('cmake@3.14:',type='build')

    def cmake_args(self):
        try:
            self.compiler.cxx14_flag
        except UnsupportedCompilerFlag:
            InstallError('amsi requires a C++14-compliant C++ compiler')

        args = [
                 self.define("CMAKE_CXX_COMPILER",self.spec['mpi'].mpicxx),
                 self.define("CMAKE_C_COMPILER",self.spec['mpi'].mpicc),
                 self.define("CMAKE_Fortran_COMPILER",self.spec['mpi'].mpif77),
                 self.define("BUILD_EXTERNAL", False),
                 self.define_from_variant('ENABLE_VERBOSITY','verbosity'),
                 self.define_from_variant('ENABLE_ZOLTAN','zoltan'),
                 self.define_from_variant('BUILD_TESTS','tests'),
                 self.define('PETSC_DIR',self.spec['petsc'].prefix),
                ]
        return args
