from collections.abc import Callable
from functools import wraps
from typing import NoReturn, overload

from app.utils.types import AsyncCallable, is_coroutine


class ExceptionManager[T]:
    def __init__(self) -> None:
        self._exception_handlers: dict[type[Exception], Callable[[Exception], T]] = {}

    def register[E: Exception](
        self, exception_type: type[E]
    ) -> Callable[[Callable[[E], T]], Callable[[E], T]]:
        def decorator(func: Callable[[E], T]) -> Callable[[E], T]:
            self._exception_handlers[exception_type] = func  # pyright: ignore [reportArgumentType]
            return func

        return decorator

    def handle(self, exception: Exception, /) -> T:
        exception_handler = self._exception_handlers.get(type(exception))
        if exception_handler is None:
            raise exception

        return exception_handler(exception)

    @overload
    def __call__[**P, R](
        self: "ExceptionManager[NoReturn]", fn: AsyncCallable[P, R], /
    ) -> AsyncCallable[P, R]: ...

    @overload
    def __call__[**P, R](
        self: "ExceptionManager[NoReturn]", fn: Callable[P, R], /
    ) -> Callable[P, R]: ...

    @overload
    def __call__[**P](self, fn: AsyncCallable[P, T], /) -> AsyncCallable[P, T]: ...

    @overload
    def __call__[**P](self, fn: Callable[P, T], /) -> Callable[P, T]: ...

    def __call__[**P, R](
        self, fn: Callable[P, T] | AsyncCallable[P, T], /
    ) -> Callable[P, T | R] | AsyncCallable[P, T | R]:
        if is_coroutine(fn):

            @wraps(fn)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                try:
                    return await fn(*args, **kwargs)
                except Exception as exc:
                    return self.handle(exc)

            return async_wrapper

        @wraps(fn)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return fn(*args, **kwargs)  # pyright: ignore[reportReturnType]
            except Exception as exc:
                return self.handle(exc)

        return sync_wrapper
