from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, List, Literal, Optional, TypeVar

from typing_extensions import ParamSpec

from morph.task.utils.knowledge.inspection import (
    MorphKnowledgeMetaObjectGlossaryTerm,
    MorphKnowledgeMetaObjectSchema,
)

from .state import MorphFunctionMetaObject, MorphGlobalContext

Param = ParamSpec("Param")
RetType = TypeVar("RetType")
F = TypeVar("F", bound=Callable)


def _get_morph_function_id(func: Callable) -> str:
    if hasattr(func, "__morph_fid__"):
        return str(func.__morph_fid__)
    else:
        filename = inspect.getfile(func)
        function_name = func.__name__
        new_fid = f"{filename}:{function_name}"
        func.__morph_fid__ = new_fid  # type: ignore
        return new_fid


def _attribute_wrapper(func: F, fid: str) -> F:
    context = MorphGlobalContext.get_instance()
    func.__morph_fid__ = fid  # type: ignore
    meta_obj = MorphFunctionMetaObject(
        id=fid,
        name=func.__name__,
        function=func,
        description=None,
        title=None,
        schemas=None,
        terms=None,
        arguments=[],
        data_requirements=[],
        output_paths=[],
        output_type=None,
        connection=None,
    )
    context.update_meta_object(fid, meta_obj)
    return func


def func(
    name: str | None = None,
    description: str | None = None,
    title: str | None = None,
    schemas: list[MorphKnowledgeMetaObjectSchema] | None = None,
    terms: list[MorphKnowledgeMetaObjectGlossaryTerm] | None = None,
    output_paths: list[str] | None = None,
    output_type: Optional[
        Literal["dataframe", "csv", "visualization", "markdown", "json"]
    ] = None,
    **kwargs: dict[str, Any],
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    context = MorphGlobalContext.get_instance()

    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        fid = _get_morph_function_id(func)

        arg_value = kwargs.get("arguments", [])  # type: ignore
        arguments: List[str] = arg_value if isinstance(arg_value, list) else []

        data_req_value = kwargs.get("data_requirements", [])  # type: ignore
        data_requirements: List[str] = (
            data_req_value if isinstance(data_req_value, list) else []
        )

        connection = kwargs.get("connection")
        if not isinstance(connection, (str, type(None))):
            connection = None

        meta_obj = MorphFunctionMetaObject(
            id=fid,
            name=name or func.__name__,
            function=func,
            description=description,
            title=title,
            schemas=schemas,
            terms=terms,
            arguments=arguments,
            data_requirements=data_requirements,
            output_paths=output_paths or ["_private/{name}/{now()}{ext()}"],
            output_type=output_type,
            connection=connection,
        )
        context.update_meta_object(fid, meta_obj)

        @wraps(func)
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            return func(*args, **kwargs)

        return wrapper
        # return _attribute_wrapper(wrapper, fid)

    # check if decorator is called with args
    if callable(name):
        func = name  # type: ignore
        name = func.__name__
        description = None
        return decorator(func)

    return decorator


def argument(
    var_name: str,
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    context = MorphGlobalContext.get_instance()

    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        fid = _get_morph_function_id(func)
        meta = context.search_meta_object(fid)
        if meta and meta.arguments:
            context.update_meta_object(
                fid,
                MorphFunctionMetaObject(
                    id=fid,
                    name=meta.name,
                    function=meta.function,
                    description=meta.description,
                    title=meta.title,
                    schemas=meta.schemas,
                    terms=meta.terms,
                    arguments=meta.arguments + [var_name],
                    data_requirements=meta.data_requirements,
                    output_paths=meta.output_paths,
                    output_type=meta.output_type,
                    connection=meta.connection,
                ),
            )
        else:
            context.update_meta_object(
                fid,
                MorphFunctionMetaObject(
                    id=fid,
                    name=func.__name__,
                    function=func,
                    description=None,
                    title=None,
                    schemas=None,
                    terms=None,
                    arguments=[var_name],
                    data_requirements=None,
                    output_paths=None,
                    output_type=None,
                    connection=None,
                ),
            )

        @wraps(func)
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            return func(*args, **kwargs)

        return wrapper
        # return _attribute_wrapper(wrapper, fid)

    return decorator


def load_data(
    name: str,
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    context = MorphGlobalContext.get_instance()

    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        fid = _get_morph_function_id(func)
        meta = context.search_meta_object(fid)
        if meta and meta.data_requirements:
            context.update_meta_object(
                fid,
                MorphFunctionMetaObject(
                    id=fid,
                    name=meta.name,
                    function=meta.function,
                    description=meta.description,
                    title=meta.title,
                    schemas=meta.schemas,
                    terms=meta.terms,
                    arguments=meta.arguments,
                    data_requirements=meta.data_requirements + [name],
                    output_paths=meta.output_paths,
                    output_type=meta.output_type,
                    connection=meta.connection,
                ),
            )
        else:
            context.update_meta_object(
                fid,
                MorphFunctionMetaObject(
                    id=fid,
                    name=func.__name__,
                    function=func,
                    description=None,
                    title=None,
                    schemas=None,
                    terms=None,
                    arguments=None,
                    data_requirements=[name],
                    output_paths=None,
                    output_type=None,
                    connection=None,
                ),
            )

        @wraps(func)
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            return func(*args, **kwargs)

        return wrapper
        # return _attribute_wrapper(wrapper, fid)

    return decorator
