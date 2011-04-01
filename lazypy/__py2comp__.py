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
