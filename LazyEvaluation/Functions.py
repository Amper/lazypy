"""
Lazy Evaluation for Python - functions for lazy function calling

Copyright (c) 2004, Georg Bauer <gb@murphy.bofh.ms>, except where the file
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

# $Id: Functions.py 41 2004-12-27 20:21:08Z gb $

from Promises import Promise
from Futures import Future

def delay(funk, args=None, kw=None, promiseclass=Promise):

	"""
	This is a lazy variant on the apply function. It returns a promise
	for the function call that will be evaluated when needed. You can
	override the class to be used for the promise.
	"""

	if args is None: args = []
	if kw is None: kw = {}
	return promiseclass(funk, args, kw)

def lazy(funk, promiseclass=Promise):

	"""
	This function returns a lazy variant on the passed in function.
	That lazy variant will not directly evaluate but will push that
	evaluation off to some promise point. The class to be used for
	the promise can be overridden.
	"""

	def lazy_funk(*args, **kw):
		return promiseclass(funk, args, kw)

	return lazy_funk

def spawn(funk, args=None, kw=None, futureclass=Future):

	"""
	This is a parallel variant on the apply function. It returns a future
	for the function call that will be evaluated in the background. You can
	override the class to be used for the future.
	"""

	if args is None: args = []
	if kw is None: kw = {}
	return futureclass(funk, args, kw)

def future(funk, futureclass=Future):

	"""
	This function returns a future variant on the passed in function.
	That future variant will not directly evaluate but will push that
	evaluation off to the background. The class to be used for
	the future can be overridden. Every call to a future function will
	return a new future.
	"""

	def future_funk(*args, **kw):
		return futureclass(funk, args, kw)

	return future_funk

