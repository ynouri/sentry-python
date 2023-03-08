from functools import wraps

import sentry_sdk
from sentry_sdk._types import TYPE_CHECKING
from sentry_sdk.tracing_utils import _get_running_span_or_transaction
from sentry_sdk.consts import OP
from sentry_sdk.utils import logger, qualname_from_function


if TYPE_CHECKING:
    from typing import Any


def start_child_span_decorator(func):
    # type: (Any) -> Any
    """
    Decorator to add child spans for functions.

    This is the Python 2 compatible version of the decorator.
    Duplicated code from ``sentry_sdk.tracing_utils_python3.start_child_span_decorator``.

    See also ``sentry_sdk.tracing.trace()``.
    """

    @wraps(func)
    def func_with_tracing(*args, **kwargs):
        # type: (*Any, **Any) -> Any

        span_or_trx = _get_running_span_or_transaction(sentry_sdk.Hub.current)

        if span_or_trx is None:
            logger.warning(
                "No transaction found. Not creating a child span for %s. "
                "Please start a Sentry transaction before calling this function.",
                qualname_from_function(func),
            )
            return func(*args, **kwargs)

        with span_or_trx.start_child(
            op=OP.FUNCTION,
            description=qualname_from_function(func),
        ):
            return func(*args, **kwargs)

    return func_with_tracing
