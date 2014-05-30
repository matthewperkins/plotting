from traits.api import HasTraits, Instance, Int, Float, on_trait_change
from traitsui.api import View, Group, Item
from enable.api import ColorTrait
from enable.component_editor import ComponentEditor
from chaco.api import marker_trait, Plot, ArrayPlotData, VPlotContainer
from numpy import linspace, sin
import pdb
import numpy as np

class HHCurrentTraits(HasTraits):

    gateplot = Instance(VPlotContainer)
    ivplot = Instance(Plot)

    ErevCur1 = Float(-60)
    GmaxCur1 = Float(0.05)
    MvhalfCur1 = Float(-80)
    MKCur1 = Float(10)
    MssminCur1 = Float(0)
    Mdenom_expCur1 = Float(1)
    MpCur1 = Float(1)

    NvhalfCur1 = Float(-80)
    NKCur1 = Float(10)
    NssminCur1 = Float(0)
    Ndenom_expCur1 = Float(1)
    NpCur1 = Float(1)

    HvhalfCur1 = Float(-80)
    HKCur1 = Float(10)
    HssminCur1 = Float(0)
    Hdenom_expCur1 = Float(1)
    HpCur1 = Float(1)

    ErevCur2 = Float(-60)
    GmaxCur2 = Float(0.05)
    MvhalfCur2 = Float(-80)
    MKCur2 = Float(10)
    MssminCur2 = Float(0)
    Mdenom_expCur2 = Float(1)
    MpCur2 = Float(1)

    NvhalfCur2 = Float(-80)
    NKCur2 = Float(10)
    NssminCur2 = Float(0)
    Ndenom_expCur2 = Float(1)
    NpCur2 = Float(1)

    HvhalfCur2 = Float(-80)
    HKCur2 = Float(10)
    HssminCur2 = Float(0)
    Hdenom_expCur2 = Float(1)
    HpCur2 = Float(1)
    
    traits_view = View(
        Group(Group(Item('gateplot', editor=ComponentEditor(), show_label=False),
                    Group(Group(Group(Item('MvhalfCur1'),
                                      Item('MKCur1'),
                                      Item('MssminCur1'),
                                      Item('Mdenom_expCur1'),
                                      Item('MpCur1'),
                                      orientation = "vertical"),
                                Group(Item('NvhalfCur1'),
                                      Item('NKCur1'),
                                      Item('NssminCur1'),
                                      Item('Ndenom_expCur1'),
                                      Item('NpCur1'),
                                      orientation = "vertical"),
                                Group(Item('HvhalfCur1'),
                                      Item('HKCur1'),
                                      Item('HssminCur1'),
                                      Item('Hdenom_expCur1'),
                                      Item('HpCur1'),
                                      orientation = "vertical")),
                          Group(Group(Item('MvhalfCur2'),
                                      Item('MKCur2'),
                                      Item('MssminCur2'),
                                      Item('Mdenom_expCur2'),
                                      Item('MpCur2'),
                                      orientation = "vertical"),
                                Group(Item('NvhalfCur2'),
                                      Item('NKCur2'),
                                      Item('NssminCur2'),
                                      Item('Ndenom_expCur2'),
                                      Item('NpCur2'),
                                      orientation = "vertical"),
                                Group(Item('HvhalfCur2'),
                                      Item('HKCur2'),
                                      Item('HssminCur2'),
                                      Item('Hdenom_expCur2'),
                                      Item('HpCur2'),
                                      orientation = "vertical")))),
              orientation = "horizontal"),
        Group(Item('ivplot', editor=ComponentEditor(), show_label=False),
              Group(Item('ErevCur1'),
                    Item('GmaxCur1'),
                    Item('ErevCur2'),
                    Item('GmaxCur2'),
                    orientation = "vertical"),
              orientation = "horizontal"))

    def __init__(self):

        super(HHCurrentTraits, self).__init__()
        # gates
        self.vm = linspace(-120,65,1000)
        ((MCur1,NCur1,HCur1),(MCur2,NCur2,HCur2)) = self.__gates()
        self.Cur1gatedata = ArrayPlotData(x=self.vm, M=MCur1, N=NCur1, H=HCur1)
        self.Cur2gatedata = ArrayPlotData(x=self.vm, M=MCur2, N=NCur2, H=HCur2)

        Cur1gatesplot = Plot(self.Cur1gatedata)
        Cur1gatesplot.plot(("x", "M"), type = "line", color = "blue")
        Cur1gatesplot.plot(("x", "N"), type = "line", color = "green")
        Cur1gatesplot.plot(("x", "H"), type = "line", color = "red")

        Cur2gatesplot = Plot(self.Cur2gatedata)
        Cur2gatesplot.plot(("x", "M"), type = "line", color = "blue")
        Cur2gatesplot.plot(("x", "N"), type = "line", color = "green")
        Cur2gatesplot.plot(("x", "H"), type = "line", color = "red")

        gateplot = VPlotContainer(Cur1gatesplot, Cur2gatesplot)
        self.gateplot = gateplot

        (Cur1,Cur2) = self.__iv()
        self.ivdata = ArrayPlotData(x=self.vm, nA1=Cur1, nA2=Cur2, combin=Cur1+Cur2)
        ivplot = Plot(self.ivdata)
        ivplot.plot(("x", "nA1"), type = "line", color = "blue")
        ivplot.plot(("x", "nA2"), type = "line", color = "green")
        ivplot.plot(("x", "combin"), type = "line", color = "black")
        self.ivplot = ivplot

    def __gates(self):
        MCur1 = (1-self.MssminCur1)/(1 + np.exp((self.vm - self.MvhalfCur1)/self.MKCur1))**self.Mdenom_expCur1 + self.MssminCur1
        NCur1 = (1-self.NssminCur1)/(1 + np.exp((self.vm - self.NvhalfCur1)/self.NKCur1))**self.Ndenom_expCur1 + self.NssminCur1
        HCur1 = (1-self.HssminCur1)/(1 + np.exp((self.vm - self.HvhalfCur1)/self.HKCur1))**self.Hdenom_expCur1 + self.HssminCur1
        MCur2 = (1-self.MssminCur2)/(1 + np.exp((self.vm - self.MvhalfCur2)/self.MKCur2))**self.Mdenom_expCur2 + self.MssminCur2
        NCur2 = (1-self.NssminCur2)/(1 + np.exp((self.vm - self.NvhalfCur2)/self.NKCur2))**self.Ndenom_expCur2 + self.NssminCur2
        HCur2 = (1-self.HssminCur2)/(1 + np.exp((self.vm - self.HvhalfCur2)/self.HKCur2))**self.Hdenom_expCur2 + self.HssminCur2
        return ((MCur1,NCur1,HCur1),(MCur2, NCur2, HCur2))

    def __iv(self):
        ((MCur1,NCur1,HCur1),(MCur2,NCur2,HCur2)) = self.__gates()
        Cur1 = (MCur1**self.MpCur1 * NCur1**self.NpCur1 * HCur1**self.HpCur1)*self.GmaxCur1*(self.vm - self.ErevCur1)
        Cur2 = (MCur2**self.MpCur2 * NCur2**self.NpCur2 * HCur2**self.HpCur2)*self.GmaxCur2*(self.vm - self.ErevCur2)
        return (Cur1,Cur2)

    @on_trait_change('ErevCur1','GmaxCur1','MvhalfCur1',
                     'MKCur1','MssminCur1','Mdenom_expCur1',
                     'MpCur1','NvhalfCur1','NKCur1',
                     'NssminCur1','Ndenom_expCur1','NpCur1',
                     'HvhalfCur1','HKCur1','HssminCur1',
                     'Hdenom_expCur1','HpCur1',
                     'ErevCur2','GmaxCur2','MvhalfCur2',
                     'MKCur2','MssminCur2','Mdenom_expCur2',
                     'MpCur2','NvhalfCur2','NKCur2',
                     'NssminCur2','Ndenom_expCur2','NpCur2',
                     'HvhalfCur2','HKCur2','HssminCur2',
                     'Hdenom_expCur2','HpCur2')
    def _calc_current(self):
        ((MCur1,NCur1,HCur1),(MCur2,NCur2,HCur2)) = self.__gates()
        (Cur1, Cur2) = self.__iv()
        comb = Cur1 + Cur2
        self.Cur1gatedata.set_data("M", MCur1)
        self.Cur1gatedata.set_data("N", NCur1)
        self.Cur1gatedata.set_data("H", HCur1)
        self.Cur2gatedata.set_data("M", MCur2)
        self.Cur2gatedata.set_data("N", NCur2)
        self.Cur2gatedata.set_data("H", HCur2)
        self.ivdata.set_data("nA1", Cur1)
        self.ivdata.set_data("nA2", Cur2)
        self.ivdata.set_data("combin", comb)

if __name__ == "__main__":
    HHCurrentTraits().configure_traits()
