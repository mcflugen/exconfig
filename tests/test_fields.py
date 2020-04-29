import pytest

from exconfig import (
    BooleanField,
    Configuration,
    FloatField,
    IntegerField,
    ValidationError,
)


@pytest.mark.parametrize(
    "field,value",
    (
        (IntegerField, 42),
        (FloatField, 3.14),
        (BooleanField, True),
        (BooleanField, False),
    ),
)
def test_default(field, value):
    foo = field("foo", default=value).bind(Configuration(), "foo")
    foo.process(None)
    assert foo.data == value


@pytest.mark.parametrize(
    "field,value", ((IntegerField, 3.14), (FloatField, "pi"), (BooleanField, -1))
)
def test_wrong_type(field, value):
    with pytest.raises(ValidationError):
        field("foo", default=value).bind(Configuration(), "foo")
