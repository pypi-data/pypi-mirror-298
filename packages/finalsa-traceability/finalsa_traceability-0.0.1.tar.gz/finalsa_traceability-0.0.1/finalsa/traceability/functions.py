from uuid import uuid4
import string
import random


HTTP_HEADER_CORRELATION_ID = "X-Correlation-ID"
HTTP_HEADER_TRACE_ID = "X-Trace-ID"
HTTP_HEADER_SPAN_ID = "X-Span-ID"

ASYNC_CONTEXT_CORRELATION_ID = "correlation_id"
ASYNC_CONTEXT_TRACE_ID = "trace_id"
ASYNC_CONTEXT_SPAN_ID = "span_id"


def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def default_correlation_id(
    service_name: str = "DEFAULT",
) -> str:
    return f"{service_name}-{id_generator()}"


def default_span_id() -> str:
    return str(uuid4())


def default_trace_id() -> str:
    return str(uuid4())


def add_hope_to_correlation(
    correlation_id: str,
) -> str:
    hope = id_generator()
    return f"{correlation_id}-{hope}"
