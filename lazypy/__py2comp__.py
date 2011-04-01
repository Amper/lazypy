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
PY_VER = sys.version_info[0]

__all__ = ["apply", 
           "unicode", 
           "cmp",
           "long",
           ]

if PY_VER >= 3:
    apply = lambda func, args=[], kwargs={}: func(*args, **kwargs)
    unicode = str
    cmp = lambda a,b: (a > b) - (a < b)
    long = int
else:
	apply = apply
	unicode = unicode
	cmp = cmp
	long = long
