from collections.abc import AsyncGenerator, Awaitable, Callable, Iterator
from dataclasses import dataclass, field
from typing import Self

type MiddlewareResult[T] = AsyncGenerator[None, T | None]
type Middleware[**P, T] = Callable[P, MiddlewareResult[T]]


@dataclass(eq=False, frozen=True, slots=True)
class MiddlewareGroup[**P, T]:
    __middlewares: list[Middleware[P, T]] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    @property
    def __stack(self) -> Iterator[Middleware[P, T]]:
        return iter(self.__middlewares)

    def add(self, *middlewares: Middleware[P, T]) -> Self:
        self.__middlewares.extend(middlewares)
        return self

    async def invoke(
        self,
        handler: Callable[P, Awaitable[T]],
        /,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T | None:
        return await self.__apply_stack(handler, self.__stack)(*args, **kwargs)

    @classmethod
    def __apply_middleware(
        cls,
        handler: Callable[P, Awaitable[T | None]],
        middleware: Middleware[P, T],
    ) -> Callable[P, Awaitable[T | None]]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
            generator: MiddlewareResult[T] = middleware(*args, **kwargs)
            value: T | None = None

            try:
                await anext(generator)

                try:
                    value = await handler(*args, **kwargs)
                except BaseException as exc:
                    await generator.athrow(exc)
                else:
                    await generator.asend(value)

            except StopAsyncIteration:
                ...

            finally:
                await generator.aclose()

            return value

        return wrapper

    @classmethod
    def __apply_stack(
        cls,
        handler: Callable[P, Awaitable[T | None]],
        stack: Iterator[Middleware[P, T]],
    ) -> Callable[P, Awaitable[T | None]]:
        for middleware in stack:
            new_handler = cls.__apply_middleware(handler, middleware)
            return cls.__apply_stack(new_handler, stack)

        return handler
