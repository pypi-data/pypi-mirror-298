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
from .utils import example_file

gROOT.SetBatch(True)


def test_bins_io(example_file):
    import json
    from triggercalib import HltEff

    tree, path = example_file

    h1 = HltEff(
        "test_write_bins",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        expert_mode=True,
        lazy=True,
    )
    h1.set_binning(
        {"varA": {"label": "Variable A", "bins": [3, 0, 3]}},
        compute_bins=True,
        bin_cut="var1 > 5200 && var1 < 5360 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h1.write_bins("results/test_bins_io_binning.json")

    # Read in binning scheme
    with open("results/test_bins_io_binning.json", "r") as binning_file:
        binning = json.load(binning_file)

    h2 = HltEff(
        "test_read_bins",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        binning=binning,
        expert_mode=True,
        lazy=True,
    )

    assert h1.binning_scheme == h2.binning_scheme
