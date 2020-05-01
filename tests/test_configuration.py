import pytest

from exconfig import Configuration, IntegerField, FloatField


def test_non_defaults(tmpdir):
    class ExampleConfiguration(Configuration):
        int_field = IntegerField("int_field", default=50)
        float_field = FloatField("float_field", default=50.0)

    with tmpdir.as_cwd():
        with open("test.yaml", "w") as fp:
            print("int_field: 5000", file=fp)
        config = ExampleConfiguration.from_yaml("test.yaml")

    assert config["int_field"].data == 5000
    assert config["float_field"].data == pytest.approx(50.0)
