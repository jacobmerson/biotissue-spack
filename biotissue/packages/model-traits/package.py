# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ModelTraits(CMakePackage):
    """ Model setup and querying in C++. """

    homepage = "https://github.com/jacobmerson/model-traits/"
    url      = "https://github.com/jacobmerson/model-traits/archive/refs/tags/v0.1.0.tar.gz"

    maintainers = ['jacobmerson']

    version('0.1.0', sha256='ff7c1c5be6977f1d3dc592e8b6c5bff5a8b7ea80d0f059d85c02300bdb8faf2c')



    variant('tests', default=False, description='builds the tests')
    variant('yaml', default=True, description='build the Yaml IO backend')
    variant('simmetrix', default=False, description='build the Simmetrix backend')
    variant('pumi', default=False, description='build the pumi examples')

    depends_on('yaml-cpp@0.6.3:',when='+yaml')
    depends_on('catch2@3.0.0-preview3:', when='+tests')
    depends_on('pumi', when='+pumi')
    depends_on('simmetrix-simmodsuite', when='+simmetrix')
    depends_on('fmt@7.1.3')
    depends_on('cmake@3.14.0:',type='build')

    def cmake_args(self):
        args = [self.define('BUILD_EXTERNAL',False),
                self.define_from_variant('ENABLE_SCOREC','pumi'),
                self.define_from_variant('ENABLE_SIMMETRIX','simmetrix'),
                self.define_from_variant('ENABLE_YAML','yaml'),
                self.define_from_variant('BUILD_TESTING','tests')]
        return args
