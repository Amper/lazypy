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

import sys
assert sys.hexversion >= 0x02070000, 'at least Python 2.7 is needed'

__version__ = "0.6"
__all__ = ["Promise",
           "PromiseMetaClass",
           "force",
           "Future",
           "ForkedFuture",
           "LazyEvaluated",
           "LazyEvaluatedMetaClass",
           "delay",
           "lazy",
           "spawn",
           "future",
           "fork",
           "forked",
          ]

from lazypy.Promises import Promise, PromiseMetaClass, force
from lazypy.Futures import Future
from lazypy.ForkedFutures import ForkedFuture
from lazypy.LazyClasses import LazyEvaluated, LazyEvaluatedMetaClass
from lazypy.Functions import delay, lazy, spawn, future, fork, forked
