import builtins
import datetime
from typing import (
    Any,
    Callable,
    Coroutine,
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
    TypeVar,
    cast,
)

from streamable.iters import (
    AsyncConcurrentMappingIterable,
    CatchingIterator,
    ConcurrentFlatteningIterable,
    FlatteningIterator,
    GroupingByIterator,
    GroupingIterator,
    ObservingIterator,
    RaisingIterator,
    ThreadConcurrentMappingIterable,
    ThrottlingIntervalIterator,
    ThrottlingPerSecondIterator,
    TruncatingOnCountIterator,
    TruncatingOnPredicateIterator,
)

T = TypeVar("T")
U = TypeVar("U")

from streamable.util import (
    NO_REPLACEMENT,
    NoopStopIteration,
    reraise_as,
    validate_concurrency,
    validate_group_interval,
    validate_group_size,
    validate_iterator,
    validate_throttle_interval,
    validate_throttle_per_second,
    validate_truncate_args,
)


def catch(
    iterator: Iterator[T],
    kind: Type[Exception] = Exception,
    when: Callable[[Exception], Any] = bool,
    replacement: T = NO_REPLACEMENT,  # type: ignore
    finally_raise: bool = False,
) -> Iterator[T]:
    validate_iterator(iterator)
    return CatchingIterator(
        iterator,
        kind,
        when,
        replacement,
        finally_raise=finally_raise,
    )


def flatten(iterator: Iterator[Iterable[T]], concurrency: int = 1) -> Iterator[T]:
    validate_iterator(iterator)
    validate_concurrency(concurrency)
    if concurrency == 1:
        return FlatteningIterator(iterator)
    else:
        return RaisingIterator(
            iter(
                ConcurrentFlatteningIterable(
                    iterator,
                    concurrency=concurrency,
                    buffer_size=concurrency,
                )
            )
        )


def group(
    iterator: Iterator[T],
    size: Optional[int] = None,
    interval: Optional[datetime.timedelta] = None,
    by: Optional[Callable[[T], Any]] = None,
) -> Iterator[List[T]]:
    validate_iterator(iterator)
    validate_group_size(size)
    validate_group_interval(interval)
    if size is None:
        size = cast(int, float("inf"))
    if interval is None:
        interval_seconds = float("inf")
    else:
        interval_seconds = interval.total_seconds()
    if by is not None:
        by = reraise_as(by, StopIteration, NoopStopIteration)
        return GroupingByIterator(iterator, size, interval_seconds, by)
    return GroupingIterator(iterator, size, interval_seconds)


def map(
    transformation: Callable[[T], U], iterator: Iterator[T], concurrency: int = 1
) -> Iterator[U]:
    validate_iterator(iterator)
    validate_concurrency(concurrency)
    transformation = reraise_as(transformation, StopIteration, NoopStopIteration)
    if concurrency == 1:
        return builtins.map(transformation, iterator)
    else:
        return RaisingIterator(
            iter(
                ThreadConcurrentMappingIterable(
                    iterator,
                    transformation,
                    concurrency=concurrency,
                    buffer_size=concurrency,
                )
            )
        )


def amap(
    transformation: Callable[[T], Coroutine[Any, Any, U]],
    iterator: Iterator[T],
    concurrency: int = 1,
) -> Iterator[U]:
    validate_iterator(iterator)
    validate_concurrency(concurrency)
    return RaisingIterator(
        iter(
            AsyncConcurrentMappingIterable(
                iterator,
                transformation,
                buffer_size=concurrency,
            )
        )
    )


def observe(iterator: Iterator[T], what: str) -> Iterator[T]:
    validate_iterator(iterator)
    return ObservingIterator(iterator, what)


def throttle(
    iterator: Iterator[T],
    per_second: int = cast(int, float("inf")),
    interval: datetime.timedelta = datetime.timedelta(0),
) -> Iterator[T]:
    validate_iterator(iterator)
    validate_throttle_per_second(per_second)
    validate_throttle_interval(interval)

    if per_second < float("inf"):
        iterator = ThrottlingPerSecondIterator(iterator, per_second)
    if interval > datetime.timedelta(0):
        iterator = ThrottlingIntervalIterator(iterator, interval.total_seconds())
    return iterator


def truncate(
    iterator: Iterator[T],
    count: Optional[int] = None,
    when: Optional[Callable[[T], Any]] = None,
) -> Iterator[T]:
    validate_iterator(iterator)
    validate_truncate_args(count, when)
    if count is not None:
        iterator = TruncatingOnCountIterator(iterator, count)
    if when is not None:
        iterator = TruncatingOnPredicateIterator(iterator, when)
    return iterator
