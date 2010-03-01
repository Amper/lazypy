import sys
import unittest

from LazyEvaluation import *
from LazyEvaluation.Utils import NoneSoFar

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
        assert isinstance(promise, Promise)
        assert promise == 11
        assert promise == 11
    
    def testDelayList(self):

        def berta(a,b):
            return range(a,b)

        promise = delay(berta, (0, 10))
        assert isinstance(promise, Promise)
        assert len(promise) == 10
        assert len(promise) == 10
    
    def testIntegers(self):
        funk = lazy(anton)
        assert isinstance(funk(5,6), Promise)
        assert funk(5,6) == 11
        assert str(funk(5,6)) == '11'
        assert -funk(5,6) == -11

    def testBinary(self):
        funk = lazy(anton)
        assert funk(5,6)|funk(9,7) == 27
        assert funk(5,6)&funk(9,7) == 0
    
    def testIntegerCombined(self):
        funk = lazy(anton)
        assert funk(5,6)+11 == 22
        assert 11+funk(5,6) == 22
        assert funk(5,6)*3 == 33
        assert 3*funk(5,6) == 33
    
    def testBools(self):
        funk = lazy(anton)
        assert funk(5,6)
        assert not funk(5,-5)

    def testFloats(self):
        funk = lazy(anton)
        assert isinstance(funk(5.1,6.2), Promise)
        assert funk(5.1,6.2) == 11.3

    def testLongs(self):
        funk = lazy(anton)
        assert isinstance(funk(5L,6L), Promise)
        assert funk(3333333333333L,5555555555555L) == 8888888888888L

    def testStrings(self):
        funk = lazy(anton)
        assert isinstance(funk('anton','berta'), Promise)
        assert str(funk('anton', 'berta')) == 'antonberta'
        assert funk('anton', 'berta') == 'antonberta'
        assert funk('anton', 'berta') > 'anton'

    def testStringConcat(self):
        funk = lazy(anton)
        assert funk('anton', 'berta') + 'blah' == 'antonbertablah'
        assert 'blah' + funk('anton', 'berta')  == 'blahantonberta'

    def testStringMult(self):
        funk = lazy(anton)
        assert funk('anton','berta')*2 == 'antonbertaantonberta'
        assert 2*funk('anton','berta') == 'antonbertaantonberta'
        assert 'blah'*funk(1,1) == 'blahblah'
        assert funk(1,1)*'blah' == 'blahblah'
    
    def testUnicode(self):
        funk = lazy(anton)
        assert isinstance(funk(u'anton',u'berta'), Promise)
        assert unicode(funk('anton', 'berta')) == u'antonberta'
        assert funk(u'anton', u'berta') == u'antonberta'
    
    def testAttribute(self):
        funk = lazy(anton)
        a = getattr(funk(5,6), 'isnich', 99)
        assert a == 99
    
    def testStringInterpolation(self):
        funk = lazy(anton)
        assert (funk('blah%s', 'blubb%d') % ('anton', 5)) == 'blahantonblubb5'

class TestCase200LazyDicts(unittest.TestCase):

    def setUp(self):
        def anton(a,b):
            return dict([(x,x) for x in range(a,b)])
        
        self.g = lazy(anton)

    def testCreate(self):
        hash = self.g(1,6)
        assert hash == {1:1, 2:2, 3:3, 4:4, 5:5}
    
    def testKeys(self):
        hash = self.g(1,6)
        l = force(hash).keys()
        l.sort()
        assert l == [1,2,3,4,5]

    def testValues(self):
        hash = self.g(1,6)
        l = force(hash).values()
        l.sort()
        assert l == [1,2,3,4,5]
    
    def testAccess(self):
        hash = self.g(1,6)
        assert hash[3] == 3
    
class TestCase300LazyClass(unittest.TestCase):

    def setUp(self):
        self.obj = LazyClass()
    
    def testPromises(self):
        assert isinstance(self.obj.anton(5,6), MyPromise)
    
    def testForcing(self):
        promise = self.obj.anton(5,6)
        assert isinstance(promise, MyPromise)
        assert not promise.forced()
        assert promise == 11
        assert promise.forced()

    def testDirectAccess(self):
        assert self.obj.anton(5,6) == 11

    def testBinaryOperator(self):
        assert self.obj.anton(5,6)+self.obj.berta(5,6) == 41

    def testMixedNumeric(self):
        assert self.obj.anton(5,6)+5 == 16
        assert 5+self.obj.anton(5,6) == 16

    def testStringMultiply(self):
        assert self.obj.caesar()*3 == 'blahblahblah'

    def testAttributeAccess(self):
        assert force(self.obj.detlef()).blah.blubb == 5

    def testInlineModification(self):
        anton = self.obj.anton(5,6)
        anton += 11
        assert anton == 22

class TestCase400LazyLists(unittest.TestCase):

    def setUp(self):
        
        def berta(a,b):
            return range(a,b)

        self.func = lazy(berta)

    def testCreate(self):
        l = self.func(0,10)
        assert isinstance(l, Promise)
        assert l == range(0,10)
    
    def testAccess(self):
        assert self.func(0,10)[6] == 6
        assert self.func(0,10)[0] == 0
        assert self.func(0,10)[-1] == 9
    
    def testSlice(self):
        assert self.func(0,10)[6:8] == [6,7]
        assert self.func(0,10)[:2] == [0,1]
        assert self.func(0,10)[-2:] == [8,9]
        assert self.func(0,10)[:] == range(0,10)

    def testExtendedSlice(self):
        assert self.func(0,10)[1:5:2] == [1,3]
    
    def testLen(self):
        assert len(self.func(0,5)) == 5
    
    def testIter(self):
        l = []
        for el in self.func(0,10):
            l.append(el)
        assert l == range(0,10)
    
    def testListComprehension(self):
        l = [int(x) for x in self.func(0,10)]
        assert l == range(0,10)

class TestCase500Futures(unittest.TestCase):

    def testFastFuture(self):
        f = spawn(lambda : 5+6)
        assert isinstance(f, Future)
        assert f == 11

    def testLongerFuture(self):
        
        def fib(n):
            if n in (0,1):
                return 1
            return fib(n-1) + fib(n-2)

        f = future(fib)
        assert f(5) == fib(5)
        assert f(10) == fib(10)
        assert f(20) == fib(20)
    
class TestCase550ForkedFutures(unittest.TestCase):

    def testFastFuture(self):
        f = spawn(lambda : 5+6, futureclass=ForkedFuture)
        assert isinstance(f, ForkedFuture)
        assert f == 11

    def testLongerFuture(self):
        
        def fib(n):
            if n in (0,1):
                return 1
            return fib(n-1) + fib(n-2)

        f = future(fib, futureclass=ForkedFuture)
        assert f(5) == fib(5)
        assert f(10) == fib(10)
        assert f(20) == fib(20)
        assert f(30) == fib(30)
    
class TestCase600LazyMethod(unittest.TestCase):

    def testAttribute(self):
        o = ClassWithLazyMethod()
        assert isinstance(o.attr, Promise)
        assert o.attr == 11
    
    def testNonZero(self):
        o = ClassWithLazyMethod()
        assert isinstance(o.attr, Promise)
        assert getattr(o.attr, 'blah', True)

    def testString(self):
        o = ClassWithLazyMethod()
        assert isinstance(o.attr, Promise)
        assert ('a%sb' % o.attr) == 'a11b'

    def testInteger(self):
        o = ClassWithLazyMethod()
        assert isinstance(o.attr, Promise)
        assert 5+o.attr == 16

if __name__ == '__main__':
    unittest.main()

