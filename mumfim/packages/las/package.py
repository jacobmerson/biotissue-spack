# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Las(CMakePackage):
    """LAS provides a zero-overhead API to use the general operations of a
    linear algebra library operating on large (parallel) matrices and vectors.
    Currently the library only allows double-values as scalars."""

    homepage = "https://github.com/wrtobin/las"
    url      = "https://github.com/wrtobin/las/archive/v0.1.tar.gz"
    git      = "https://github.com/wrtobin/las.git"

    maintainers = ['jacobmerson']

    version('develop', branch='dev')
    version('0.1', sha256='17333998c2ebb9004f10ff37a82ce8ec3d229f2fc2bb32f9e820f6c217aa9bc7')
    version('0.1.2', sha256='18f30cde4e069d5f8979a55b09f247a0dd2a90004047c6f531723702a2c3c22b')

    variant('mpi', default=True, description='build with MPI')
    variant('petsc', default=False, description='build the petsc backend')
    variant('pumi', default=False, description='build the pumi interfaces')
    variant('sparskit', default=True, description='builds the sparskit backend')
    variant('tests', default=False, description='builds the tests')

    depends_on('pumi', when='+pumi')
    depends_on('petsc+mpi', when='+petsc')
    depends_on('mpi', when='+petsc')
    depends_on('pkg-config', when='+petsc', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('catch2@2.11.3:', type='build', when='+tests')
    depends_on('cmake@3.14:',type='build')
    conflicts("~mpi", when="+petsc")
    #depends_on('ninja', type='build')
    #generator = 'Ninja'

    def cmake_args(self):
        args = [
                self.define_from_variant("WITH_MPI", "mpi"),
                self.define("CMAKE_C_COMPILER", self.spec['mpi'].mpicc),
                self.define("CMAKE_CXX_COMPILER", self.spec['mpi'].mpicxx),
                self.define("CMAKE_Fortran_COMPILER", self.spec['mpi'].mpifc),
                self.define("WITH_KOKKOS", False),
                self.define_from_variant("WITH_PETSC","petsc"),
                self.define_from_variant("WITH_PUMI","pumi"),
                self.define_from_variant("WITH_SPARSKIT","sparskit"),
                self.define_from_variant("BUILD_TESTS","tests"),
                ]
        if "+mpi" in self.spec:
            args.extend([self.define("MPI_HOME",self.spec['mpi'].prefix),])
        if "+petsc" in self.spec:
            args.append(self.define("PETSC_DIR",self.spec['petsc'].prefix))
        return args
