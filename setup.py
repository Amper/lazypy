from setuptools import setup

setup(
    version = "0.3",
    description = "Lazy Evaluation for Python",
    author = "Georg Bauer",
    author_email = "gb@rfc1437.de",
    url = "http://bitbucket.org/rfc1437/lazypy/",
    name='lazypy', 
    long_description=file("README.md").read(),
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
)
