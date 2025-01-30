from collections.abc import Callable, Coroutine
from functools import partial
from inspect import iscoroutinefunction
from typing import Any, TypeGuard

__all__ = ["AsyncCallable", "is_coroutine"]

type AsyncCallable[**P, R] = Callable[P, Coroutine[Any, Any, R]]


def is_coroutine[**P, R](
    fn: Callable[P, R] | Callable[P, Coroutine[Any, Any, R]], /
) -> TypeGuard[Callable[P, Coroutine[Any, Any, R]]]:
    if iscoroutinefunction(fn):
        return True

    if isinstance(fn, partial):
        return iscoroutinefunction(fn.func)

    call_method = getattr(fn, "__call__", None)  # noqa: B004
    return iscoroutinefunction(call_method)
