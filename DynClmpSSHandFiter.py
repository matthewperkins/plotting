from traits.api import HasTraits, Instance, Int, Float, on_trait_change
from traitsui.api import View, Group, Item
from enable.api import ColorTrait
from enable.component_editor import ComponentEditor
from chaco.api import marker_trait, Plot, ArrayPlotData, VPlotContainer
from numpy import linspace, sin
import pdb
import numpy as np

class HHCurrentTraits(HasTraits):

    plots = Instance(VPlotContainer)

    Erev = Float(-60)
    Gmax = Float(0.05)
    Mvhalf = Float(-80)
    MK = Float(10)
    Mssmin = Float(0)
    Mdenom_exp = Float(1)
    Mp = Float(1)

    Nvhalf = Float(-80)
    NK = Float(10)
    Nssmin = Float(0)
    Ndenom_exp = Float(1)
    Np = Float(1)

    Hvhalf = Float(-80)
    HK = Float(10)
    Hssmin = Float(0)
    Hdenom_exp = Float(1)
    Hp = Float(1)
    
    traits_view = View(
        Group(
            Group(Item('plots', editor=ComponentEditor(), show_label=False),
                  Group(Item('Mvhalf'),
                        Item('MK'),
                        Item('Mssmin'),
                        Item('Mdenom_exp'),
                        Item('Mp'),
                        orientation = "vertical"),
                  Group(Item('Nvhalf'),
                        Item('NK'),
                        Item('Nssmin'),
                        Item('Ndenom_exp'),
                        Item('Np'),
                        orientation = "vertical"),
                  Group(Item('Hvhalf'),
                        Item('HK'),
                        Item('Hssmin'),
                        Item('Hdenom_exp'),
                        Item('Hp'),
                        orientation = "vertical"),
                  Group(Item('Erev'),
                        Item('Gmax'),
                        orientation = "vertical"),
                  orientation = "horizontal")
            )
        )

    def __init__(self):

        super(HHCurrentTraits, self).__init__()

        # gates
        self.vm = linspace(-120,65,1000)
        (M, N, H) = self.__gates()
        nA = self.__iv()
        self.gatedata = ArrayPlotData(x=self.vm, M=M, N=N, H=H)
        self.ivdata = ArrayPlotData(x=self.vm, nA=nA)
        
        gateplot = Plot(self.gatedata)
        gateplot.plot(("x", "M"), type = "line", color = "blue")
        gateplot.plot(("x", "N"), type = "line", color = "green")
        gateplot.plot(("x", "H"), type = "line", color = "red")

        ivplot = Plot(self.ivdata)
        ivplot.plot(("x", "nA"), type = "line", color = "black")

        container = VPlotContainer(ivplot, gateplot)
        container.spacing = 0
        gateplot.x_axis.orientation = "top"
        gateplot.padding_bottom = 0
        ivplot.padding_top = 0
        
        self.plots = container

    def __gates(self):
        M = (1-self.Mssmin)/(1 + np.exp((self.vm - self.Mvhalf)/self.MK))**self.Mdenom_exp + self.Mssmin
        N = (1-self.Nssmin)/(1 + np.exp((self.vm - self.Nvhalf)/self.NK))**self.Ndenom_exp + self.Nssmin
        H = (1-self.Hssmin)/(1 + np.exp((self.vm - self.Hvhalf)/self.HK))**self.Hdenom_exp + self.Hssmin
        return (M,N,H)

    def __iv(self):
        (M,N,H) = self.__gates()
        return (M**self.Mp * N**self.Np * H**self.Hp) * self.Gmax * (self.vm - self.Erev)

    @on_trait_change('Erev','Gmax','Mvhalf',
                     'MK','Mssmin','Mdenom_exp',
                     'Mp','Nvhalf','NK',
                     'Nssmin','Ndenom_exp','Np',
                     'Hvhalf','HK','Hssmin',
                     'Hdenom_exp','Hp')
    def _calc_current(self):
        (M, N, H) = self.__gates()
        nA = self.__iv()
        self.gatedata.set_data("M", M)
        self.gatedata.set_data("N", N)
        self.gatedata.set_data("H", H)
        self.ivdata.set_data("nA", nA)

class CompositeCurrent(HasTraits):

    gates = Instance(VPlotContainer)
    iv = Instance(Plot)

    

    

if __name__ == "__main__":
    HHCurrentTraits().configure_traits()
