from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'jsacm'
LONG_DESCRIPTION = 'A python package to aid in programming'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="jsacm", 
        version=VERSION,
        author="Jacob Browning",
        author_email="<jacobbrowning2008@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['deep_translator','aspose.words','datetime'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)