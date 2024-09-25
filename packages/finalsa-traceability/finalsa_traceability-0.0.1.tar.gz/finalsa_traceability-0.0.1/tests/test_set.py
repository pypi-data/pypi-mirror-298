from finalsa.traceability import (
    correlation_id,
    trace_id,
    span_id,
    id_generator,
    default_correlation_id,
    default_span_id,
    default_trace_id,
    set_span_id,
    set_trace_id,
    set_correlation_id,
    set_context,
    set_context_from_dict,
    get_correlation_id,
    get_trace_id,
    get_span_id,
    __version__,
    __all__,
)


def test__version__():
    assert __version__ == "0.0.1"


def test__all__():
    assert __all__ == [
        "correlation_id",
        "trace_id",
        "span_id",
        "id_generator",
        "default_correlation_id",
        "default_span_id",
        "default_trace_id",
        "set_span_id",
        "set_trace_id",
        "set_correlation_id",
        "set_context",
        "set_context_from_dict",
        "get_correlation_id",
        "get_trace_id",
        "get_span_id",
    ]


def test_correlation_id():
    assert correlation_id.get() == None
    correlation_id.set("123")
    assert correlation_id.get() == "123"


def test_trace_id():
    assert trace_id.get() == None
    trace_id.set("123")
    assert trace_id.get() == "123"


def test_span_id():
    assert span_id.get() == None
    span_id.set("123")
    assert span_id.get() == "123"


def test_id_generator():
    assert id_generator() != id_generator()
    assert len(id_generator()) == 4
    assert id_generator(10) != id_generator(10)
    assert len(id_generator(10)) == 10


def test_default_correlation_id():
    assert default_correlation_id() != default_correlation_id()
    default_with_name = default_correlation_id("service")
    assert default_with_name.startswith("service-")

    default_without_name = default_correlation_id()
    assert default_without_name.startswith("DEFAULT-")


def test_default_span_id():
    assert default_span_id() != default_span_id()
    assert len(default_span_id()) == 36


def test_default_trace_id():
    assert default_trace_id() != default_trace_id()
    assert len(default_trace_id()) == 36


def test_set_span_id():
    set_span_id("123")
    assert span_id.get() == "123"


def test_set_trace_id():
    set_trace_id("123")
    assert trace_id.get() == "123"


def test_set_correlation_id():
    set_correlation_id("123")
    value = correlation_id.get()
    assert value.startswith("123-")
    set_correlation_id(
        service_name="service")
    value = correlation_id.get()
    assert value.startswith("service-")


def test_set_context():
    set_context(correlation_id="123", trace_id="123", span_id="123")
    assert correlation_id.get().startswith("123-")
    assert trace_id.get() == "123"
    assert span_id.get() == "123"


def test_set_context_from_dict():
    set_context_from_dict({
        "correlation_id": "123",
        "trace_id": "123",
        "span_id": "123",
    })
    assert correlation_id.get().startswith("123-")
    assert trace_id.get() == "123"
    assert span_id.get() == "123"


def test_set_context_from_dict_empty():
    set_context_from_dict({
    }, "service")
    assert correlation_id.get().startswith("service-")
    assert trace_id.get() != None
    assert span_id.get() != None
    assert span_id.get() != ""
    assert trace_id.get() != ""


def test_get_correlation_id():
    set_correlation_id("123")
    assert get_correlation_id() == correlation_id.get()

def test_get_trace_id():
    set_trace_id("123")
    assert get_trace_id() == trace_id.get()
    
def test_get_span_id():
    set_span_id("123")
    assert get_span_id() == span_id.get()
    
def test_get_correlation_id_none():
    correlation_id.set(None)
    assert get_correlation_id() == None
    