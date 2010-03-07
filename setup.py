from setuptools import setup
from lazypy import __version__

setup(
    version = __version__,
    description = "Lazy Evaluation for Python",
    author = "Georg Bauer",
    author_email = "gb@rfc1437.de",
    url = "http://bitbucket.org/rfc1437/lazypy/",
    name='lazypy', 
    long_description=file("README").read(),
    license='MIT/X',
    platforms=['BSD','Linux','MacOS X', 'win32'],
    packages=['LazyEvaluation'],
    scripts=['test.py'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    test_suite="lazypy.tests",
)
