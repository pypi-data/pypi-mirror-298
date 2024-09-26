from typing import Any, Literal, Optional, TypeVar, Union, overload

import numpy as np


def is_set(x: Any) -> bool:
    return x not in (None, "unset")


T1 = TypeVar("T1")
T2 = TypeVar("T2")


def userval_or_default(userval: T1, /, *, default: T2) -> Union[T1, T2]:
    # it'd be nice to avoid a Union as a return type, however it's not clear
    # how to express what this function does in typing language.
    # In practice this is used in places where it's very hard to constrain T1, so
    # the infered return type always degrades down to Any anyway.
    if is_set(userval):
        return userval
    else:
        return default


def parse_output_number_range(
    on: Union[list[int], int, Literal["unset"], None],
    maxval: Optional[int] = None,
) -> list[int]:
    if not is_set(on):
        if maxval is None:
            raise ValueError("Can't parse a range from unset values without a max.")
        return [maxval]

    if isinstance(on, int):
        return [on]

    assert isinstance(on, list) and all(isinstance(o, int) for o in on)

    if len(on) > 3:
        raise ValueError(
            f"Can't parse a range from sequence {on} with more than 3 values."
        )
    if len(on) == 1:
        return on

    if on[1] < on[0]:
        raise ValueError("Can't parse a range with max < min.")

    # make the upper boundary inclusive
    on[1] += 1
    ret = list(range(*on))
    if maxval is not None and (max_requested := ret[-1]) > maxval:
        raise ValueError(
            f"No output beyond {maxval} is available, but {max_requested} was requested."
        )
    return ret


def parse_range(extent, dim: int) -> tuple[Optional[float], ...]:
    if not is_set(extent):
        return (None,) * 2 * dim

    if len(extent) != 2 * dim:
        raise ValueError(
            f"Received sequence `extent` with incorrect size {len(extent)}. Expected exactly {2*dim=} values."
        )
    return tuple(float(i) if i != "x" else None for i in extent)


@overload
def range_converter(
    extent: tuple[Optional[float], Optional[float]],
    abscissa: np.ndarray,
    ordinate: np.ndarray,
) -> tuple[float, float]: ...


@overload
def range_converter(
    extent: tuple[Optional[float], Optional[float], Optional[float], Optional[float]],
    abscissa: np.ndarray,
    ordinate: np.ndarray,
) -> tuple[float, float, float, float]: ...


def range_converter(extent, abscissa, ordinate):
    if len(extent) == 4:
        return (
            _ if (_ := extent[0]) is not None else abscissa.min(),
            _ if (_ := extent[1]) is not None else abscissa.max(),
            _ if (_ := extent[2]) is not None else ordinate.min(),
            _ if (_ := extent[3]) is not None else ordinate.max(),
        )
    elif len(extent) == 2:
        return (
            _ if (_ := extent[0]) is not None else abscissa.min(),
            _ if (_ := extent[1]) is not None else abscissa.max(),
        )
    else:
        raise TypeError(f"Expected extent to be of lenght 2 or 4, got {len(extent)=}")


def parse_image_format(s: Optional[str]) -> str:
    from matplotlib.backend_bases import FigureCanvasBase

    if not is_set(s):
        return FigureCanvasBase.get_default_filetype()

    assert isinstance(s, str)
    _, _, ext = s.rpartition(".")
    if ext not in (
        available := list(FigureCanvasBase.get_supported_filetypes().keys())
    ):
        raise ValueError(
            f"Received unknown file format '{s}'. "
            f"Available formated are {available}."
        )
    return ext
