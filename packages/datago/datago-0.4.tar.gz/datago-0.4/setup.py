import setuptools
from setuptools.command.build_ext import build_ext
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()


class BinaryDistribution(setuptools.Distribution):
    def has_ext_modules(_):
        return True


class CustomBuildExtCommand(build_ext):
    def run(self):
        build_ext.run(self)
        for so_file in glob.glob('*.so'):
            self.copy_file(so_file, self.build_lib)

setuptools.setup(
    name="datago",
    version="0.4",
    author="Photoroom",
    author_email="team@photoroom.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    distclass=BinaryDistribution,
    cmdclass={
        'build_ext': CustomBuildExtCommand,
    },
)
