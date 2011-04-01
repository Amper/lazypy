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

__all__ = ["NoneSoFar",
           "getitem",
           "setitem",
           "delitem",
           "getslice",
           "setslice",
           "delslice",
          ]

class NoneSoFar(object):

    """
    This is a singleton to give you something to put somewhere that
    should never be a rightfull return value of anything.
    """
    
    def __str__(self):
        return 'NoneSoFar'
    
    def __repr__(self):
        return 'NoneSoFar'

    def __nonzero__(self):
        return 0

NoneSoFar = NoneSoFar()

def getitem(obj, key):
    """
    This is a helper function needed in promise objects to pass
    on __getitem__ calls. It just mimicks the getattr call, only
    it uses dictionary style access.
    """
    return obj[key]

def setitem(obj, key, value):
    """
    This is a helper function needed in promise objects to pass
    on __setitem__ calls. It just mimicks the setattr call, only
    it uses dictionary style access.
    """
    obj[key] = value

def delitem(obj, key):
    """
    This is a helper function needed in promise objects to pass
    on __delitem__ calls. It just mimicks the delattr call, only
    it uses dictionary style access.
    """
    del obj[key]

def getslice(obj, start, stop):
    """
    This is a helper function needed in promise objects to pass
    on __getslice__ calls. It just mimicks the getattr call, only
    it uses dictionary style access.
    """
    return obj[start:stop]

def setslice(obj, start, stop, value):
    """
    This is a helper function needed in promise objects to pass
    on __setslice__ calls. It just mimicks the setattr call, only
    it uses dictionary style access.
    """
    obj[start:stop] = value

def delslice(obj, start, stop):
    """
    This is a helper function needed in promise objects to pass
    on __delslice__ calls. It just mimicks the delattr call, only
    it uses dictionary style access.
    """
    del obj[start:stop]

