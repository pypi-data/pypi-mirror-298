from finalsa.traceability.functions import (
    default_correlation_id, default_span_id,
    default_trace_id, add_hope_to_correlation
)
from contextvars import ContextVar
from typing import Optional

correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)
trace_id: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
span_id: ContextVar[Optional[str]] = ContextVar('span_id', default=None)


def get_correlation_id() -> Optional[str]:
    return correlation_id.get()


def set_correlation_id(
    value: Optional[str] = None,
    service_name: Optional[str] = None,
):
    if value is None:
        value = default_correlation_id(
            service_name
        )
    else:
        value = add_hope_to_correlation(
            value
        )
    correlation_id.set(value)


def get_trace_id() -> Optional[str]:
    return trace_id.get()


def set_trace_id(value: Optional[str] = None):
    if value is None:
        value = default_trace_id()
    trace_id.set(value)


def get_span_id() -> Optional[str]:
    return span_id.get()


def set_span_id(value: Optional[str] = None):
    if value is None:
        value = default_span_id()
    span_id.set(value)


def set_context(
    correlation_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    service_name: Optional[str] = None,
):
    set_correlation_id(correlation_id, service_name)
    set_trace_id(trace_id)
    set_span_id(span_id)


def set_context_from_dict(
    context: dict,
    service_name: Optional[str] = None,
):
    set_context(
        context.get('correlation_id'),
        context.get('trace_id'),
        context.get('span_id'),
        service_name
    )
