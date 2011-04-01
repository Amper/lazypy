from setuptools import setup
from lazypy import __version__

setup(
    version = __version__,
    description = "Lazy Evaluation for Python",
    author = "Georg Bauer, Alexander [Amper] Marshalov",
    author_email = "alone.amer@gmail.com",
    url = "https://github.com/Amper/lazypy",
    name='lazypy', 
    long_description=file("README").read(),
    license='MIT/X',
    platforms=['BSD','Linux','MacOS X', 'win32'],
    packages=['lazypy'],
    scripts=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    test_suite="lazypy.tests",
)
