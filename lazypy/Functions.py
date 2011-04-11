"""
Lazy Evaluation for Python - main package with primary exports

Copyright (c) 2004, Georg Bauer <gb@murphy.bofh.ms>, 
Copyright (c) 2011, Alexander Marshalov <alone.amper@gmail.com>, 
except where the file explicitly names other copyright holders and licenses.

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from lazypy.Promises import Promise
from lazypy.Futures import Future
from lazypy.ForkedFutures import ForkedFuture

__all__ = ["delay",
           "lazy",
           "spawn",
           "future",
           "fork",
           "forked",
          ]

def delay(func, args=None, kw=None, promiseclass=Promise):

    """
    This is a lazy variant on the apply function. It returns a promise
    for the function call that will be evaluated when needed. You can
    override the class to be used for the promise.
    """

    if args is None: 
    	args = []
    if kw is None: 
    	kw = {}
    return promiseclass(func, args, kw)

def lazy(func, promiseclass=Promise):

    """
    This function returns a lazy variant on the passed in function.
    That lazy variant will not directly evaluate but will push that
    evaluation off to some promise point. The class to be used for
    the promise can be overridden.
    """

    def lazy_func(*args, **kw):
        return promiseclass(func, args, kw)
    lazy_func.__doc__ = func.__doc__

    return lazy_func

def spawn(func, args=None, kw=None, futureclass=Future):

    """
    This is a parallel variant on the apply function. It returns a future
    for the function call that will be evaluated in the background. You can
    override the class to be used for the future.
    """

    if args is None: 
    	args = []
    if kw is None: 
    	kw = {}
    return futureclass(func, args, kw)

def future(func, futureclass=Future):

    """
    This function returns a future variant on the passed in function.
    That future variant will not directly evaluate but will push that
    evaluation off to the background. The class to be used for
    the future can be overridden. Every call to a future function will
    return a new future.
    """

    def future_func(*args, **kw):
        return futureclass(func, args, kw)
    lazy_func.__doc__ = func.__doc__

    return future_func

def fork(func, args=None, kw=None, futureclass=ForkedFuture):

    """
    This is a parallel variant on the apply function. It returns a future
    for the function call that will be evaluated in the background. You can
    override the class to be used for the future. It uses forked futures
    by default.
    """

    if args is None: 
    	args = []
    if kw is None: 
    	kw = {}
    return futureclass(func, args, kw)

def forked(func, futureclass=ForkedFuture):

    """
    This function returns a future variant on the passed in function.
    That future variant will not directly evaluate but will push that
    evaluation off to the background. The class to be used for
    the future can be overridden. Every call to a future function will
    return a new future. It uses forked futures by default.
    """

    def future_func(*args, **kw):
        return futureclass(func, args, kw)
    lazy_func.__doc__ = func.__doc__

    return future_func

