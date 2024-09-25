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


def test_raw(example_file):
    from triggercalib import HltEff

    tree, path = example_file

    h = HltEff(
        "test_raw",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        expert_mode=True,
    )
    h.set_binning(
        {"varA": {"label": "Variable A", "bins": [3, 0, 3]}},
        compute_bins=True,
        bin_cut="var1 > 5200 && var1 < 5360 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h.counts()
    h.efficiencies()
    h.write("results/test_raw/output_test_raw.root")
