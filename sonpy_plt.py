import os
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from NeuroTools.spike2.sonpy import son
import pdb
#from son import son
from mpl_toolkits.axes_grid.axislines import Subplot

# change plotting params
plt.rcParams['figure.subplot.hspace'] = 0.01

# use this hack to add custom modules in myown locale
import sys
custom_path = os.path.expanduser('~') +  os.sep + 'Documents' + os.sep + 'weiss_lab' + os.sep + 'Pyprocessing'
sys.path.append(custom_path)
from b63Vclamp import B63Vclamp_spk2_csv_reader as b63
from smatrixedge import smatrixedge as is_m_edge


def hideaxs(axes):
# this weird Subplot imported from the toolkits let you indivdually set the axis lines to be invisible
# now I am hiding all of the axis lines
    axes.axis["right"].set_visible(False)
    axes.axis["top"].set_visible(False)
    axes.axis["bottom"].set_visible(False)
    axes.axis["left"].set_visible(False)
    axes.patch.set_alpha(0) # set the background of the plotting axes to be transparent

class comp_cc:
    def __init__(self,cntrlfname,expfname,chan_nums, chanlims, xlims, pair=False):
        self.cntrlfname = cntrlfname
        self.pair = pair
        self.expfname = expfname
        self.chans = chan_nums
        self.chanlims = chanlims
        self.xlims = xlims
        self.get_data()
        self.cntrlaxes = []
        self.expaxes = []
        self.diff_axes = []
        self.mk_axes()
        self.setlims()

    def get_data(self):
        self.cntrldata = []
        self.expdata = []
        if not(type(self.chans)==type([])):
            self.chans = [self.chans]
        for i in self.chans:
            self.cntrldata.append(son.Channel(i,self.cntrlfname).data())
            self.expdata.append(son.Channel(i,self.expfname).data())
        self.numblocks = self.cntrldata[0].shape[0]

    def mk_axes_order(self):
        '''either splits number of columns in the plotting into top and bottom, or if pair = True, interleaves columns'''
        length = self.plot_cols
        cntrl = np.r_[1:(length/2)+1]
        exp = np.r_[(length/2) + 1 : length + 1]
        if self.pair == True:
            self.cntrlord = 2*(np.r_[1:len(cntrl)+1])-1
            self.expord = 2*(np.r_[1:len(exp)+1])
        else:
            self.cntrlord = cntrl
            self.expord = exp

    def setlims(self,diff=False):
        ''' chan lims must be an array of tuples'''
        for cond in range(2):
            for block in range(self.numblocks):
                for chan in self.chans:
                    chanindx = self.chans.index(chan)
                    self.set_which_subplot(chan,cond,block)
                    self.currentsubplot.set_ylim(self.chanlims[chanindx])

    def setxlims(self,diff=False):
        ''' chan lims must be an array of tuples'''
        for cond in range(2):
            for block in range(self.numblocks):
                for chan in self.chans:
                    chanindx = self.chans.index(chan)
                    self.set_which_subplot(chan,cond,block)
                    self.currentsubplot.set_xlim(self.xlims[chanindx])
                    
    def mk_axes(self, overdraw = False, pair = False):
        if self.cntrlaxes.__len__()!=0:
            return

        self.fig = plt.figure()
        self.plot_rows = len(self.chans)
        self.overdraw = overdraw
        if overdraw == False:
            self.plot_cols = self.numblocks * 2
        else:
            self.plot_cols = self.numblocks
        self.mk_axes_order()
        for chan in range(len(self.chans)):
            self.cntrlaxes.append([])
            self.expaxes.append([])
            for plotnum in range(self.numblocks):
                print('cntrl' + str(self.plot_rows) + str(self.plot_cols) + str(self.cntrlord[plotnum] + (chan*self.plot_cols)))
                print('exp' + str(self.plot_rows) + str(self.plot_cols) + str(self.expord[plotnum] + (chan*self.plot_cols)))
                tmpcntrlaxes = Subplot(self.fig, self.plot_rows, self.plot_cols, self.cntrlord[plotnum] + (chan*self.plot_cols))
                if overdraw == True:
                    tmpexpaxes = tmpcntrlaxes
                else:
                    tmpexpaxes = Subplot(self.fig, self.plot_rows, self.plot_cols, self.expord[plotnum] + (chan*self.plot_cols))
                self.cntrlaxes[chan].append(tmpcntrlaxes)
                self.expaxes[chan].append(tmpexpaxes)
                ### have to add each axis to object figure
                self.fig.add_subplot(tmpcntrlaxes)
                self.fig.add_subplot(tmpexpaxes)

    def set_which_subplot(self, channum, condition, blocknum):
        chanindx = self.chans.index(channum)
        if condition == 0:
            self.pltdata = self.cntrldata[chanindx][blocknum]
            self.currentsubplot = self.cntrlaxes[chanindx][blocknum%(self.plot_cols)] # again with the modulo
        elif condition == 1:
            self.pltdata = self.expdata[chanindx][blocknum]
            self.currentsubplot = self.expaxes[chanindx][blocknum%(self.plot_cols)]
        else:
            print 'condition arguement is not right'

    def plot_all(self, **keywords):
        for cond in range(2):
            for chan in self.chans:
                for block in range(self.numblocks):
                    self.set_which_subplot(chan, cond, block)
                    print(str(chan) + str(cond) + str(block))
                    print(self.currentsubplot.__repr__())
                    if cond == 0:
                        linclr = 'black'
                    else:
                        linclr = 'blue'
                    self.currentsubplot.plot(self.pltdata,color = linclr, **keywords)
                    if is_m_edge(self.plot_cols, self.plot_rows, edge='r',byrow=True):
