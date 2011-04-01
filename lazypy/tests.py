from __future__ import unicode_literals
import sys
import unittest

from lazypy import *
from lazypy.Utils import NoneSoFar

class MySpecialError(Exception):
    pass

def anton(a,b):
    return a+b

class ClassWithAttrs:
    pass

class ClassWithLazyMethod:

    def __init__(self):
        self.attr = self.anton(5,6)

    def anton(self, a, b):
        return a+b
    anton = lazy(anton)

class MyPromise(object):

    __metaclass__ = PromiseMetaClass

    def __init__(self, func, args, kw):
        self.__func = func
        self.__args = args
        self.__kw = kw
        self.__result = NoneSoFar

    def forced(self):
        return self.__result is not NoneSoFar
    
    def __force__(self):
        if self.__result is NoneSoFar:
            args = [force(arg) for arg in self.__args]
            kw = dict([(k, force(v)) for (k, v)
                    in self.__kw.items()])
            self.__result = apply(self.__func, args, kw)
        return self.__result

class LazyClass(LazyEvaluated):

    __promiseclass__ = MyPromise

    def anton(self, a, b):
        return a+b

    def berta(self, a, b):
        return a*b

    def caesar(self):
        return 'blah'
    
    def detlef(self):
        res = ClassWithAttrs()
        res.blah = ClassWithAttrs()
        res.blah.blubb = 5
        return res

class TestCase100Simple(unittest.TestCase):

    def testDelay(self):
        promise = delay(anton, (5, 6))
        self.assertTrue(isinstance(promise, Promise))
        self.assertEqual(promise, 11)
        self.assertEqual(promise, 11)
    
    def testDelayList(self):

        def berta(a,b):
            return range(a,b)

        promise = delay(berta, (0, 10))
        self.assertTrue(isinstance(promise, Promise))
        self.assertEqual(len(promise), 10)
        self.assertEqual(len(promise), 10)
    
    def testIntegers(self):
        funk = lazy(anton)
        self.assertTrue(isinstance(funk(5,6), Promise))
        self.assertEqual(funk(5,6), 11)
        self.assertEqual(str(funk(5,6)), '11')
        self.assertEqual(-funk(5,6), -11)

    def testBinary(self):
        funk = lazy(anton)
        self.assertEqual(funk(5,6)|funk(9,7), 27)
        self.assertEqual(funk(5,6)&funk(9,7), 0)
    
    def testIntegerCombined(self):
        funk = lazy(anton)
        self.assertEqual(funk(5,6)+11, 22)
        self.assertEqual(11+funk(5,6), 22)
        self.assertEqual(funk(5,6)*3, 33)
        self.assertEqual(3*funk(5,6), 33)
    
    def testBools(self):
        funk = lazy(anton)
        self.assertTrue(funk(5,6))
        self.assertFalse(funk(5,-5))

    def testFloats(self):
        funk = lazy(anton)
        self.assertTrue(isinstance(funk(5.1,6.2), Promise))
        self.assertEqual(funk(5.1,6.2), 11.3)

    def testLongs(self):
        funk = lazy(anton)
        self.assertTrue(isinstance(funk(5,6), Promise))
        self.assertEqual(funk(3333333333333,5555555555555), 8888888888888)

    def testStrings(self):
        funk = lazy(anton)
        self.assertTrue(isinstance(funk('anton','berta'), Promise))
        self.assertEqual(str(funk('anton', 'berta')), 'antonberta')
        self.assertEqual(funk('anton', 'berta'), 'antonberta')
        self.assertTrue(funk('anton', 'berta') > 'anton')

    def testStringConcat(self):
        funk = lazy(anton)
        self.assertEqual(funk('anton', 'berta') + 'blah', 'antonbertablah')
        self.assertEqual('blah' + funk('anton', 'berta'), 'blahantonberta')

    def testStringMult(self):
        funk = lazy(anton)
        self.assertEqual(funk('anton','berta')*2, 'antonbertaantonberta')
        self.assertEqual(2*funk('anton','berta'), 'antonbertaantonberta')
        self.assertEqual('blah'*funk(1,1), 'blahblah')
        self.assertEqual(funk(1,1)*'blah', 'blahblah')
    
    def testUnicode(self):
        funk = lazy(anton)
        self.assertTrue(isinstance(funk('anton','berta'), Promise))
        self.assertEqual(unicode(funk('anton', 'berta')), 'antonberta')
        self.assertEqual(funk('anton', 'berta'), 'antonberta')
    
    def testAttribute(self):
        funk = lazy(anton)
        a = getattr(funk(5,6), 'isnich', 99)
        self.assertEqual(a, 99)
    
    def testStringInterpolation(self):
        funk = lazy(anton)
        self.assertEqual((funk('blah%s', 'blubb%d') % ('anton', 5)), 'blahantonblubb5')

