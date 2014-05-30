from traits.api import HasTraits, Instance, Int, Float, Array, on_trait_change, Button
from traitsui.api import View, Group, Item
from enable.api import ColorTrait
from enable.component_editor import ComponentEditor
from chaco.api import marker_trait, Plot, ArrayPlotData, VPlotContainer
from numpy import linspace, sin
import pdb
import numpy as np
import sys

class HHCurrentTraits(HasTraits):

    plots = Instance(VPlotContainer)
    # write_button = Instance(Button)
    write_button = Button()

    ErevCur1 = Float(20)
    GmaxCur1 = Float(0.05)
    MvhalfCur1 = Float(50)
    MKCur1 = Float(-80)
    MssminCur1 = Float(0)
    Mdenom_expCur1 = Float(1)
    MpCur1 = Float(1)

    NvhalfCur1 = Float(25)
    NKCur1 = Float(10)
    NssminCur1 = Float(0)
    Ndenom_expCur1 = Float(1)
    NpCur1 = Float(1)

    HvhalfCur1 = Float(-80)
    HKCur1 = Float(10)
    HssminCur1 = Float(0)
    Hdenom_expCur1 = Float(1)
    HpCur1 = Float(0)

    ErevCur2 = Float(20)
    GmaxCur2 = Float(0.08)
    MvhalfCur2 = Float(-45)
    MKCur2 = Float(-5)
    MssminCur2 = Float(0)
    Mdenom_expCur2 = Float(1)
    MpCur2 = Float(1)

    NvhalfCur2 = Float(25)
    NKCur2 = Float(10)
    NssminCur2 = Float(0)
    Ndenom_expCur2 = Float(1)
    NpCur2 = Float(1)

    HvhalfCur2 = Float(-80)
    HKCur2 = Float(10)
    HssminCur2 = Float(0)
    Hdenom_expCur2 = Float(1)
    HpCur2 = Float(0)

    traits_view = View(
        Group(
            Item('plots', editor=ComponentEditor(), show_label=False),
            Group(
                Group(
                    Group(
                        Item('MvhalfCur1'),
                        Item('MKCur1'),
                        Item('MssminCur1'),
                        Item('Mdenom_expCur1'),
                        Item('MpCur1'),
                        orientation = "vertical"),
                    Group(
                        Item('NvhalfCur1'),
                        Item('NKCur1'),
                        Item('NssminCur1'),
                        Item('Ndenom_expCur1'),
                        Item('NpCur1'),
                        orientation = "vertical"),
                    Group(
                        Item('HvhalfCur1'),
                        Item('HKCur1'),
                        Item('HssminCur1'),
                        Item('Hdenom_expCur1'),
                        Item('HpCur1'),
                        orientation = "vertical"),
                    Group(
                        Item('GmaxCur1'),
                        Item('ErevCur1'),
                        orientation = "vertical")),
                Group(
                    Group(
                        Item('MvhalfCur2'),
                        Item('MKCur2'),
                        Item('MssminCur2'),
                        Item('Mdenom_expCur2'),
                        Item('MpCur2'),
                        orientation = "vertical"),
                    Group(
                        Item('NvhalfCur2'),
                        Item('NKCur2'),
                        Item('NssminCur2'),
                        Item('Ndenom_expCur2'),
                        Item('NpCur2'),
                        orientation = "vertical"),
                    Group(
                        Item('HvhalfCur2'),
                        Item('HKCur2'),
                        Item('HssminCur2'),
                        Item('Hdenom_expCur2'),
                        Item('HpCur2'),
                        orientation = "vertical"),
                    Group(
                        Item('GmaxCur2'),
                        Item('ErevCur2'),
                        orientation = "vertical")),
                Item('write_button'),
                orientation = "horizontal"),
            orientation = "horizontal"))
    
    def __init__(self, ExprmntVm=None, ExprmntnA=None):

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

        (Cur1,Cur2) = self.__iv()
        self.ivdata = ArrayPlotData(x=self.vm, nA1=Cur1, nA2=Cur2, combin=Cur1+Cur2)
        ivplot = Plot(self.ivdata)
        ivplot.plot(("x", "nA1"), type = "line", color = "blue")
        ivplot.plot(("x", "nA2"), type = "line", color = "green")
        ivplot.plot(("x", "combin"), type = "line", color = "black")
        
        if ExprmntVm is not None:
            self.ivdata.set_data('ExptVm',ExprmntVm)
            self.ivdata.set_data('ExptnA',ExprmntnA)
            ivplot.plot(("ExptVm", "ExptnA"),
                        type = "scatter", color = "red", marker_size = 5)


        self.plots = VPlotContainer(ivplot, Cur2gatesplot, Cur1gatesplot)
        self.plots.spacing = 0
        ivplot.padding_top = 0
        Cur1gatesplot.padding_bottom = 0
        Cur2gatesplot.padding_top = 0

        self.write_button = Button(label="Print_Pars")

    def __gates(self):
        MCur1 = (1-self.MssminCur1)/(1 + np.exp((self.vm - self.MvhalfCur1)/self.MKCur1))**self.Mdenom_expCur1 + self.MssminCur1
        NCur1 = (1-self.NssminCur1)/(1 + np.exp((self.vm - self.NvhalfCur1)/self.NKCur1))**self.Ndenom_expCur1 + self.NssminCur1
        HCur1 = (1-self.HssminCur1)/(1 + np.exp((self.vm - self.HvhalfCur1)/self.HKCur1))**self.Hdenom_expCur1 + self.HssminCur1
        MCur2 = (1-self.MssminCur2)/(1 + np.exp((self.vm - self.MvhalfCur2)/self.MKCur2))**self.Mdenom_expCur2 + self.MssminCur2
        NCur2 = (1-self.NssminCur2)/(1 + np.exp((self.vm - self.NvhalfCur2)/self.NKCur2))**self.Ndenom_expCur2 + self.NssminCur2
        HCur2 = (1-self.HssminCur2)/(1 + np.exp((self.vm - self.HvhalfCur2)/self.HKCur2))**self.Hdenom_expCur2 + self.HssminCur2
        if self.MpCur1==0:
            MCur1 = np.repeat(0,len(self.vm))
        if self.NpCur1==0:
            NCur1 = np.repeat(0,len(self.vm))
        if self.HpCur1==0:
            HCur1 = np.repeat(0,len(self.vm))
        if self.MpCur2==0:
            MCur2 = np.repeat(0,len(self.vm))
        if self.NpCur2==0:
            NCur2 = np.repeat(0,len(self.vm))
        if self.HpCur2==0:
            HCur2 = np.repeat(0,len(self.vm))
        return ((MCur1,NCur1,HCur1),(MCur2, NCur2, HCur2))

    def __iv(self):
        ((MCur1,NCur1,HCur1),(MCur2,NCur2,HCur2)) = self.__gates()
        Cur1 = (MCur1**self.MpCur1 * NCur1**self.NpCur1 * HCur1**self.HpCur1)*self.GmaxCur1*(self.vm - self.ErevCur1)
        Cur2 = (MCur2**self.MpCur2 * NCur2**self.NpCur2 * HCur2**self.HpCur2)*self.GmaxCur2*(self.vm - self.ErevCur2)
        return (Cur1,Cur2)

    # '+' matches all traits on the object
    @on_trait_change('+')
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

    def _write_button_fired(self):
        with open('pars.txt', 'wt') as sys.stdout: self.print_traits()

def main(atf_path):
    ''' pass in the full path of an ATF file with the difference current IV'''
    from atf_reader import ATFreader
    atf = ATFreader(atf_path)
    mV = atf.read_data()[:,0]
    nA = atf.read_data()[:,1]
    HHCurrentTraits(ExprmntVm = mV, ExprmntnA = nA).configure_traits()

if __name__ == "__main__":
    ''' pass in the full path of an ATF file with the difference current IV'''
    import sys
    if len(sys.argv)<2:
        print("need name of axon text file")
        raise ValueError
    main(sys.argv[1])



