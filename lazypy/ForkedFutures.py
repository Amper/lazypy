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

from multiprocessing import Process, Pipe
from lazypy.Promises import Promise, PromiseMetaClass
from lazypy.Utils import NoneSoFar

__all__ = ["ForkedFuture",
          ]

# It's awful, but works in Python 2 and Python 3
ForkedFuture = PromiseMetaClass('ForkedFuture', (object,), {})
class ForkedFuture(ForkedFuture):

    """
    This class builds future objects. A future is something that
    will be evaluated in parallel to the current flow of command.
    If you access the value of a future, your code will block until
    the value becomes available.

    The initialization get's the function and it's parameters to
    delay. If this is a promise that is created because of a delayed
    method on a promise, args[0] will be another promise of the same
    class as the current promise and func will be one of (getattr,
    apply, getitem, getslice). This knowledge can be used to optimize
    chains of delayed functions. Method access on promises will be
    factored as one getattr promise followed by one apply promise.

    A delayed future (applying lazy operators - either the lazy HOF
    or some of getattr, getitem, getslice or call) will create a
    normal promise.
    """

    __delayclass__ = Promise

    def __init__(self, func, args, kw):
        """
        Start a process with the function to be computed. Block the
        result with a queue so that somebody trying to force the
        value will block until we are complete. If the process
        get's an exception, store that for raising on force.
        """

        def thunk():
            try:
                res = apply(func, args, kw)
                self.__pipe_out.send((True, res))
            except Exception as e:
                self.__pipe_out.send((False, e))

        self.__pipe_out, self.__pipe_in = Pipe()
        self.__result = NoneSoFar
        self.__exception = NoneSoFar
        self.__proc = Process(target=thunk)
        self.__proc.start()
    
    def __force__(self):
        """
        This function returns either the value or the exception
        of the future. If the future hasn't completed yet, this
        call will block until it has.
        """

        if self.__result is NoneSoFar and self.__exception is NoneSoFar:
            (f, v) = self.__pipe_in.recv()
            if f:
                self.__result = v
            else:
                self.__exception = v
        if self.__result is not NoneSoFar:
            return self.__result
        elif self.__exception is not NoneSoFar:
            raise self.__exception
    
