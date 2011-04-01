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

import functools
import sys
from lazypy.Utils import *
from lazypy.__py2comp__ import *


def force(value):
    """
    This helper function forces evaluation of a promise. A promise
    for this function is something that has a __force__ method (much
    like an iterator in python is anything that has a __iter__
    method).
    """

    f = getattr(value, '__force__', None)
    if f: 
    	return f()
    else: 
    	return value

class PromiseMetaClass(type):

    """
    This meta class builds the behaviour of promise classes. It's mainly
    building standard methods with special behaviour to mimick several
    types in Python.
    
    The __magicmethods__ list defines what magic methods are created. Only
    those magic methods are defined that are not already defined by the
    class itself.
    
    __magicrmethods__ is much like __magicmethods__ only that it provides
    both the rmethod and the method so the proxy can decide what to use.
    
    The __magicfunctions__ list defines methods that should be mimicked by
    using some predefined function.
    
    The promise must define a __force__ method that will force evaluation
    of the promise.
    """

    __magicmethods__ = ['__abs__', '__pos__', '__invert__', '__neg__']
    
    __magicrmethods__ = [('__radd__', '__add__'), 
                         ('__rsub__', '__sub__'),
                         ('__rdiv__', '__div__'), 
                         ('__rmul__', '__mul__'),
                         ('__rand__', '__and__'), 
                         ('__ror__', '__or__'),
                         ('__rxor__', '__xor__'), 
                         ('__rlshift__', '__lshift__'),
                         ('__rrshift__', '__rshift__'), 
                         ('__rmod__', '__mod__'),
                         ('__rdivmod__', '__divmod__'), 
                         ('__rtruediv__', '__truediv__'),
                         ('__rfloordiv__', '__floordiv__'), 
                         ('__rpow__', '__pow__')]
    
    __magicfunctions__ = [('__cmp__', cmp), 
                          ('__str__', str),
                          ('__unicode__', unicode), 
                          ('__complex__', complex),
                          ('__int__', int), 
                          ('__long__', long), 
                          ('__float__', float),
                          ('__oct__', oct), 
                          ('__hex__', hex), 
                          ('__hash__', hash),
                          ('__len__', len), 
                          ('__iter__', iter), 
                          ('__delattr__', delattr),
                          ('__setitem__', setitem), 
                          ('__delitem__', delitem),
                          ('__setslice__', setslice), 
                          ('__delslice__', delslice),
                          ('__getitem__', getitem), 
                          ('__call__', apply),
                          ('__getslice__', getslice), 
                          ('__nonzero__', bool)]

    def __init__(klass, name, bases, attributes):
        for k in klass.__magicmethods__:
            if k not in attributes:
                setattr(klass, k, klass.__forcedmethodname__(k))
        for (k, v) in klass.__magicrmethods__:
            if k not in attributes:
                setattr(klass, k, klass.__forcedrmethodname__(k, v))
            if v not in attributes:
                setattr(klass, v, klass.__forcedrmethodname__(v, k))
        for (k, v) in klass.__magicfunctions__:
            if k not in attributes:
                setattr(klass, k, klass.__forcedmethodfunc__(v))
        super(PromiseMetaClass, klass).__init__(name, bases, attributes)

    def __forcedmethodname__(self, method):
        """
        This method builds a forced method. A forced method will
        force all parameters and then call the original method
        on the first argument. The method to use is passed by name.
        """

        
        def wrapped_method(self, *args, **kwargs):
            result = force(self)
            meth = getattr(result, method)
            args = [force(arg) for arg in args]
            kwargs = dict([(k,force(v)) for k,v in kwargs.items()])
            return meth(*args, **kwargs)

        return wrapped_method
    
    def __forcedrmethodname__(self, method, alternative):
        """
        This method builds a forced method. A forced method will
        force all parameters and then call the original method
        on the first argument. The method to use is passed by name.
        An alternative method is passed by name that can be used
        when the original method isn't availabe - but with reversed
        arguments. This can only handle binary methods.
        """

        def wrapped_method(self, other):
            self = force(self)
            other = force(other)
            meth = getattr(self, method, None)
            if meth is not None:
                res = meth(other)
                if res is not NotImplemented:
                    return res
            meth = getattr(other, alternative, None)
            if meth is not None:
                res = meth(self)
                if res is not NotImplemented:
                    return res
            return NotImplemented

        return wrapped_method
    
    def __forcedmethodfunc__(self, func):
        """
        This method builds a forced method that uses some other
        function to accomplish it's goals. It forces all parameters
        and then calls the function on those arguments.
        """

        def wrapped_method(*args, **kwargs):
            args = [force(arg) for arg in args]
            kwargs = dict([(k,force(v)) for k,v in kwargs.items()])
            return func(*args, **kwargs)

        return wrapped_method
    
    def __delayedmethod__(self, func):
        """
        This method builds a delayed method - one that accomplishes
        it's choire by calling some function if itself is forced.
        A class can define a __delayclass__ if it want's to
        override what class is created on delayed functions. The
        default is to create the same class again we are already
        using.
        """

        def wrapped_method(*args, **kw):
            klass = args[0].__class__
            klass = getattr(klass, '__delayclass__', klass)
            return klass(func, args, kw)

        return wrapped_method
    
# It's awful, but works in Python 2 and Python 3
Promise = PromiseMetaClass('Promise', (object,), {})
class Promise(Promise):

    """
    The initialization get's the function and it's parameters to
    delay. If this is a promise that is created because of a delayed
    method on a promise, args[0] will be another promise of the same
    class as the current promise and func will be one of (getattr,
    apply, getitem, getslice). This knowledge can be used to optimize
    chains of delayed functions. Method access on promises will be
    factored as one getattr promise followed by one apply promise.
    """

    __metaclass__ = PromiseMetaClass

    def __init__(self, func, args, kw):
        """
        Store the object and name of the attribute for later
        resolving.
        """
        self.__func = func
        self.__args = args
        self.__kw = kw
        self.__result = NoneSoFar
    
    def __force__(self):
        """
        This method forces the value to be computed and cached
        for future use. All parameters to the call are forced,
        too.
        """

        if self.__result is NoneSoFar:
            args = [force(arg) for arg in self.__args]
            kw = dict([(k, force(v)) for (k, v)
                    in self.__kw.items()])
            self.__result = self.__func(*args, **kw)
        return self.__result
