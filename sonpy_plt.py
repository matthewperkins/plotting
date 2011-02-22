import os
import re
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rcParams['figure.subplot.hspace'] = 0.001
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

def dothescalebars(axes, xrngfrac, yrngfrac, xposfrac, yposfrac, xpadfrac, ypadfrac):
    yscalebar = mkscalebar_length(yrngfrac, axes.get_ylim())
    xscalebar = mkscalebar_length(xrngfrac, axes.get_xlim())
    xpos,ypos = mkscale_pos(axes,xposfrac,yposfrac)
    xpad,ypad = mkscale_plot_pad(axes, xpadfrac, ypadfrac)
    
    axes.plot([xpos - xscalebar, xpos], [ypos,ypos], color = '#140060')
    axes.plot([xpos, xpos], [ypos + ypad, ypos + yscalebar + ypad], color = '#140060')
    axes.text(xpos + xpad, ypos + ypad, str(yscalebar))
    axes.text(xpos - (xscalebar/2), (ypos - ypad*3), str(xscalebar/10000), va = 'bottom',ha = 'left',)  ###NOTE need a better way to get back to seconds from data points !!!!!!!!!!!!!!!!

def mkscalebar_length(nominal_length_fraction, axslim):
    base = 10
    axsrange = axslim[1] - axslim[0]
    expnt = math.floor(math.log10(axsrange))
    singletenpower = 10**expnt
    fltrmn = float(axsrange)/float(singletenpower)
    if fltrmn>5:
        singletenpower = singletenpower*10
        addedsingletenpower = singletenpower
    elif fltrmn>1.5:
        addedsingletenpower = singletenpower * round(float(axsrange)/float(singletenpower),0)
    else:
        addedsingletenpower = singletenpower * (axsrange//singletenpower)
    scalebarlength = addedsingletenpower * nominal_length_fraction
    return scalebarlength

def mkscale_pos(axs, xfrac, yfrac):
    xrng = axs.get_xlim()[1] - axs.get_xlim()[0]
    yrng = axs.get_ylim()[1] - axs.get_ylim()[0]
    xpos = axs.get_xlim()[1] - xrng*xfrac
    ypos = axs.get_ylim()[1] - yrng*yfrac
    return xpos, ypos

def mkscale_plot_pad(axs, xpadfrac, ypadfrac):
    xrng = axs.get_xlim()[1] - axs.get_xlim()[0]
    yrng = axs.get_ylim()[1] - axs.get_ylim()[0]
    xpad = xrng*xpadfrac
    ypad = yrng*ypadfrac
    return xpad, ypad

def hideaxs(axes):
# this weird Subplot imported from the toolkits let you indivdually set the axis lines to be invisible
# now I am hiding all of the axis lines
    axes.axis["right"].set_visible(False)
    axes.axis["top"].set_visible(False)
    axes.axis["bottom"].set_visible(False)
    axes.axis["left"].set_visible(False)
    axes.patch.set_alpha(0) # set the background of the plotting axes to be transparent

class comp_cc:
    def __init__(self, cntrlfname, expfname, chan_nums, chanlims, xlims=[], pair=False):
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

    def get_data(self):
        self.cntrldata = []
        self.expdata = []
        if not(type(self.chans)==type([])):
            self.chans = [self.chans]
        for i in self.chans:
            self.cntrldata.append(son.Channel(i,self.cntrlfname).data())
            self.expdata.append(son.Channel(i,self.expfname).data())
        if (len(self.cntrldata[0].shape))==1:
            self.numblocks = 1
            self.cntrldata = []
            self.expdata = []
            for i , chan in enumerate(self.chans):
                self.cntrldata.append([son.Channel(chan,self.cntrlfname).data(),son.Channel(chan,self.cntrlfname).data()])
                self.expdata.append([son.Channel(chan,self.expfname).data(),son.Channel(chan,self.expfname).data()])
        elif (len(self.cntrldata[0].shape))>1:
            self.numblocks = self.cntrldata[0].shape[0]
        else:
            print 'crap'

    def mk_axes_order(self):
        '''either splits number of columns in the plotting into top and bottom, or if pair = True, interleaves columns'''
        length = self.fig.num_cols
        cntrl = np.r_[1:(length/2)+1]
        exp = np.r_[(length/2) + 1 : length + 1]
        if self.pair == True:
            self.cntrlord = 2*(np.r_[1:len(cntrl)+1])-1
            self.expord = 2*(np.r_[1:len(exp)+1])
        else:
            self.cntrlord = cntrl
            self.expord = exp

    def mk_axes(self, overdraw = False, pair = False):
        if self.cntrlaxes.__len__()!=0:
            hreturn

        self.fig = plt.figure()
        self.fig.patch.set_alpha(0)
        self.fig.num_rows = len(self.chans)
        self.overdraw = overdraw
        if overdraw == False:
            self.fig.num_cols = self.numblocks * 2
        else:
            self.fig.num_cols = self.numblocks
        self.mk_axes_order()
        for chan in range(len(self.chans)):
            self.cntrlaxes.append([])
            self.expaxes.append([])
            for plotnum in range(self.numblocks):
                tmpcntrlaxes = Subplot(self.fig, self.fig.num_rows, self.fig.num_cols, self.cntrlord[plotnum] + (chan*self.fig.num_cols))
                if overdraw == True:
                    tmpexpaxes = tmpcntrlaxes
                else:
                    tmpexpaxes = Subplot(self.fig, self.fig.num_rows, self.fig.num_cols, self.expord[plotnum] + (chan*self.fig.num_cols))
                self.cntrlaxes[chan].append(tmpcntrlaxes)
                self.expaxes[chan].append(tmpexpaxes)
                ### have to add each axis to object figure
                self.fig.add_subplot(tmpcntrlaxes)
                self.fig.add_subplot(tmpexpaxes)

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

    def setlims(self,diff=False):
        ''' chan lims must be an array of tuples'''
        for cond in range(2):
            for block in range(self.numblocks):
                for chan in self.chans:
                    print 'start slm'
                    print cond
                    print block
                    print chan
                    chanindx = self.chans.index(chan)
                    print self.chanlims[chanindx]
                    self.set_which_subplot(chan,cond,block)
                    print (self.currentsubplot.get_ylim())
                    self.currentsubplot.set_ylim(self.chanlims[chanindx])
                    print (self.currentsubplot.get_ylim())
                    print 'end slm'

    def set_diff_lims(self,yrangelist):
        ''' chan lims must be an array of tuples'''
        for c, chan in enumerate(self.chans):
            map(lambda axinst: axinst.set_ylim(yrangelist[c]), self.diff_axes[c])

    def setxlims(self,diff=False):
        if self.xlims == []:
            return
        ''' chan lims must be an array of tuples'''
        for cond in range(2):
            for block in range(self.numblocks):
                for chan in self.chans:
                    chanindx = self.chans.index(chan)
                    self.set_which_subplot(chan,cond,block)
                    self.currentsubplot.set_xlim(self.xlims[chanindx])

    def set_diff_xlims(self,xrangelist):
        ''' chan lims must be an array of tuples'''
        for b in range(self.numblocks):
            for c, chan in enumerate(self.chans):
                self.set_which_diff_subplot(c,b)
                self.current_diff_subplot.set_xlim(xrangelist[c])

    def make_scale_bars(self):
        subplotcntr = 0
        for chan in self.chans:
            for cond in range(2):
                for block in range(self.numblocks):
                    chanindx = self.chans.index(chan)
                    self.set_which_subplot(chan,cond,block)
                    if (is_m_edge(self.fig.num_cols, self.fig.num_rows, subplotcntr, edge='r',byrow=True)):
                        dothescalebars(self.currentsubplot, 0.1, 0.2, 0.05, 0.21, 0.01, 0.01)
                      # dothescalebars(axes, xrngfrac, yrngfrac, xposfrac, yposfrac, xpadfrac, ypadfrac):
                        
                    subplotcntr = subplotcntr + 1

    def make_diff_scale_bars(self):
        subplotcntr = 0
        for chan in self.chans:
            for block in range(self.numblocks):
                chanindx = self.chans.index(chan)
                self.set_which_diff_subplot(chanindx,block)
                if is_m_edge(self.diff_plot_cols, self.diff_plot_rows, subplotcntr, edge='r',byrow=True):
                    dothescalebars(self.current_diff_subplot, 0.1, 0.2, 0.05, 0.21, 0.01, 0.01)
                    subplotcntr = subplotcntr + 1

    def set_which_subplot(self, channum, condition, blocknum):
        chanindx = self.chans.index(channum)
        
        if condition == 0:
            self.pltdata = self.cntrldata[chanindx][blocknum]
            self.currentsubplot = self.cntrlaxes[chanindx][blocknum] # again with the modulo
        elif condition == 1:
            self.pltdata = self.expdata[chanindx][blocknum]
            self.currentsubplot = self.expaxes[chanindx][blocknum]
        else:
            print 'condition arguement is not right'

    def set_which_diff_subplot(self, chanindx, blocknum):
        if chanindx == 0:
            self.diff_plt_data = np.array([self.cntrldata[chanindx][blocknum],self.expdata[chanindx][blocknum]])
        else:
            self.diff_plt_data = self.expdata[chanindx][blocknum] - self.cntrldata[chanindx][blocknum]
        self.current_diff_subplot = self.diff_axes[chanindx][blocknum%(self.diff_plot_cols)] # again with the modulo

    def plot_all(self, addline=False, lineat=-65, **keywords):
        subplotcounter = 0
        for cond in range(2):
            for chan in self.chans:
                for block in range(self.numblocks):
                    self.set_which_subplot(chan, cond, block)
                    print(str(chan) + str(cond) + str(block))
                    print(self.currentsubplot.__repr__())
                    if cond == 0:
                        linclr = '#140060'
                    else:
                        linclr = '#B43EDE'
                    self.currentsubplot.plot(self.pltdata,color = linclr, **keywords)
                    hideaxs(self.currentsubplot)
                    subplotcounter = subplotcounter+1
                    if addline==True:
                        self.currentsubplot.axhline(lineat, linestyle = 'dashed', color = 'grey', linewidth = 0.2)

    def plot_diff(self, **keywords):
        self.mk_diff_axes()
        for chanindx, chan in enumerate(self.chans):
            for block in range(self.numblocks):
                self.set_which_diff_subplot(chanindx, block)
                if len(self.diff_plt_data.shape)>1:
                    map(lambda data: self.current_diff_subplot.plot(data, **keywords), self.diff_plt_data)
                else:
                    self.current_diff_subplot.plot(self.diff_plt_data, **keywords)
                    self.current_diff_subplot.axhline(0, linestyle= 'dashed', color = 'grey')
                hideaxs(self.current_diff_subplot)

    def add_stock_title(self, string='', x=0.5, y=0.98, **keywords):
        cntrlname = os.path.basename(self.cntrlfname).split('.')[0]
        expname = os.path.basename(self.expfname).split('.')[0]
        if not(string==''):
            self.fig.suptitle(string, x=x, y=y)
        else:
            self.fig.suptitle(cntrlname, x = 0.2, y=0.98,color= '#140060', **keywords)
            self.fig.suptitle(expname, x = 0.7, y=0.98,color= '#B43EDE',**keywords)

    def add_stock_diff_title(self, string='', x=0.5, y=0.98, **keywords):
        cntrlname = os.path.basename(self.cntrlfname).split('.')[0]
        expname = os.path.basename(self.expfname).split('.')[0]
        if not(string==''):
            self.diff_fig.suptitle(string, x=x, y=y)
        else:
            self.diff_fig.suptitle(cntrlname, x = 0.2, y=0.98,color= '#140060', **keywords)
            self.diff_fig.suptitle(expname, x = 0.7, y=0.98,color= '#B43EDE',**keywords)

