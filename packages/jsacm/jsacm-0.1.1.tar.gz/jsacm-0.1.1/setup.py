from setuptools import setup, find_packages
# re run setup = python setup.py sdist bdist_wheel
# re upload to pypi = twine upload --verbose dist/*
# or = twine upload --skip-existing dist/*
VERSION = '0.1.1' 
DESCRIPTION = 'jsacm helps programers :)'
LONG_DESCRIPTION = 'A python package to aid in programming (calculator credit to Oliver)'

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
        install_requires=['deep_translator','aspose.words','datetime','names','pytubefix'], # add any additional packages that 
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