
import abc

from typing import *


class RegistryBase:
    pass


class CallerBase:

    def __init__(self, dispatcher):
        pass

    def call(self, callable):
        return callable()


class DispatcherBase:
    """Base class for all concrete dispatcher implementations.

    You can't use this directly. If you look for a way to do routing
    or dispatch events, use one of the classes ihneriting from DispatcherBase.

    Alternatively you can also inherit from DispatcherBase yourself and
    create your own dispatcher.

    All dispatchers follow the same structure:

        - they have a registry object defining the strategy to links keys
         to callable.  The registry can later, giving a key, find the
         corresponding callable(s). Often those are mappings between
         strings and functions.

        - they have a caller objecting defining the strategy to call a callable:
         how to pass arguments to it, how to handle errors, etc.

        - they have a register() method delegating the linking to the registry.
         E.G: dispatcher.register('foo.bar', do_stuff).

        - they have a dispatch method using the registry to find a callable and
         then using the caller to call the callable. Very often this result
         in something like:

            dispatcher.dispatch('foo.bar', some_arg='value')

        Which then will trigger:

            do_stuff(some_arg='value')
    """
    # Declarative hooks to setup the registry, matcher and caller. Used in
    # the build_* methods as factories.
    registry_factory = None  # type: Callable[..., RegistryBase]
    caller_factory = CallerBase  # type: Callable[..., CallerBase]

    def __init__(
        self,
        registry_factory: Callable[..., RegistryBase]=None,
        caller_factory: Callable[..., CallerBase]=None,
    ):
        """Create a dispatcher with proper strategies.

        Args:
            registry_factory (Callable[RegistryBase], optional): how to
              build the registry object. You can also set registry_factory
              or implement build_registry() in a child class. Or override
              register() and match().
            caller_factory (Callable[CallerBase], optional): how to
              build the caller object. You can also set caller_factory
              or implement build_caller() in a child class. Or override
              call().
        """
        # Make sure we have at least one registry, matcher and caller object
        # as attributes. We try to get a factory from parameters and if we
        # can't we build it using self.build_* which by default tries to
        # use a factory defines in cls.*_factory. This allow the children
        # classes to override the registry, matcher and caller at any time
        # and in any way.

        if registry_factory:
            self.registry = registry_factory(self)
        else:
            self.registry = self.build_registry()

        if caller_factory:
            self.caller = caller_factory(self)
        else:
            self.caller = self.build_caller()

    def build_registry(self):
        if self.registry_factory:
            return self.registry_factory(self)
        return None

    def build_caller(self):
        if self.caller_factory:
            return self.caller_factory(self)
        return None

    def register(
        self,
        key: Any,
        callback: Callable,
    ):
        """Link a callable to a key.

        The way the callable is linked to a key depends of the implementation.

        Registering is delegating to the registry.

        Args:
            key (Any): the object allowing to find the callable when we later
                       trigger dispatching. Often a string. The convention
                       varies depending of the implementation.
            callback (Callable): the callable that may be called when
                                 dispatching using the matching key. Often
                                 a function.

        Return:
            None
        """
        try:
            return self.registry.register(key, callable)
        except AttributeError:
            if self.registry:
                raise
            raise NotImplementedError(
                'No strategy to register a callable. You must either:\n'
                '- override the register() method;\n'
                '- define registry_factory as class attribute;\n'
                '- pass a registry_factory to __init__;\n'
                '- override build_registry;\n'
            )

    def match(self, key: Any):
        """Return one or a group of callables matching the key.

        Matching is delegated to the self.registry object.

        Args:
            key (Any): An object that can be used to find matching callables
                       in the registry. Often it's a string.

        Return:
            A matching callable or a group of matching callables. The way
            the callables are grouped depends of the implementation, but
            will be most likely an iterable.
        """
        try:
            return self.registry.match(key)
        except AttributeError:
            if self.registry:
                raise
            raise NotImplementedError(
                'No strategy to match a callable. You must either:\n'
                '- override the match() method;\n'
                '- define registry_factory as class attribute;\n'
                '- pass a registry_factory to __init__;\n'
                '- override build_registry;\n'
            )

    def call(self, callables: Any):
        """Call the callable or group of callable.

        Calling is delegated to the self.matcher which choose the strategy.

        Args:
            callables (Any): Description

        Returns:
            Any: Whatever the caller choose to return.
        """
        return self.caller.call(callables)

    def dispatch(self, key: Any):
        """ Try to match callable(s) with the key then call them.

            Matching is delegated to the match() method.

            Calling is delegated to the call() method.

        Args:
            key (Any): Description

        Returns:
            Any: Whatever the self.call() choose to return. Which by default
                 what self.caller.call() choose to return.
        """
        # todo: deal with call() and match() not being implemented
        try:
            callables = self.match(key)
        except AttributeError:
            if self.registry:
                raise
            raise NotImplementedError(
                'No strategy to match a key. You must either:\n'
                '- override the match() method;\n'
                '- define registry_factory as class attribute;\n'
                '- pass a registry_factory to __init__;\n'
                '- override build_registry;\n'
            )
        return self.caller.call(callables)



# TODO: write ReversableDispatcher
