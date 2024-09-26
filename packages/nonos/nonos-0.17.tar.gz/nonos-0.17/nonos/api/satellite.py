import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import numpy as np
from lick.lick import lick_box

from nonos.api.analysis import Coordinates, GasField, Plotable
from nonos.loaders import Recipe, loader_from, recipe_from

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from nonos._types import FloatArray, PathT


def file_analysis(
    filename: "PathT",
    *,
    inifile: Optional[str] = None,
    code: Optional[str] = None,
    directory: Optional["PathT"] = None,
    norb: Optional[int] = None,
) -> "FloatArray":
    from scipy.ndimage import uniform_filter1d

    if directory is None:
        directory = Path.cwd()
    else:
        directory = Path(directory)

    columns = np.loadtxt(directory / filename, dtype="float64").T
    if norb is None:
        return columns

    loader = loader_from(
        code=code,
        parameter_file=inifile,
        directory=directory,
    )
    recipe = recipe_from(code=code, parameter_file=inifile, directory=directory)
    ini = loader.load_ini_file().meta

    if recipe is Recipe.IDEFIX_VTK and "analysis" in ini["Output"]:
        analysis = ini["Output"]["analysis"]
        rpini = ini["Planet"]["dpl"]
        Ntmean = round(norb * 2 * np.pi * pow(rpini, 1.5) / analysis)
        for i in range(1, len(columns) - 1):
            columns[i] = uniform_filter1d(columns[i], Ntmean)
    else:
        raise NotImplementedError(
            f"moving average on {norb} orbits is not implemented for the recipe {recipe}"
        )
    return columns


def planet_analysis(
    planet_number, *, inifile="", code="", directory="", norb=None
):  # pragma: no cover
    from nonos.api.from_simulation import Parameters

    warnings.warn(
        "nonos.api.satellite.planet_analysis is deprecated and will be removed in "
        "a future version. Please use nonos.api.satellite.file_analysis instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )
    if norb is not None:
        warnings.warn(
            "The norb argument has no effect and is deprecated",
            stacklevel=2,
        )
    init = Parameters(inifile=inifile, code=code, directory=directory)
    init.loadIniFile()
    init.loadPlanetFile(planet_number=planet_number)
    return init


class NonosLick:
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        lx: GasField,
        ly: GasField,
        field: GasField,
        *,
        xmin: Optional[float] = None,
        xmax: Optional[float] = None,
        ymin: Optional[float] = None,
        ymax: Optional[float] = None,
        size_interpolated: int = 1000,
        niter_lic: int = 6,
        kernel_length: int = 101,
        method: str = "linear",
        method_background: str = "nearest",
        light_source: bool = True,
    ):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

        # (x,y) are 2D meshgrids at cell centers
        self.X, self.Y, self.LINE1, self.LINE2, self.F, self.lick = lick_box(
            x,
            y,
            lx.data,
            ly.data,
            field.data,
            xmin=self.xmin,
            xmax=self.xmax,
            ymin=self.ymin,
            ymax=self.ymax,
            size_interpolated=size_interpolated,
            niter_lic=niter_lic,
            kernel_length=kernel_length,
            method=method,
            method_background=method_background,
            light_source=light_source,
        )

    def plot(
        self,
        fig: "Figure",
        ax: "Axes",
        *,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        alpha: float = 0.45,
        log: bool = False,
        cmap=None,
        title: Optional[str] = None,
        density_streamlines: Optional[float] = None,
        color_streamlines: str = "black",
    ):
        dict_background = {}
        dict_background["field"] = "background"
        dict_background["abscissa"] = "x"
        dict_background["ordinate"] = "y"
        dict_background[dict_background["field"]] = self.F
        dict_background[dict_background["abscissa"]] = self.X
        dict_background[dict_background["ordinate"]] = self.Y

        dict_lick = {}
        dict_lick["field"] = "lick"
        dict_lick["abscissa"] = "x"
        dict_lick["ordinate"] = "y"
        dict_lick[dict_lick["field"]] = self.lick
        dict_lick[dict_lick["abscissa"]] = self.X
        dict_lick[dict_lick["ordinate"]] = self.Y

        im = Plotable(dict_background).plot(
            fig,
            ax,
            vmin=vmin,
            vmax=vmax,
            log=log,
            cmap=cmap,
            filename=None,
            dpi=500,
            title=title,
            shading="nearest",
            rasterized=True,
        )
        Plotable(dict_lick).plot(
            fig,
            ax,
            log=False,
            cmap="binary_r",
            filename=None,
            dpi=500,
            title=None,
            alpha=alpha,
            shading="nearest",
            rasterized=True,
        )
        if density_streamlines is not None:
            ax.streamplot(
                self.X,
                self.Y,
                self.LINE1,
                self.LINE2,
                density=density_streamlines,
                arrowstyle="->",
                linewidth=0.5,
                color=color_streamlines,
                # color=np.log10(self.F*np.sqrt(self.LINE1**2+self.LINE2**2)),#/np.max(np.log10(self.F*np.sqrt(self.LINE1**2+self.LINE2**2))),
                # cmap=cb.cbmap("binary_r"),
            )
        ax.set_xlim(self.xmin, self.xmax)
        ax.set_ylim(self.ymin, self.ymax)
        return im


def compute(
    field: str,
    data: np.ndarray,
    ref: GasField,
):
    ret_data = data
    ret_coords = ref.coords
    geometry = ret_coords.geometry
    return GasField(
        field,
        ret_data,
        ret_coords,
        geometry,
        ref.on,
        operation=ref.operation,
        inifile=ref.inifile,
        directory=ref.directory,
        rotate_by=ref._rotate_by,
    )


def from_data(
    *,
    field: str,
    data: np.ndarray,
    coords: Coordinates,
    on: int,
    operation: str,
    inifile: Optional[str] = None,
    code: Optional[str] = None,
    directory: str = "",
    rotate_grid: int = -1,
):  # pragma: no cover
    warnings.warn(
        "nonos.api.satellite.from_data is deprecated and will be removed "
        "in a future version. Please use nonos.api.satellite.compute instead",
        category=DeprecationWarning,
        stacklevel=2,
    )
    ret_data = data
    ret_coords = coords
    geometry = coords.geometry
    return GasField(
        field,
        ret_data,
        ret_coords,
        geometry,
        on,
        operation=operation,
        inifile=inifile,
        code=code,
        directory=directory,
        rotate_grid=rotate_grid,
    )


def from_file(
    *,
    field: str,
    operation: str,
    on: int,
    directory: Optional["PathT"] = None,
):
    if directory is None:
        directory = Path.cwd()
    else:
        directory = Path(directory)
    repout = field.lower()
    headername = directory / "header" / f"header_{operation}.npy"
    with open(headername, "rb") as file:
        dict_coords = np.load(file, allow_pickle=True).item()

    geometry, coord0, coord1, coord2 = dict_coords.values()
    ret_coords = Coordinates(geometry, coord0, coord1, coord2)

    fileout = directory / repout / f"_{operation}_{field}.{on:04d}.npy"
    with open(fileout, "rb") as file:
        ret_data = np.load(file, allow_pickle=True)

    return GasField(
        field,
        ret_data,
        ret_coords,
        geometry,
        on,
        operation=operation,
        directory=directory,
    )
