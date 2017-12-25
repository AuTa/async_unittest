import asyncio
import functools
import unittest
import inspect
try:
    import uvloop as async_loop
except ImportError:
    async_loop = asyncio


class TestCaseMeta(type(unittest.TestCase)):
    """Metaclass for async method.

    """

    @staticmethod
    def _iter_methods(bases, ns):
        for base in bases:
            # methods of parent class
            for methname in dir(base):
                if not methname.startswith('test_'):
                    continue

                meth = getattr(base, methname)
                if not inspect.iscoroutinefunction(meth):
                    continue

                yield methname, meth

        for methname, meth in ns.items():
            # classmethods
            if not methname.startswith('test_'):
                continue

            if not inspect.iscoroutinefunction(meth):
                continue

            yield methname, meth

    def __new__(mcls, name, bases, ns, *args, **kwargs):
        for methname, meth in mcls._iter_methods(bases, ns):
            # add decorate to async test method
            @functools.wraps(meth)
            def wrapper(self, *args, __meth__=meth, **kwargs):
                self.loop.run_until_complete(__meth__(self, *args, **kwargs))

            ns[methname] = wrapper
        return super().__new__(mcls, name, bases, ns)


class TestCase(unittest.TestCase, metaclass=TestCaseMeta):

    @classmethod
    def setUpClass(cls):
        loop = async_loop.new_event_loop()
        asyncio.set_event_loop(loop)
        cls.loop = loop

    @classmethod
    def tearDownClass(cls):
        asyncio.set_event_loop(None)
