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

from ROOT import (
    RooMsgService,
    gROOT,
    RDataFrame,
    RooArgSet,
    RooDataSetHelper,
    RooFit,
    std,
)
from .utils import example_file, roofit_model, zfit_model

RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)
gROOT.SetBatch(True)


def test_sweights_simple_roofit(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    _, obs, pdf = roofit_model()

    h = HltEff(
        "test_sweights_simple_roofit",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/sweights_simple_roofit/",
        sweights="signal_yield",
        threads=8,
    )
    h.set_binning(
        {"varA": {"label": "Variable A", "bins": [3, 0, 3]}},
        compute_bins=True,
        bin_cut="var1 > 5200 && var1 < 5360 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h.counts()
    h.efficiencies()
    h.write("results/output_test_sweights_simple_roofit.root")

    hist = h["efficiencies"]["tos_total_efficiency_varA"]
    val = hist.GetPointY(0)

    assert (
        val > 0.8 and val < 0.9
    )  # <- see https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues/43


def test_sweights_simple_zfit(example_file):
    from triggercalib import HltEff

    tree, path = example_file
    obs, pdf = zfit_model()

    h = HltEff(
        "test_sweights_simple_zfit",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/sweights_simple_roofit/",
        sweights="signal_yield",
        threads=8,
    )
    h.set_binning(
        {"varA": {"label": "Variable A", "bins": [3, 0, 3]}},
        compute_bins=True,
        bin_cut="var1 > 5200 && var1 < 5360 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h.counts()
    h.efficiencies()
    h.write("results/output_test_sweights_simple_zfit.root")

    hist = h["efficiencies"]["tos_total_efficiency_varA"]
    val = hist.GetPointY(0)

    assert (
        val > 0.8 and val < 0.9
    )  # <- see https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues/43


def test_sweights_with_prefit(example_file):
    from triggercalib import HltEff

    tree, path = example_file

    ws, obs, pdf = roofit_model()

    # Perform prefit #
    rdf = RDataFrame(*example_file)
    rdf = rdf.Filter("isSignal")
    data = rdf.Book(
        std.move(
            RooDataSetHelper(
                "data",
                "data",
                RooArgSet(
                    obs,
                ),
            )
        ),
        (obs.GetName(),),
    )

    pdf.pdfList()[0].fitTo(data.GetValue())

    ws.var("signal_mean").setConstant(True)
    ws.var("signal_width").setConstant(True)

    # Calculate counts and efficiencies #
    h = HltEff(
        "test_sweights_with_prefit",
        tag="Hlt1DummyOne",
        probe="Hlt1DummyOne",
        particle="P",
        path=f"{path}:{tree}",
        lazy=True,
        observable=obs,
        pdf=pdf,
        output_path="results/sweights_with_prefit/",
        sweights="signal_yield",
        threads=8,
    )
    h.set_binning(
        {"varA": {"label": "Variable A", "bins": [3, 0, 3]}},
        compute_bins=True,
        bin_cut="var1 > 5200 && var1 < 5360 && P_Hlt1DummyOneDecision_TIS && P_Hlt1DummyOneDecision_TOS",
    )
    h.counts()
    h.efficiencies()
    h.write("results/output_test_sweights_with_prefit.root")

    hist = h["efficiencies"]["tos_total_efficiency_varA"]
    val = hist.GetPointY(0)

    assert (
        val > 0.8 and val < 0.9
    )  # <- see https://gitlab.cern.ch/lhcb-rta/triggercalib/-/issues/43
