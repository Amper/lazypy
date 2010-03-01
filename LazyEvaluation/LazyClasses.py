"""
Lazy Evaluation for Python - convenience classes

Copyright (c) 2004, Georg Bauer <gb@rfc1437.de>, except where the file
explicitly names other copyright holders and licenses.

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

import types

from Promises import Promise
from Functions import lazy

class LazyEvaluatedMetaClass(type):

    """
    This meta class rewrites all function attributes to not directly
    run but to yield a generator that will run the function later on.
    """

    def __init__(klass, name, bases, attributes):
        promiseclass = getattr(klass, '__promiseclass__', Promise)
        for (k, v) in attributes.items():
            if isinstance(v, types.FunctionType):
                setattr(klass, k, lazy(v, promiseclass))
        super(LazyEvaluatedMetaClass, klass).__init__(name,
            bases, attributes)

class LazyEvaluated(object):

    """
    This is the base class for all classes that should evaluate in
    a lazy fashion. You can overload __promiseclass__ if you want to
    have different promise handling in your code.
    """

    __metaclass__ = LazyEvaluatedMetaClass
    __promiseclass__ = Promise

