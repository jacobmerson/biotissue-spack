# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Amsi(CMakePackage):
    """AMSI the Adaptive Multiscale Simulation Infrastructure is used
       as a basic framework for doing massively parallel multiscale analysis"""

    homepage = "https://github.com/wrtobin/amsi"
    #git      = "https://github.com/wrtobin/amsi.git"
    git      = "git@github.com:wrtobin/amsi.git"

    maintainers = ['jacobmerson']

    version('develop', branch='develop')


    variant('verbosity', default='LOW', description='set the verbosity of the output',
            values=('OFF', 'LOW', 'MED', 'HIGH'), multi=False)
    variant('tests', default=False, description='builds the tests')
    variant('zoltan', default=False, description='build with zoltan support')

    depends_on('mpi')
    depends_on('petsc+mpi')
    depends_on('pumi simmodsuite=full')
    depends_on('zoltan', when='+zoltan')
    depends_on('pumi+zoltan', when='+zoltan')
    # this is used to find petsc
    depends_on('pkg-config',type='build')

    def cmake_args(self):
        args = []
        args.extend(["-DCMAKE_CXX_COMPILER=%s"%self.spec['mpi'].mpicxx,
                     "-DCMAKE_C_COMPILER=%s"%self.spec['mpi'].mpicc,
                     "-DCMAKE_Fortran_COMPILER=%s"%self.spec['mpi'].mpif77])

        args.append("-DENABLE_VERBOSITY=%s"%self.spec.variants['verbosity'].value)
        if '+zoltan' in self.spec:
            args.append("-DENABLE_ZOLTAN=ON")
        else:
            args.append("-DENABLE_ZOLTAN=OFF")

        args.extend(['-DPETSC_DIR=%s'%self.spec['petsc'].prefix])
        if '+tests' in self.spec:
            args.append("-DBUILD_TESTS=ON")
        else:
            args.append("-DBUILD_TESTS=OFF")
        return args
