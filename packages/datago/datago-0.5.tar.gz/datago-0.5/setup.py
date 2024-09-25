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
    version="0.5",
    author="Photoroom",
    author_email="team@photoroom.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    package_data={
        '': ['*.h', '*.c', '*.so'],  # Include .h, .c, and .so files
    },
    distclass=BinaryDistribution,
    zip_safe=False,
    cmdclass={
        'build_ext': CustomBuildExtCommand,
    },
)
