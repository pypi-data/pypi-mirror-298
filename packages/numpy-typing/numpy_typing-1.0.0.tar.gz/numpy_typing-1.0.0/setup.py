

from setuptools import setup, find_packages
import os

if (os.path.exists("./dist")):
    os.system("rm -r ./dist/*")

VERSION = "1.0.0"
print(f"VERSION : {VERSION}")
DESCRIPTION = 'Improved numpy typing anotations'
LONG_DESCRIPTION = """
    This package adds cleaner typing to numpy arrays.  It
    has been designed for deep learning and data processing tasks which generally
    need a lot of numpy arrays of large dimensions.'
"""

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="numpy_typing",
    version=VERSION,
    author="Pirolley Melvyn",
    author_email="",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy"],
    package_data={'': ['*.py']},
    keywords=['python', 'deep learning', 'tensorflow', 'aircraft', 'classification', 'ADS-B'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)