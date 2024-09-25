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

from lhcbstyle import LHCbStyle
import matplotlib.pyplot as plt
import mplhep as hep  # Import mplhep for HEP style plotting
import numpy as np
import os
from ROOT import RooAbsPdf, RooAbsReal, RooDataSet, TCanvas
from typing import Annotated, List, Union
import zfit


class Plot:

    def __init__(
        self,
        name: str,
        observable: Union[RooAbsReal, zfit.Space],
        data: Union[RooDataSet, zfit.Data],
        pdf: Union[RooAbsPdf, zfit.pdf.BasePDF],
        extension: str = ".pdf",
        backend: str = "roofit",
    ):

        self.name = name
        self.observable = observable
        self.data = data
        self.pdf = pdf
        self.extension = extension
        self.backend = backend

        if self.backend == "roofit":
            with LHCbStyle():
                self.canvas = TCanvas(self.name)
                self.canvas.cd()

                self.frame = self.observable.frame()
                self.data.plotOn(self.frame)
                if hasattr(self.pdf, "coefList") and callable(
                    getattr(self.pdf, "coefList")
                ):
                    colors = ["r", "g", "b", "o"]

                    for pdf_i, color in zip(self.pdf.pdfList(), colors):
                        self.pdf.plotOn(
                            self.frame,
                            Components=[pdf_i],
                            LineStyle="--",
                            LineColor=color,
                        )
                self.pdf.plotOn(self.frame)

                self.frame.Draw()

        elif self.backend == "zfit":
            hep.style.use("LHCb2")
            self.fig, self.ax = plt.subplots()

            _, bin_edges, _ = self.ax.hist(
                self.data.value(self.observable).numpy(),
                bins=100,
                density=False,
                label="Data",
                color="black",
                histtype="step",
            )

            pdf_xvals = np.linspace(bin_edges[0], bin_edges[-1], 1000)

            for component in self.pdf.pdfs:
                component_yield = component.get_yield().numpy()
                component_yvals = (
                    component.pdf(pdf_xvals)
                    * component_yield
                    * (bin_edges[1] - bin_edges[0])
                )
                self.ax.plot(
                    pdf_xvals, component_yvals, label=component.name, marker="none"
                )

            total_yield = self.pdf.get_yield().numpy()
            pdf_yvals = (
                self.pdf.pdf(pdf_xvals) * total_yield * (bin_edges[1] - bin_edges[0])
            )
            self.ax.plot(
                pdf_xvals, pdf_yvals, label=self.pdf.name, marker="none", color="r"
            )

            self.fig.legend()

            self.ax.set_xlim(bin_edges[0], bin_edges[-1])

            self.ax.set_title(self.name)
            self.ax.set_xlabel(self.observable.obs[0])
            self.ax.set_ylabel("Counts per bin")
            hep.lhcb.label(loc=0, ax=self.ax, label="Preliminary", data=True, rlabel="")

    def save(self, plot_path: str):
        path = os.path.join(plot_path, self.name)
        if not os.path.exists(plot_path):
            os.makedirs(plot_path)

        if self.backend == "roofit":
            self.canvas.Print(f"{path}{self.extension}")
        elif self.backend == "zfit":
            self.fig.savefig(f"{path}{self.extension}")
            plt.close(self.fig)


class Sideband:

    def __init__(
        self,
        variable: str,
        variable_range: Annotated[List[float], 2],
        sideband_range: Annotated[List[float], 2],
        signal_range: Annotated[List[float], 2] = None,
    ):

        self.variable = variable
        self.range = variable_range
        self.sideband = sideband_range

        if signal_range:
            self.signal = signal_range
        else:
            self.signal = [
                self.sideband[0] - self.range[0],
                self.range[1] - self.sideband[1],
            ]

    def scale(self, width=None):
        if not (width):
            width = self.signal[1] - self.signal[0]
        return width / (
            (self.sideband[0] - self.range[0]) + (self.range[1] - self.sideband[1])
        )

    def range_cut(self):
        var = self.variable
        return f"({var} > {self.range[0]}) && ({var} < {self.range[1]})"

    def sideband_cut(self):
        var = self.variable
        lower_cut = f"({var} > {self.range[0]}) && ({var} < {self.sideband[0]})"
        upper_cut = f"({var} < {self.range[1]}) && ({var} > {self.sideband[1]})"
        return f"({lower_cut}) || ({upper_cut})"

    def signal_cut(self):
        var = self.variable
        return f"({var} > {self.signal[0]}) && ({var} < {self.signal[1]})"
