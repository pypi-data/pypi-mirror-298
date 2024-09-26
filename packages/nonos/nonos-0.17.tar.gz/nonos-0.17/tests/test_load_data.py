import os
import shutil

import numpy as np
import pytest

from nonos.api import GasDataSet


def test_from_npy_error(test_data_dir):
    with pytest.raises(FileNotFoundError):
        GasDataSet(
            500,
            operation="typo",
            directory=test_data_dir / "idefix_spherical_planet3d",
        )


def test_roundtrip_simple(test_data_dir, tmp_path):
    ds = GasDataSet(500, directory=test_data_dir / "idefix_spherical_planet3d")
    assert ds.nfields == 7

    gf = ds["RHO"].azimuthal_average()

    gf.save(tmp_path)
    dsnpy = GasDataSet(
        500,
        operation="azimuthal_average",
        directory=tmp_path,
    )
    assert dsnpy.nfields == 1


@pytest.mark.parametrize(
    "implicit_directory",
    [
        pytest.param(True, id="implicit directory"),
        pytest.param(False, id="explicit directory"),
    ],
)
def test_simple_fargo_adsg(test_data_dir, implicit_directory):
    data_dir = test_data_dir / "fargo_adsg_planet"
    if implicit_directory:
        os.chdir(data_dir)
        directory = None
    else:
        directory = data_dir.absolute()

    ds = GasDataSet(
        200,
        code="fargo_adsg",
        inifile="planetpendragon_200k.par",
        directory=directory,
    )
    assert ds.nfields == 1


def test_roundtrip_no_operation_all_field(test_data_dir, tmp_path):
    os.chdir(test_data_dir / "idefix_spherical_planet3d")

    ds = GasDataSet(500)
    assert ds.nfields == 7

    gf = ds["RHO"]

    gf.save(tmp_path)
    dsnpy = GasDataSet(
        500,
        operation="",
        directory=tmp_path,
    )
    assert dsnpy.nfields == 1
    np.testing.assert_array_equal(ds["RHO"].data, dsnpy["RHO"].data)


def test_roundtrip_other_dir(test_data_dir, tmp_path):
    os.chdir(test_data_dir / "idefix_spherical_planet3d")
    gf = GasDataSet(500)["RHO"].azimuthal_average()
    gf.save(tmp_path)
    dsnpy = GasDataSet(
        500,
        operation="azimuthal_average",
        directory=tmp_path,
    )
    assert dsnpy.nfields == 1


@pytest.mark.parametrize("header_only", [True, False])
def test_save_to_new_dir(header_only, test_data_dir, tmp_path):
    gf = GasDataSet(500, directory=test_data_dir / "idefix_spherical_planet3d")["RHO"]

    savedir = tmp_path / "savedir"

    # exercise saving to a directory that doesn't exist yet
    saved_file = gf.save(savedir, header_only=header_only)
    assert savedir.exists
    assert savedir == saved_file.parents[1]
    if header_only:
        assert not saved_file.exists()
    else:
        assert saved_file.is_file()

        # exercise saving again
        write_time = saved_file.stat().st_mtime
        saved_file_2 = gf.save(savedir, header_only=header_only)
        assert saved_file_2 == saved_file
        assert saved_file_2.stat().st_mtime == write_time, "File was overwritten"


def test_npy_radial_at_r(test_data_dir, tmp_path):
    os.chdir(test_data_dir / "idefix_spherical_planet3d")
    gf = GasDataSet(500)["RHO"].radial_at_r(1.1)
    gf.save(tmp_path)
    dsnpy = GasDataSet(
        500,
        operation="radial_at_r1.1",
        directory=tmp_path,
    )
    assert list(dsnpy.keys()) == ["RHO"]


def test_latitudinal_projection(test_data_dir):
    os.chdir(test_data_dir / "idefix_spherical_planet3d")
    theta = np.arctan(5 * 0.1)
    gflpt = GasDataSet(500)["RHO"].latitudinal_projection(theta)
    gflp = GasDataSet(500)["RHO"].latitudinal_projection()
    np.testing.assert_equal(gflpt.data, gflp.data)


def test_radial_average_interval_vmin_vmax(test_data_dir):
    os.chdir(test_data_dir / "idefix_spherical_planet3d")
    with pytest.raises(
        ValueError,
        match=r"The radial interval vmin=1 and vmax=None should be defined",
    ):
        GasDataSet(500)["RHO"].radial_average_interval(1)


def test_default_operation_name(test_data_dir):
    os.chdir(test_data_dir / "idefix_spherical_planet3d")
    gf = GasDataSet(500)["RHO"].radial_average_interval(1, 2)
    assert gf.operation == "radial_average_interval_1_2"


def test_custom_operation_name(test_data_dir):
    os.chdir(test_data_dir / "idefix_spherical_planet3d")
    gfno = GasDataSet(500)["RHO"].radial_average_interval(
        1, 2, operation_name="radial_custom"
    )
    assert gfno.operation == "radial_custom"


def test_save_current_dir(test_data_dir, tmp_path):
    src_dir = test_data_dir / "idefix_spherical_planet3d"
    shutil.copy(src_dir / "idefix.ini", tmp_path)
    shutil.copy(src_dir / "data.0500.vtk", tmp_path)

    inifile = tmp_path / "idefix.ini"
    time_inifile = inifile.stat().st_mtime
    gf = GasDataSet(500, directory=tmp_path)["RHO"]
    gf.save(tmp_path)
    assert inifile.stat().st_mtime == time_inifile


