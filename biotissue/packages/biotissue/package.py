# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Biotissue(CMakePackage):
    """AMSI the Adaptive Multiscale Simulation Infrastructure is used
       as a basic framework for doing massively parallel multiscale analysis"""

    homepage = "https://github.com/wrtobin/biotissue"
    #git      = "https://github.com/wrtobin/biotissue.git"
    git      = "git@github.com:wrtobin/biotissue.git"

    maintainers = ['jacobmerson']

    version('develop', branch='develop')


    variant('tests', default=False, description='builds the tests')
    variant('kokkos', default=True, description='build with kokkos support')
    variant('logrun', default=False, description='enable logging')
    variant('verbosity', default='LOW', description='set the verbosity of the output',
            values=('OFF', 'LOW', 'MED', 'HIGH'), multi=False)
    variant('micro_backend', default='sparskit', description='set the microscale backend',
            values=('sparskit','petsc'), multi=False)

    depends_on('mpi')
    depends_on('amsi')
    depends_on('las+pumi+petsc+sparskit')
    #depends_on('pumi simmodsuite=full')
    depends_on('pumi')
    conflicts('pumi simmodsuite=none')
    depends_on('yaml-cpp@0.3.0')
    depends_on('pkg-config', type='build')
    depends_on('kokkos+cuda+wrapper+cuda_lambda', when='+kokkos%gcc')
    depends_on('kokkos+cuda+cuda_lambda', when='+kokkos')
    #depends_on('cuda', when='+kokkos')
    depends_on('catch2@2.11.3:', type='build', when='+tests')
    depends_on('ninja', type='build')
    generator = 'Ninja'

    def cmake_args(self):
        args = []
        args.extend(["-DCMAKE_CXX_COMPILER=%s"%self.spec['mpi'].mpicxx,
                     "-DCMAKE_C_COMPILER=%s"%self.spec['mpi'].mpicc,
                     "-DCMAKE_Fortran_COMPILER=%s"%self.spec['mpi'].mpif77])

        args.append("-DENABLE_VERBOSITY=%s"%self.spec.variants['verbosity'].value)
        args.append("-DMICRO_BACKEND=%s"%self.spec.variants['micro_backend'].value)
        args.append("-DCMAKE_CXX_STANDARD=11")
        #args.append("-DCMAKE_CXX_FLAGS=-Wno-unused-variable -Wno-unused-but-set-variable")

        # these values shouldn't be needed since when we build with spack,
        # all of this information is encoded in the CMAKE_PREFIX_PATH variable
        args.extend(["-Dlas_DIR=%s"%self.spec['las'].prefix.lib.cmake,
                     "-Dlas_core_DIR=%s"%self.spec['las'].prefix.lib.cmake])
        #args.extend(["-Dlas_DIR=%s"%self.spec['las'].prefix.lib.cmake,
        #             "-Dlas_core_DIR=%s"%self.spec['las'].prefix.lib.cmake,
        #             "-Damsi_DIR=%s"%self.spec['amsi'].prefix.lib.cmake,
        #             "-Dyaml-cpp_DIR=%s"%self.spec["yaml-cpp"].prefix.lib.pkgconfig,
        #             "-DKokkos_DIR=%s"%self.spec["kokkos"].prefix.lib64.cmake.Kokkos,
        #             ])
        # for the compile commands database
        args.append("-DCMAKE_EXPORT_COMPILE_COMMANDS=true")

        if '+kokkos' in self.spec:
            args.append("-DENABLE_KOKKOS=ON")
        else:
            args.append("-DENABLE_KOKKOS=OFF")
        if '+logrun' in self.spec:
            args.append("-DLOGRUN=ON")
        else:
            args.append("-DLOGRUN=OFF")
        if '+tests' in self.spec:
            args.append("-DBUILD_TESTS=ON")
        else:
            args.append("-DBUILD_TESTS=OFF")
        return args
