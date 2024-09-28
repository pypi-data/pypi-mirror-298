from setuptools import setup, find_packages

VERSION = '3.4.15' 
DESCRIPTION = 'flag package'
LONG_DESCRIPTION = 'You just have to look for the flag'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="flagpypi", 
        version=VERSION,
        author="John Doe",
        author_email="john_doe@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)