#####                         round(self.currentsubplot.get_ylim()*0.25,
##### smatrixedge(ncols, nrows, sindx, edge='b', byrow=False):
                    hideaxs(self.currentsubplot)

    def plot_diff(self, **keywords):
        self.mk_diff_axes()
        for chanindx, chan in enumerate(self.chans):
            for block in range(self.numblocks):
                self.set_which_diff_subplot(chanindx, block)
                self.current_diff_subplot.plot(self.diff_plt_data, **keywords)
                hideaxs(self.current_diff_subplot)
        
    def set_diff_lims(self,yrangelist):
        ''' chan lims must be an array of tuples'''
        for block in range(self.numblocks):
            for chan in self.chans:
                chanindx = self.chans.index(chan)
                self.set_which_diff_subplot(chanindx,block)
                self.current_diff_subplot.set_ylim(yrangelist[chanindx])

    def set_diff_xlims(self,xrangelist):
        ''' chan lims must be an array of tuples'''
        for block in range(self.numblocks):
            for chan in self.chans:
                chanindx = self.chans.index(chan)
                self.set_which_diff_subplot(chanindx,block)
                self.current_diff_subplot.set_xlim(xrangelist[chanindx])

    def set_which_diff_subplot(self, chanindx, blocknum):
        self.diff_plt_data = self.expdata[chanindx][blocknum] - self.cntrldata[chanindx][blocknum]
        self.current_diff_subplot = self.diff_axes[chanindx][blocknum%(self.diff_plot_cols)] # again with the modulo

    def mk_diff_axes(self):
        if self.diff_axes.__len__()!=0:
            return
        self.diff_fig = plt.figure()
        self.diff_plot_rows = len(self.chans)
        self.diff_plot_cols = self.numblocks
        for i, chan in enumerate(self.chans):
            self.diff_axes.append([])
            for plotnum in range(self.numblocks):
                tmpdiffaxes = Subplot(self.diff_fig, self.diff_plot_rows, self.diff_plot_cols, plotnum+1 + (i*self.diff_plot_cols))
                self.diff_axes[i].append(tmpdiffaxes)
                ### have to add each axis to object figure
                self.diff_fig.add_subplot(tmpdiffaxes)

    def mk_scale_bars(self,figure)



###read data from spk2.smr
# testclass = comp_cc('2011_01_07_0005.mpd', '2011_01_07_0006.mpd', [7,8] , [(-60,20),(0,2)] )
# testclass.plot_all()
# testclass.setlims()
# testclass.fig.savefig('notworking.svg')

