import setuptools

setuptools.setup(
    name="tango-canopen-simulator",
    version="0.1.0",
    author="Sebastian Jennen",
    author_email="sj@imagearts.de",
    description="tango-canopen-simulator device driver",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    scripts=['CanopenSimulator.py']
)