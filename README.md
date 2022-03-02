# Instructions for building MuMFiM with [Spack](https://github.com/spack/spack.git)


## Initial setup

```bash
# create parent directory for all spack things
mkdir spack && cd spack
export SPACK_ROOT=`pwd`

# download spack
git clone https://github.com/spack/spack.git

# make sure to clear any modules which you
# don't want to interfere with spack
module purge

# add spack to the command line
source $SPACK_ROOT/spack/share/spack/setup-env.sh

# make directory to store all external spack repos
mkdir repos && cd repos

# download the mumfim spack repo
git clone git@github.com:jacobmerson/mumfim-spack.git

# add repositories to spack
spack repo add mumfim-spack/mumfim

```
## Modifying the spack config files

It is important to modify the various spack config files for your system.
This tells spack what compilers to use, etc. examples of the setup for the
scorec systems will be included in the `mumfim-spack` repository.

It is common practice/reccomended to use system packages for `cmake`, compilers, `python`, `cuda`,
however spack responds much better if it builds most of the libraries which need linking
against itself, so don't go too overboard with using system packages.

## Installing

```bash
spack install mumfim
```

## Setting up spack to build dependencies

`spack` can be used to install the dependencies, and leave the system in a state where
building and regular development can be used. See the [documentation](https://spack-tutorial.readthedocs.io/en/latest/tutorial_developer_workflows.html)
for an example.