class TestCase200LazyDicts(unittest.TestCase):

    def setUp(self):
        def anton(a,b):
            return dict([(x,x) for x in range(a,b)])
        
        self.g = lazy(anton)

    def testCreate(self):
        hash = self.g(1,6)
        self.assertEqual(hash, {1:1, 2:2, 3:3, 4:4, 5:5})
    
    def testKeys(self):
        hash = self.g(1,6)
        l = force(hash).keys()
        l.sort()
        self.assertEqual(l, [1,2,3,4,5])

    def testValues(self):
        hash = self.g(1,6)
        l = force(hash).values()
        l.sort()
        self.assertEqual(l, [1,2,3,4,5])
    
    def testAccess(self):
        hash = self.g(1,6)
        self.assertEqual(hash[3], 3)
    
class TestCase300LazyClass(unittest.TestCase):

    def setUp(self):
        self.obj = LazyClass()
    
    def testPromises(self):
        self.assertTrue(isinstance(self.obj.anton(5,6), MyPromise))
    
    def testForcing(self):
        promise = self.obj.anton(5,6)
        self.assertTrue(isinstance(promise, MyPromise))
        self.assertFalse(promise.forced())
        self.assertEqual(promise, 11)
        self.assertTrue(promise.forced())

    def testDirectAccess(self):
        self.assertEqual(self.obj.anton(5,6), 11)

    def testBinaryOperator(self):
        self.assertEqual(self.obj.anton(5,6)+self.obj.berta(5,6), 41)

    def testMixedNumeric(self):
        self.assertEqual(self.obj.anton(5,6)+5, 16)
        self.assertEqual(5+self.obj.anton(5,6), 16)

    def testStringMultiply(self):
        self.assertEqual(self.obj.caesar()*3, 'blahblahblah')

    def testAttributeAccess(self):
        self.assertEqual(force(self.obj.detlef()).blah.blubb, 5)

    def testInlineModification(self):
        anton = self.obj.anton(5,6)
        anton += 11
        self.assertEqual(anton, 22)

class TestCase400LazyLists(unittest.TestCase):

    def setUp(self):
        
        def berta(a,b):
            return range(a,b)

        self.func = lazy(berta)

    def testCreate(self):
        l = self.func(0,10)
        self.assertTrue(isinstance(l, Promise))
        self.assertEqual(l, range(0,10))
    
    def testAccess(self):
        self.assertEqual(self.func(0,10)[6], 6)
        self.assertEqual(self.func(0,10)[0], 0)
        self.assertEqual(self.func(0,10)[-1], 9)
    
    def testSlice(self):
        self.assertEqual(self.func(0,10)[6:8], [6,7])
        self.assertEqual(self.func(0,10)[:2], [0,1])
        self.assertEqual(self.func(0,10)[-2:], [8,9])
        self.assertEqual(self.func(0,10)[:], range(0,10))

    def testExtendedSlice(self):
        self.assertEqual(self.func(0,10)[1:5:2], [1,3])
    
    def testLen(self):
        self.assertEqual(len(self.func(0,5)), 5)
    
    def testIter(self):
        l = []
        for el in self.func(0,10):
            l.append(el)
        self.assertEqual(l, range(0,10))
    
    def testListComprehension(self):
        l = [int(x) for x in self.func(0,10)]
        self.assertEqual(l, range(0,10))

class TestCase500Futures(unittest.TestCase):

    def testFastFuture(self):
        f = spawn(lambda : 5+6)
        self.assertTrue(isinstance(f, Future))
        self.assertEqual(f, 11)

    def testLongerFuture(self):
        
        def fib(n):
            if n in (0,1):
                return 1
            return fib(n-1) + fib(n-2)

        f = future(fib)
        for n in (5, 10, 20):
            self.assertEqual(f(n), fib(n))
    
class TestCase550ForkedFutures(unittest.TestCase):

    def testFastFuture(self):
        f = fork(lambda : 5+6)
        self.assertTrue(isinstance(f, ForkedFuture))
        self.assertEqual(f, 11)
        self.assertEqual(f, 11)
        self.assertEqual(f, 11)

    def testFutureWithException(self):
        def crasher():
            raise MySpecialError(55)

        f = fork(crasher)
        self.assertTrue(isinstance(f, ForkedFuture))
        self.assertRaises(MySpecialError, crasher)

    def testLongerFuture(self):
        
        def fib(n):
            if n in (0,1):
                return 1
            return fib(n-1) + fib(n-2)

        f = forked(fib)
        for n in (5, 10, 20, 30):
            self.assertEqual(f(n), fib(n))
    
class TestCase600LazyMethod(unittest.TestCase):

    def testAttribute(self):
        o = ClassWithLazyMethod()
        self.assertTrue(isinstance(o.attr, Promise))
        self.assertEqual(o.attr, 11)
    
    def testNonZero(self):
        o = ClassWithLazyMethod()
        self.assertTrue(isinstance(o.attr, Promise))
        self.assertEqual(getattr(o.attr, 'blah', True), True)

    def testString(self):
        o = ClassWithLazyMethod()
        self.assertTrue(isinstance(o.attr, Promise))
        self.assertEqual(('a%sb' % o.attr), 'a11b')

    def testInteger(self):
        o = ClassWithLazyMethod()
        self.assertTrue(isinstance(o.attr, Promise))
        self.assertEqual(5+o.attr, 16)

if __name__ == '__main__':
    unittest.main()

