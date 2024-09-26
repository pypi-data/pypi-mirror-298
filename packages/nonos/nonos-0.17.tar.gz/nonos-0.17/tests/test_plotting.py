import os

import matplotlib.pyplot as plt
import numpy.testing as npt
import pytest
from matplotlib.colors import SymLogNorm

from nonos.api import GasDataSet, compute, find_nearest, from_data
from nonos.main import main

ARGS_TO_CHECK = {
    "vanilla_conf": ["-geometry", "polar"],
    "diff": ["-geometry", "polar", "-diff"],
    "log": ["-geometry", "polar", "-log"],
    "movie_xy": ["-geometry", "polar", "-all", "-plane", "x", "y"],
    "movie_with_diff": ["-geometry", "polar", "-all", "-diff"],
    "movie_with_multiproc": ["-geometry", "polar", "-all", "-ncpu", "2"],
}


# CLI testing


@pytest.mark.parametrize("argv", ARGS_TO_CHECK.values(), ids=ARGS_TO_CHECK.keys())
def test_plot_simple(argv, simulation_dir, capsys, tmp_path):
    os.chdir(tmp_path)
    ret = main(argv + ["-dir", str(simulation_dir), "-geometry", "polar"])

    out, err = capsys.readouterr()
    assert err == ""
    assert out == ""
    assert ret == 0
    assert len(list(tmp_path.glob("*.png"))) > 0


@pytest.mark.parametrize("format", ["pdf", "png", "jpg"])
def test_common_image_formats(format, simulation_dir, capsys, tmp_path):
    os.chdir(tmp_path)
    ret = main(["-dir", str(simulation_dir), "-fmt", format, "-geometry", "polar"])

    out, err = capsys.readouterr()
    assert err == ""
    assert out == ""
    assert ret == 0
    assert len(list(tmp_path.glob(f"*.{format}"))) > 0


def test_plot_simple_corotation(planet_simulation_dir, capsys, tmp_path):
    os.chdir(tmp_path)
    # just check that the call returns no err
    ret = main(["-cor", "0", "-dir", str(planet_simulation_dir), "-geometry", "polar"])

    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
    assert ret == 0


def test_unknown_geometry(test_data_dir, tmp_path):
    os.chdir(tmp_path)
    with pytest.raises(
        RuntimeError, match=r"Geometry couldn't be determined from data"
    ):
        main(["-dir", str(test_data_dir / "idefix_rwi")])


def test_newvtk_geometry(test_data_dir, capsys, tmp_path):
    os.chdir(tmp_path)
    ret = main(["-cor", "0", "-dir", str(test_data_dir / "idefix_newvtk_planet2d")])
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""
    assert ret == 0


def test_verbose_info(simulation_dir, capsys, tmp_path):
    os.chdir(tmp_path)
    ret = main(["-v", "-dir", str(simulation_dir), "-geometry", "polar"])

    out, err = capsys.readouterr()
    assert err == ""
    assert "Operation took" in out
    assert "INFO" in out
    assert ret == 0


# API testing


def test_plot_planet_corotation(test_data_dir):
    os.chdir(test_data_dir / "idefix_planet3d")

    ds = GasDataSet(43, geometry="polar")
    azimfield = ds["RHO"].radial_at_r().vertical_at_midplane().map("phi").data
    assert find_nearest(azimfield, azimfield.max()) != 0

    azimfieldPlanet = (
        ds["RHO"]
        .radial_at_r()
        .vertical_at_midplane()
        .map("phi", rotate_with="planet0.dat")
        .data
    )
    assert find_nearest(azimfieldPlanet, azimfieldPlanet.max()) == 0


def test_unit_conversion(test_data_dir, temp_figure_and_axis):
    os.chdir(test_data_dir / "idefix_planet3d")

    ds = GasDataSet(43, geometry="polar")
    fig, ax = temp_figure_and_axis

    plotfield10 = (
        ds["RHO"]
        .vertical_at_midplane()
        .map("R", "phi")
        .plot(fig, ax, unit_conversion=10)
    )
    plotfield = ds["RHO"].vertical_at_midplane().map("R", "phi").plot(fig, ax)

    npt.assert_allclose(plotfield10.get_array(), 10 * plotfield.get_array())


def test_vmin_vmax_api(test_data_dir, temp_figure_and_axis):
    ds = GasDataSet(1, directory=test_data_dir / "idefix_rwi", geometry="polar")
    fig, ax = temp_figure_and_axis
    p = ds["VX1"].vertical_at_midplane().map("R", "phi")

    # check that no warning is emitted from matplotlib
    im1 = p.plot(fig, ax, vmin=-1, vmax=1, norm=SymLogNorm(linthresh=0.1, base=10))
    im2 = p.plot(fig, ax, norm=SymLogNorm(linthresh=0.1, base=10, vmin=-1, vmax=1))

    npt.assert_array_equal(im1.get_array(), im2.get_array())


def test_compute_from_data(test_data_dir):
    ne = pytest.importorskip("numexpr")

    directory = test_data_dir / "idefix_planet3d"
    os.chdir(directory)

    ds = GasDataSet(43, geometry="polar")

    rhovpfield = ds["RHO"].vertical_projection()
    vx2vpfield = ds["VX2"].vertical_projection()

    rhovp = rhovpfield.data
    vx2vp = vx2vpfield.data

    with pytest.deprecated_call():
        rhovx2_from_data = from_data(
            field="RHOVX2",
            data=rhovp * vx2vp,
            coords=rhovpfield.coords,
            on=rhovpfield.on,
            operation=rhovpfield.operation,
            directory=directory,
        )

    datane = ne.evaluate("rhovp*vx2vp")
    rhovx2_compute = compute(
        field="RHOVX2",
        data=datane,
        ref=rhovpfield,
    )

    npt.assert_array_equal(rhovx2_from_data.data, rhovx2_compute.data)


def test_pbar(simulation_dir, capsys, tmp_path):
    os.chdir(tmp_path)
    ret = main(["-pbar", "-dir", str(simulation_dir), "-geometry", "polar"])

    out, err = capsys.readouterr()
    assert err == ""
    assert out == ""
    assert ret == 0


def test_corotation_api_float(test_data_dir):
    os.chdir(test_data_dir / "idefix_newvtk_planet2d")

    ds = GasDataSet(23)
    case1 = ds["RHO"].map("x", "y", rotate_with="planet0.dat")
    ds = GasDataSet(23)
    case2 = ds["RHO"].map("x", "y", rotate_by=1.89628895460529)

    npt.assert_array_equal(case1.data, case2.data)


@pytest.mark.parametrize(
    "map_args",
    [("R", "phi"), ("phi", "R")],
)
def test_reg(test_data_dir, map_args):
    ds = GasDataSet(23, directory=test_data_dir / "idefix_newvtk_planet2d")
    fig, ax = plt.subplots()
    ds["RHO"].map(*map_args).plot(fig, ax)