@pytest.mark.parametrize(
    "from_abs_path",
    [
        pytest.param(True, id="from absolute path"),
        pytest.param(False, id="from relative path"),
    ],
)
def test_api_vtk_by_name(test_data_dir, from_abs_path):
    data_dir = test_data_dir / "idefix_spherical_planet3d"
    if from_abs_path:
        input_ = str((data_dir / "data.0500.vtk").absolute())
    else:
        os.chdir(data_dir)
        input_ = "data.0500.vtk"

    ds = GasDataSet(input_)
    assert ds.on == 500

    with pytest.raises(FileNotFoundError):
        GasDataSet(input_.replace("data.0500", "datawrong.0500"))


def test_api_vtk_by_name_fargo(test_data_dir):
    GasDataSet(test_data_dir / "fargo3d_planet2d" / "gasdens40.dat")


def test_api_fluid_fargo3d(test_data_dir):
    args = (5,)
    kwargs = {
        "fluid": "dust2",
        "directory": test_data_dir / "fargo3d_multifluid",
    }
    ds = GasDataSet(*args, **kwargs)
    assert ds.nfields == 1

    kwargs["fluid"] = "dust999"
    with pytest.raises(
        FileNotFoundError,
        match=r"No file matches the pattern 'dust999\*5\.dat'",
    ):
        GasDataSet(*args, **kwargs)


def test_api_fluid_idefix(test_data_dir):
    with pytest.warns(
        UserWarning,
        match="Unused keyword argument: 'fluid'",
    ):
        GasDataSet(
            500,
            fluid="dust1",
            directory=test_data_dir / "idefix_spherical_planet3d",
        )


# fmt: off
@pytest.mark.parametrize(
    "geometry, slice_no, operation_name, operation_args, axis",
    [
        pytest.param("spherical_3d", 1, "azimuthal_at_phi", (np.pi,), "r"),
        pytest.param("spherical_3d", 1, "azimuthal_at_phi", (np.pi,), "theta"),
        pytest.param("spherical_3d", 1, "azimuthal_at_phi", (np.pi,), "phi", marks=pytest.mark.xfail(strict=True, reason="known bug in azimuthal_at_phi")),
        pytest.param("spherical_3d", 2, "vertical_at_midplane", (), "r"),
        pytest.param("spherical_3d", 2, "vertical_at_midplane", (), "theta", marks=pytest.mark.xfail(strict=True, reason="known bug in vertical_at_midplane")),
        pytest.param("spherical_3d", 2, "vertical_at_midplane", (), "phi"),
        pytest.param("spherical_3d", 3, "radial_at_r", (1.0,), "r", marks=pytest.mark.xfail(strict=True, reason="known bug in radial_at_r")),
        pytest.param("spherical_3d", 3, "radial_at_r", (1.0,), "theta"),
        pytest.param("spherical_3d", 3, "radial_at_r", (1.0,), "phi"),
        pytest.param("spherical_3d", 4, "azimuthal_average", (), "r"),
        pytest.param("spherical_3d", 4, "azimuthal_average", (), "theta"),
        pytest.param("spherical_3d", 4, "azimuthal_average", (), "phi", marks=pytest.mark.xfail(strict=True, reason="known bug in azimuthal_average")),

        pytest.param("polar_3d", 1, "azimuthal_at_phi", (np.pi,), "R"),
        pytest.param("polar_3d", 1, "azimuthal_at_phi", (np.pi,), "phi", marks=pytest.mark.xfail(strict=True, reason="known bug in azimuthal_at_phi")),
        pytest.param("polar_3d", 1, "azimuthal_at_phi", (np.pi,), "z"),
        pytest.param("polar_3d", 2, "vertical_at_midplane", (), "R"),
        pytest.param("polar_3d", 2, "vertical_at_midplane", (), "phi"),
        pytest.param("polar_3d", 2, "vertical_at_midplane", (), "z", marks=pytest.mark.xfail(strict=True, reason="known bug in vertical_at_midplane")),
        pytest.param("polar_3d", 3, "radial_at_r", (2.0078125,), "R", marks=pytest.mark.xfail(strict=True, reason="known bug in radial_at_r")),
        pytest.param("polar_3d", 3, "radial_at_r", (2.0078125,), "phi"),
        pytest.param("polar_3d", 3, "radial_at_r", (2.0078125,), "z"),
        pytest.param("polar_3d", 4, "azimuthal_average", (), "R"),
        pytest.param("polar_3d", 4, "azimuthal_average", (), "phi", marks=pytest.mark.xfail(strict=True, reason="known bug in azimuthal_average")),
        pytest.param("polar_3d", 4, "azimuthal_average", (), "z"),
    ],
)
# fmt: on
def test_api_vtk_slices_idefix(test_data_dir, geometry, slice_no, operation_name, operation_args, axis):
    on = 9
    ds = GasDataSet(test_data_dir / "idefix_vtk_slices" / geometry / f"data.{on:04d}.vtk")
    ds_phi_cut = GasDataSet(
        test_data_dir / "idefix_vtk_slices" / geometry / f"slice{slice_no}.{on:04d}.vtk"
    )
    method = getattr(ds["RHO"], operation_name)
    rho_slice_pp = method(*operation_args)
    rho_slice_cut = ds_phi_cut["RHO"]
    np.testing.assert_array_almost_equal(rho_slice_pp.data, rho_slice_cut.data)

    np.testing.assert_array_almost_equal(
        getattr(rho_slice_pp.coords, axis),
        getattr(rho_slice_cut.coords, axis),
    )
