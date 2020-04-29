import os

import pytest

from exconfig import ValidationError
from exconfig.validators import Length, OneOf, Path, Range


@pytest.mark.parametrize("lower", [None, 0, 0.0, 1.0])
@pytest.mark.parametrize("upper", [None, 1, 1.0, 10])
def test_range_is_valid(lower, upper):
    validate = Range(lower=lower, upper=upper)
    validate(None, 1.0)


@pytest.mark.parametrize("lower", [1.0 + 1e-12, 2])
@pytest.mark.parametrize("upper", [1.0 - 1e-12, 0.5])
def test_range_is_not_valid(lower, upper):
    validate = Range(lower=lower, upper=upper)
    with pytest.raises(ValidationError):
        validate(None, 1.0)


@pytest.mark.parametrize("lower", [None, 0, 1, 3])
@pytest.mark.parametrize("upper", [None, 3, 10])
@pytest.mark.parametrize(
    "iterator",
    [(1, 2, 3), [1, 2, 3], set([1, 2, 3]), {"foo": 1, "bar": 2, "baz": 3}, "123"],
)
def test_length_is_value(iterator, lower, upper):
    validate = Length(lower=lower, upper=upper)
    validate(None, iterator)


@pytest.mark.parametrize(
    "iterator",
    [(1, 2, 3), [1, 2, 3], set([1, 2, 3]), {"foo": 1, "bar": 2, "baz": 3}, "123"],
)
def test_length_is_too_short(iterator):
    validate = Length(lower=4, upper=None)
    with pytest.raises(ValidationError):
        validate(None, iterator)


@pytest.mark.parametrize(
    "iterator",
    [(1, 2, 3), [1, 2, 3], set([1, 2, 3]), {"foo": 1, "bar": 2, "baz": 3}, "123"],
)
def test_length_is_too_long(iterator):
    validate = Length(lower=None, upper=2)
    with pytest.raises(ValidationError):
        validate(None, iterator)


@pytest.mark.parametrize(
    "choices",
    [
        ("foo", "bar", "baz"),
        ["foo", "bar", "baz"],
        set(["foo", "bar", "baz"]),
        "foobarbaz",
    ],
)
def test_oneof(choices):
    validate = OneOf(choices=choices)
    validate(None, "bar")


@pytest.mark.parametrize("choices", [(), ("foo", "baz")])
def test_not_oneof(choices):
    validate = OneOf(choices=choices)
    with pytest.raises(ValidationError):
        validate(None, "bar")


@pytest.mark.parametrize("file_okay", [True, False])
@pytest.mark.parametrize("dir_okay", [True, False])
@pytest.mark.parametrize("exists", [True, False])
def test_path_to_existing_file(tmpdir, file_okay, dir_okay, exists):
    with tmpdir.as_cwd():
        with open("test.txt", "w") as fp:
            print("empty file", file=fp)
        if file_okay and exists:
            Path(file_okay=file_okay, dir_okay=dir_okay, exists=exists)(
                None, "test.txt"
            )
        else:
            with pytest.raises(ValidationError):
                Path(file_okay=file_okay, dir_okay=dir_okay, exists=exists)(
                    None, "test.txt"
                )


@pytest.mark.parametrize("file_okay", [True, False])
@pytest.mark.parametrize("dir_okay", [True, False])
@pytest.mark.parametrize("exists", [True, False])
def test_path_to_existing_dir(tmpdir, file_okay, dir_okay, exists):
    if dir_okay and exists:
        Path(file_okay=file_okay, dir_okay=dir_okay, exists=exists)(None, tmpdir)
    else:
        with pytest.raises(ValidationError):
            Path(file_okay=file_okay, dir_okay=dir_okay, exists=exists)(None, tmpdir)


@pytest.mark.parametrize("file_okay", [True, False])
@pytest.mark.parametrize("dir_okay", [True, False])
@pytest.mark.parametrize("exists", [True, False])
def test_path_to_missing_file_or_dir(tmpdir, file_okay, dir_okay, exists):
    if exists:
        with pytest.raises(ValidationError):
            Path(file_okay=file_okay, dir_okay=dir_okay, exists=exists)(
                None, "test.txt"
            )
    else:
        Path(file_okay=file_okay, dir_okay=dir_okay, exists=exists)(None, "test.txt")
