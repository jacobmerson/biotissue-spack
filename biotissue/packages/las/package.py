# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install las
#
# You can edit this file again by typing:
#
#     spack edit las
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

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
    #version('0.1', sha256='17333998c2ebb9004f10ff37a82ce8ec3d229f2fc2bb32f9e820f6c217aa9bc7')

    variant('mpi', default=True, description='build with MPI')
    variant('petsc', default=False, description='build the petsc backend')
    variant('pumi', default=False, description='build the pumi interfaces')
    variant('sparskit', default=True, description='builds the sparskit backend')
    variant('tests', default=False, description='builds the tests')

    depends_on('pumi', when='+pumi')
    depends_on('petsc+mpi', when='+petsc')
    depends_on('mpi', when='+petsc')
    depends_on('pkg-config', when='+petsc')
    depends_on('mpi', when='+mpi')

    def cmake_args(self):
        args = []
        if "+mpi" in self.spec:
            args.extend(["-DCMAKE_CXX_COMPILER=%s"%self.spec['mpi'].mpicxx,
                         "-DCMAKE_C_COMPILER=%s"%self.spec['mpi'].mpicc,
                         "-DCMAKE_Fortran_COMPILER=%s"%self.spec['mpi'].mpif77,
                         "-DWITH_MPI=ON"])
        else:
            args.extend(["-DCMAKE_CXX_COMPILER=%s"%spack_cxx,
                         "-DCMAKE_C_COMPILER=%s"%spack_cc,
                         "-DCMAKE_Fortran_COMPILER=%s"%spack_f77,
                         "-DWITH_MPI=OFF"])
        # we don't deal with building with kokkos since this backend
        # hasn't been written/tested
        args.append("-DWITH_KOKKOS=OFF")
        if '+petsc' in self.spec:
            args.extend(['-DWITH_PETSC=ON',
                         '-DPETSC_DIR=%s'%self.spec['petsc'].prefix])
        else:
            args.append('-DWITH_PETSC=OFF')
        if '+pumi' in self.spec:
            args.append('-DWITH_PUMI=ON')
        else:
            args.append('-DWITH_PUMI=OFF')

        if '+sparskit' in self.spec:
            args.append("-DBUILD_SPARSKIT=ON")
        else:
            args.append("-DBUILD_SPARSKIT=OFF")
        if '+tests' in self.spec:
            args.append("-DBUILD_TESTS=ON")
        else:
            args.append("-DBUILD_TESTS=OFF")
        return args
