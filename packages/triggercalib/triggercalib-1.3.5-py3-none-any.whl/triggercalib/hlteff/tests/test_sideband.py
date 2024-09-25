###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

from ROOT import gROOT
from .utils import example_file, test_threshold

gROOT.SetBatch(True)


def test_sideband_1D(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    sideband = {
        "var1": {
            "range": [5100, 5460],
            "sideband": [5190, 5370],
            "signal": [5200, 5360],
        }
    }

    h = HltEff(
        "test_sideband",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        sideband=sideband,
    )
    h.set_binning(
        {"varA": {"label": "Variable A", "bins": [3, 0, 3]}},
        compute_bins=True,
        bin_cut="var1 > 5200 && var1 < 5360 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h.counts()
    h.efficiencies()
    h.write("results/output_test_sideband_1D.root")

    hist = h["efficiencies"]["tos_total_efficiency_varA"]
    val = hist.GetPointY(0)

    assert (
        val > 0.8 and val < 0.9
    )  # <- see https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues/43


def test_sideband_2D(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    sideband = {
        "var1": {
            "range": [5100, 5460],
            "sideband": [5190, 5370],
            "signal": [5200, 5360],
        },
    }

    h = HltEff(
        "test_sideband",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        sideband=sideband,
    )
    h.set_binning(
        {
            "varA": {"label": "Variable A", "bins": [3, 0, 3]},
            "varB": {"label": "Variable B", "bins": [3, 2, 8]},
        },
        compute_bins=True,
        bin_cut="var1 > 5200 && var1 < 5360 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h.counts()
    h.efficiencies()
    h.write("results/output_test_sideband_2D.root")

    hist = h["efficiencies"]["tos_total_efficiency_varA_varB"]
    val = hist.GetZ()[0]

    assert (
        val > 0.8 and val < 0.9
    )  # <- see https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues/43
