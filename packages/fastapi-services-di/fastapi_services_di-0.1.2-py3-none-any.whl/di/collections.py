import inspect
from types import UnionType, NoneType
from typing import TypeVar, Union, get_origin, get_args, Annotated, ParamSpec, override

from fastapi import params, Depends, Request, Response

T = TypeVar("T")
Params = ParamSpec("Params")
RETURN_TYPE = TypeVar("RETURN_TYPE")
RETURN_NONE = lambda: None  # noqa: E731


class NoServiceRegistered(Exception):
    def __init__(self, __t):
        super().__init__(f"No service for type '{__t}' has been registered.")


def singleton(cls, *args: Params.args, **kwargs: Params.kwargs):
    instance = getattr(cls, "__instance__", None)
    if instance is None:
        instance = object.__new__(cls)
        setattr(cls, "__instance__", instance)
    return instance


class Dependency:
    def __init__(self, factory):
        self.factory = factory

    def build(self):
        pass


class SingletonDependency(Dependency):
    @override
    def build(self):
        self.factory.__new__ = singleton
        return self.factory


class ScopedDependency(Dependency):
    pass


class ServiceCollection:
    __slots__ = ("__container",)

    def __init__(self):
        self.__container: dict[type, Dependency] = {}

    def __add(self, service_type, factory):
        self.__container[service_type] = factory

    def add_scoped(self, service_type: type[T], implementation_type: type[T] | None = None) -> None:
        self.__add(service_type, ScopedDependency(implementation_type or service_type))

    def add_singleton(self, service_type: type[T], implementation_type: type[T] | None = None) -> None:
        self.__add(service_type, SingletonDependency(implementation_type or service_type))

    def add_instance(self, service_type: type[T], instance: T) -> None:
        self.__add(service_type, SingletonDependency(lambda: instance))

    def build(self):
        for serv in self.__container:
            self.resolve(serv)

    def resolve(self, __t):
        dependency = self.__container[__t]
        sig = inspect.signature(dependency.factory)
        parameters = []

        for p in sig.parameters.values():
            hint = p.annotation

            if hint in (Request, Response,):
                parameters.append(p)
                continue

            if depends := self.__container.get(hint):
                parameters.append(p.replace(annotation=Annotated[p.annotation, Depends(depends.factory)]))
                continue

            origin = get_origin(hint)
            args = get_args(hint)

            if origin:
                if origin is Annotated and isinstance(args[1], params.Depends):
                    parameters.append(p)
                    continue

                if origin in (Union, UnionType,):
                    set_parameter = False

                    for hint in args:
                        if depends := self.__container.get(hint):
                            parameters.append(p.replace(annotation=Annotated[p.annotation, Depends(depends.factory)]))
                            set_parameter = True
                            break

                    if not set_parameter:
                        if NoneType not in args:
                            raise NoServiceRegistered(hint)

                        parameters.append(p.replace(annotation=Annotated[p.annotation, Depends(RETURN_NONE)]))
                    continue

                if depends := self.__container.get(origin):
                    parameters.append(p.replace(annotation=Annotated[p.annotation, Depends(depends.factory)]))
                    continue

                raise NoServiceRegistered(hint)

        dependency.factory.__signature__ = sig.replace(parameters=parameters)
        dependency.build()
        return dependency.factory
