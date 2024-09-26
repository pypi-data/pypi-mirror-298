import re
from itertools import combinations
from typing import Optional

import numpy as np
import pytest

from nonos.api._angle_parsing import _parse_planet_file, _parse_rotation_angle
from nonos.parsing import (
    parse_image_format,
    parse_output_number_range,
    parse_range,
    range_converter,
    userval_or_default,
)


@pytest.mark.parametrize(
    "received, expected",
    [
        (("val", "default"), "val"),
        (("unset", "default"), "default"),
        ((None, "default"), "default"),
        (("unset", None), None),
        ((None, None), None),
    ],
)
def test_userval_or_default(received, expected):
    userval, default = received
    assert userval_or_default(userval, default=default) == expected


@pytest.mark.parametrize(
    "received, expected",
    [
        (1, [1]),
        (0, [0]),
        ([1], [1]),
        ([0, 1], [0, 1]),
        ([0, 2], [0, 1, 2]),
        ([0, 5], [0, 1, 2, 3, 4, 5]),
        ([10, 20, 5], [10, 15, 20]),
        ([0, 299, 50], [0, 50, 100, 150, 200, 250]),
    ],
)
def test_range_outputs(received, expected):
    assert parse_output_number_range(received) == expected


def test_from_maxval():
    maxval = 1.0
    assert parse_output_number_range(None, maxval=maxval) == [maxval]


def test_unparseable_data():
    with pytest.raises(
        ValueError, match="Can't parse a range from unset values without a max."
    ):
        parse_output_number_range("unset")


def test_invalid_request():
    with pytest.raises(
        ValueError, match="No output beyond 5 is available, but 10 was requested."
    ):
        parse_output_number_range([1, 10], maxval=5)


def test_invalid_nargs():
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Can't parse a range from sequence [1, 2, 3, 4] with more than 3 values."
        ),
    ):
        parse_output_number_range([1, 2, 3, 4])


@pytest.mark.parametrize(
    "dim, extent",
    [
        (2, ("0.4", "8", "0", "-0.2", "0.2")),
        (1, (0.4, 8, 0.2)),
    ],
)
def test_invalid_nargs_parse_range(dim, extent):
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"Received sequence `extent` with incorrect size {len(extent)}. Expected exactly {2*dim=} values."
        ),
    ):
        parse_range(extent, dim)


@pytest.mark.parametrize(
    "received",
    [
        [1, 0],
        [1, 0, 1],
        [1, 0, 2],
    ],
)
def test_invalid_range(received):
    with pytest.raises(ValueError, match="Can't parse a range with max < min."):
        parse_output_number_range(received)


@pytest.mark.parametrize(
    "abscissa, ordinate, dim, expected",
    [
        (
            np.linspace(0.2, 10, 100),
            np.linspace(-np.pi, np.pi, 100),
            2,
            (0.2, 10.0, -np.pi, np.pi),
        ),
        (np.linspace(0.2, 10, 100), np.zeros(2), 1, (0.2, 10.0)),
    ],
)
def test_parse_range(abscissa, ordinate, dim, expected):
    extent1 = parse_range("unset", dim=dim)
    assert range_converter(extent1, abscissa=abscissa, ordinate=ordinate) == expected
    extent2 = parse_range(("0.5", "5", "-0.2", "0.2"), dim=2)
    assert range_converter(
        extent2,
        abscissa=np.linspace(0.2, 10, 100),
        ordinate=np.linspace(-0.4, 0.4, 100),
    ) == (0.5, 5, -0.2, 0.2)
    extent3 = parse_range(("0.4", "9.5"), dim=1)
    assert range_converter(
        extent3, abscissa=np.linspace(0.2, 10, 100), ordinate=np.zeros(2)
    ) == (0.4, 9.5)
    extent4 = parse_range(("0.5", "x", "-0.2", "x"), dim=2)
    assert extent4 == (0.5, None, -0.2, None)
    assert range_converter(
        extent4,
        abscissa=np.linspace(0.2, 10, 100),
        ordinate=np.linspace(-0.4, 0.4, 100),
    ) == (0.5, 10.0, -0.2, 0.4)


def test_range_converter_error():
    with pytest.raises(
        TypeError,
        match="Expected extent to be of lenght 2 or 4,",
    ):
        range_converter(extent=[], abscissa=None, ordinate=None)


@pytest.mark.parametrize(
    "received, expected",
    [
        (".png", "png"),
        (".pdf", "pdf"),
        ("png", "png"),
        ("pdf", "pdf"),
    ],
)
def test_image_format(received, expected):
    assert parse_image_format(received) == expected


@pytest.mark.parametrize("received", ["unset", None])
def test_image_format_default(received):
    result = parse_image_format(received)
    assert isinstance(result, str)
    assert re.fullmatch(r"\w+", result)


def test_invalid_image_format():
    fake_ext = ".pnd"
    with pytest.raises(
        ValueError,
        match=f"^(Received unknown file format '{fake_ext}'. Available formated are)",
    ):
        parse_image_format(fake_ext)


class TestParsePlanetFile:
    def test_from_filename(self):
        input_ = "test"
        assert _parse_planet_file(planet_file=input_) == input_

    def test_from_number(self):
        input_ = 456
        assert _parse_planet_file(planet_number=input_) == f"planet{input_}.dat"

    def test_both_args(self):
        with pytest.raises(TypeError):
            _parse_planet_file(
                planet_file="test",
                planet_number=1,
            )

    def test_no_args(self):
        assert _parse_planet_file() == "planet0.dat"


def mock_find_phip(
    planet_number: Optional[int] = None,  # noqa: ARG001
    *,
    planet_file: Optional[str] = None,  # noqa: ARG001
) -> float:
    return 0.0


class TestParseRotationAngle:
    example_inputs = {
        "rotate_by": 1.0,
        "rotate_with": "planet0.dat",
        "planet_number_argument": ("test", 0),
    }
    default_kwargs = {
        "rotate_by": None,
        "rotate_with": None,
        "planet_number_argument": ("test", None),
        "find_phip": mock_find_phip,
        "stacklevel": 2,
    }

    @pytest.mark.parametrize("kwargs", combinations(example_inputs.items(), 2))
    def test_two_inputs(self, kwargs):
        conf = {**self.default_kwargs, **dict(kwargs)}
        with pytest.raises(TypeError, match="Can only process one argument"):
            _parse_rotation_angle(**conf)

    def test_all_inputs(self):
        conf = {**self.default_kwargs, **self.example_inputs}
        with pytest.raises(TypeError, match="Can only process one argument"):
            _parse_rotation_angle(**conf)

    def test_from_rotate_with(self):
        conf = {
            **self.default_kwargs,
            "rotate_with": self.example_inputs["rotate_with"],
        }
        result = _parse_rotation_angle(**conf)
        assert result == 0.0

    def test_from_planet_number(self):
        conf = {
            **self.default_kwargs,
            "planet_number_argument": self.example_inputs["planet_number_argument"],
        }
        with pytest.deprecated_call():
            result = _parse_rotation_angle(**conf)
        assert result == 0.0
