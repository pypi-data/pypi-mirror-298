import os

import numpy as np
import numpy.testing as npt
import pytest

from nonos.api import GasDataSet, file_analysis


class TestFileAnalysis:
    @pytest.mark.parametrize(
        "directory",
        ["idefix_planet3d", "fargo_adsg_planet"],
    )
    def test_simple(self, test_data_dir, directory):
        result = file_analysis(
            "planet0.dat",
            directory=test_data_dir / directory,
        )
        assert isinstance(result, np.ndarray)

    def test_norb(self, test_data_dir):
        result = file_analysis(
            "planet0.dat",
            directory=test_data_dir / "idefix_planet3d",
            norb=10,
        )
        assert isinstance(result, np.ndarray)

    def test_norb_not_idefix(self, test_data_dir):
        with pytest.raises(NotImplementedError):
            file_analysis(
                "planet0.dat",
                directory=test_data_dir / "fargo_adsg_planet",
                norb=10,
            )

    def test_implicit_directory(self, test_data_dir):
        os.chdir(test_data_dir / "idefix_planet3d")
        result = file_analysis("planet0.dat")
        assert isinstance(result, np.ndarray)


class TestGasDataSetFromNpy:
    expected_keys = ["RHO"]
    args = (7283,)
    kwargs = {"operation": "azimuthal_average"}
    directory = "pluto_spherical"

    def test_from_npy_implicit_directory(self, test_data_dir):
        os.chdir(test_data_dir / self.directory)
        ds = GasDataSet(*self.args, **self.kwargs)
        assert sorted(ds.keys()) == self.expected_keys

    def test_from_npy_explicit_directory(self, test_data_dir):
        ds = GasDataSet(
            *self.args,
            **self.kwargs,
            directory=test_data_dir / self.directory,
        )
        assert sorted(ds.keys()) == self.expected_keys

    def test_deprecation(self, test_data_dir):
        with pytest.deprecated_call():
            ds = GasDataSet.from_npy(
                *self.args,
                **self.kwargs,
                directory=test_data_dir / self.directory,
            )
        assert sorted(ds.keys()) == self.expected_keys


def test_find_rhill(test_data_dir):
    ds = GasDataSet(23, directory=test_data_dir / "idefix_newvtk_planet2d")
    rp = ds["RHO"].find_rp()
    rhill = ds["RHO"].find_rhill()
    assert rhill < rp


def test_field_map_no_mutation(test_data_dir):
    ds = GasDataSet(500, directory=test_data_dir / "idefix_spherical_planet3d")
    f = ds["RHO"].radial_at_r(1.0).vertical_at_midplane()
    d0 = f.data.copy()
    f.map("phi", rotate_by=1.0)
    d1 = f.data.copy()
    npt.assert_array_equal(d1, d0)
