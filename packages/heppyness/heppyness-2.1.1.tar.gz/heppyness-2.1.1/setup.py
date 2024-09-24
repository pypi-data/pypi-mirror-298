import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='heppyness',
    license='HEP license, based on MIT license',
    version='2.1.1',
    author='Stefan Richter',
    author_email='stefan.richter@cern.ch',
    maintainer='Stefan Richter',
    maintainer_email='stefan.richter@cern.ch',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.cern.ch/strichte/heppy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'uproot',
        'uproot-methods',
        'awkward',
        'pandas',
        'pyyaml',
        'sphinx_rtd_theme',
    ],
    python_requires='>=3.6',
)
