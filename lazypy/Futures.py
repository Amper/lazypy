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

from threading import Condition, Thread
from lazypy.Promises import Promise, PromiseMetaClass
from lazypy.Utils import NoneSoFar

__all__ = ["Future",
          ]

class BrokenFutureError(Exception):
    """
    This exception is thrown if a future is broken - if it neither
    has a result nor has an exception.
    """
    pass

# It's awful, but works in Python 2 and Python 3
Future = PromiseMetaClass('Future', (object,), {})
class Future(Future):

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
        Start a thread with the function to be computed. Block the
        result with a lock so that somebody trying to force the
        value will block until we are complete. If the thread
        get's an exception, store that for raising on force.

        We use a thread condition to make sure that the thread is
        started before we continue our main flow.
        """

        def thunk():
            self.__sync.acquire()
            try:
                self.__sync.notify()
                try:
                    self.__result = apply(func, args, kw)
                except Exception as e:
                    self.__exception = e
            finally:
                self.__sync.release()

        self.__result = NoneSoFar
        self.__exception = NoneSoFar
        self.__sync = Condition()
        self.__sync.acquire()
        try:
            self.__thread = Thread(target=thunk)
            self.__thread.start()
            self.__sync.wait()
        finally:
            self.__sync.release()
    
    def __force__(self):
        """
        This function returns either the value or the exception
        of the future. If the future hasn't completed yet, this
        call will block until it has.
        """

        self.__sync.acquire()
        try:
            if self.__result is not NoneSoFar:
                return self.__result
            elif self.__exception is not NoneSoFar:
                raise self.__exception
            else:
                raise BrokenFutureError
        finally:
            self.__sync.release()
    

