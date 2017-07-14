
from dyspatch.dispatchers import DispatcherBase


def test_minimal_implementation():

    class MinimalDispatcher(DispatcherBase):

        def __init__(self, *args, **kwargs):
            self.mapping = {}
            super().__init__(*args, **kwargs)

        def register(self, key, callable):
            self.mapping[key] = callable

        def match(self, key):
            return self.mapping[key]


    dispatcher = MinimalDispatcher()
    dispatcher.register('foo', lambda: 'bar')
    assert dispatcher.dispatch('foo') == 'bar'
