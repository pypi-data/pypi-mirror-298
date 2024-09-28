import abc
from asyncio import Lock
from dataclasses import dataclass
import dataclasses
from enum import IntFlag, auto
import functools
import types
import typing as t
from inspect import Signature, Parameter, isclass, iscoroutinefunction
from contextlib import asynccontextmanager


def is_lambda_function(obj):
    return isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>"


def is_context_manager(obj):
    return hasattr(obj, "__aenter__") and hasattr(obj, "__aexit__")


class ServiceLifetime(IntFlag):
    TRANSIENT = auto()
    SCOPED = auto()
    SINGLETON = auto()
    ONCE = SCOPED | SINGLETON


T = t.TypeVar("T")
U = t.TypeVar("U")


class DIException(Exception):
    pass


class CircularDependencyException(DIException):
    pass


class InstantiationException(DIException):
    pass


class DependencyResolutionContext:
    def __init__(self, container: "Container"):
        self._container = container
        self._chain: t.Set[t.Type] = set()
        self._stack = []

    def push(self, typ: t.Type[T]):
        if typ in self._chain:
            raise CircularDependencyException()

        self._chain.add(typ)
        self._stack.append(typ)

    def remove(self, typ: t.Type[T]):
        self._chain.remove(typ)

    def __call__(self, typ: t.Type):
        self.push(typ)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        elem = self._stack.pop()
        self._chain.remove(elem)


@dataclass
class ServiceProvider:
    base_type: t.Type
    concrete_type_or_factory: t.Type | t.Callable[..., t.Any]
    lifetime: ServiceLifetime
    instance: t.Any
    lock: Lock


class Container:
    PRIMITIVE_TYPES = (
        str,
        int,
    )

    def __init__(self, container: "Container" = None):
        self._registered_services: t.Dict[t.Any, list[ServiceProvider]] = {}
        self._pending_ctx_managers = []

        if container:
            for base_type, providers in container.registered_services.items():
                for provider in providers:
                    if provider.lifetime is ServiceLifetime.SINGLETON:
                        self._add_provider(base_type, provider)
                    else:
                        self._add_provider(
                            base_type, dataclasses.replace(provider, instance=None)
                        )

    def _add_provider(self, key: str | t.Type, provider: ServiceProvider):
        if providers := self._registered_services.get(key, None):
            providers.append(provider)
        else:
            self._registered_services[key] = [provider]

    def register(
        self,
        base_type: t.Type[T],
        concrete_type_or_factory: t.Type[U] | t.Callable[..., U] | t.Any,
        lifetime: ServiceLifetime,
    ):

        if lifetime not in ServiceLifetime.ONCE:
            if not callable(concrete_type_or_factory) and not isclass(
                concrete_type_or_factory
            ):
                raise DIException(
                    "Transient lifetime requires a callable or class type, not a instance."
                )

        service_provider = ServiceProvider(
            base_type, concrete_type_or_factory, lifetime, None, Lock()
        )

        self._add_provider(base_type, service_provider)
        self._add_provider(base_type.__name__, service_provider)

    @property
    def registered_services(self):
        return self._registered_services

    def _get_service_definition(
        self, name_or_type: str | t.Type
    ) -> ServiceProvider | None:
        return self._registered_services.get(name_or_type, None)

    def add_transient(self, typ, concrete_typ=None):
        return self.register(typ, concrete_typ or typ, ServiceLifetime.TRANSIENT)

    def add_scoped(self, typ, concrete_typ=None):
        return self.register(typ, concrete_typ or typ, ServiceLifetime.SCOPED)

    def add_singleton(self, typ, concrete_typ=None):
        return self.register(typ, concrete_typ or typ, ServiceLifetime.SINGLETON)

    def create_scope(self):
        scoped_container = Container(self)
        return scoped_container

    @asynccontextmanager
    async def scoped(self):
        scope = self.create_scope()
        yield scope
        await scope.close()

    def extract_depedencies(self, callable_: t.Callable[..., t.Any]):
        signature = Signature.from_callable(callable_)

        dependencies = {}
        for param_name, param in signature.parameters.items():
            if param.annotation is Parameter.empty:
                continue
            dependencies[param_name] = param.annotation
        return dependencies

    async def _resolve(
        self,
        desired_type_or_callable: t.Type[T] | t.Callable[..., T],
        context: DependencyResolutionContext,
        strict: bool = True,
    ) -> T | list[T] | None:

        if desired_type_or_callable is self.__class__:
            return self  # type: ignore

        desired_type = desired_type_or_callable

        # Discover which type is gonna be instantiated.
        providers = self._get_service_definition(desired_type)

        if providers is None or len(providers) == 0:
            if strict:
                type_name = (
                    desired_type
                    if isinstance(desired_type, str)
                    else desired_type.__name__
                )
                raise DIException(f"Type {type_name} could not be resolved.")
            return None

        async def _resolve_provider(provider):

            concrete_type_or_callable = provider.concrete_type_or_factory
            lifetime = provider.lifetime

            factory = concrete_type = concrete_type_or_callable

            if not isclass(concrete_type_or_callable) and callable(
                concrete_type_or_callable
            ):
                if is_lambda_function(concrete_type_or_callable):
                    concrete_type = desired_type
                else:
                    sig = Signature.from_callable(concrete_type_or_callable)
                    if (
                        not sig.return_annotation
                        or sig.return_annotation is Signature.empty
                    ):
                        raise DIException(
                            "Callable is not a lambda function AND has not return type."
                        )
                    concrete_type = sig.return_annotation

                factory = concrete_type_or_callable

            # Push the concrete type to the context chain, prevent circular dependency loop.
            with context(concrete_type):
                if lifetime in ServiceLifetime.ONCE:
                    await provider.lock.acquire()
                    if provider.instance is not None:
                        provider.lock.release()
                        return provider.instance

                kwargs = {}

                if isclass(factory):
                    dependencies = self.extract_depedencies(factory.__init__)
                elif callable(factory):
                    dependencies = self.extract_depedencies(factory)
                else:
                    dependencies = {}

                for key, typ in dependencies.items():
                    if typ in self.PRIMITIVE_TYPES:
                        continue
                    resolved = await self._resolve(typ, context)
                    if resolved is None:
                        continue
                    kwargs[key] = resolved

                if iscoroutinefunction(factory):
                    instance = await factory(**kwargs)
                elif callable(factory):
                    instance = factory(**kwargs)
                    if is_context_manager(instance):
                        self._pending_ctx_managers.append(instance)
                        instance = await instance.__aenter__()
                else:
                    instance = factory

                if lifetime in ServiceLifetime.ONCE:
                    provider.instance = instance
                    provider.lock.release()

                return instance

        if len(providers) > 1:
            return [await _resolve_provider(provider) for provider in providers]

        return await _resolve_provider(providers[0])

    async def get(self, desired_type: t.Type[T]) -> T:
        return await self.resolve(desired_type, True)  # type: ignore

    async def try_get(self, desired_type: t.Type[T]) -> T | None:
        return await self.resolve(desired_type, False)

    async def resolve(self, desired_type: t.Type[T], strict: bool = True) -> T | None:
        context = DependencyResolutionContext(self)
        return await self._resolve(desired_type, context, strict)

    async def get_executor(
        self, callable_: t.Callable[..., T], strict: bool = True
    ) -> t.Callable[..., T]:
        dependencies = self.extract_depedencies(callable_)
        context = DependencyResolutionContext(self)
        kwargs = {}
        for key, typ in dependencies.items():
            if typ in self.PRIMITIVE_TYPES:
                continue

            resolved = await self._resolve(typ, context, strict)
            if resolved is None:
                continue

            kwargs[key] = resolved

        return functools.partial(callable_, **kwargs)

    async def close(self):
        for ctx_manager in self._pending_ctx_managers:
            await ctx_manager.__aexit__(None, None, None)
        self._pending_ctx_managers.clear()
