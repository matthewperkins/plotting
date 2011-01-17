import os
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
#from NeuroTools.spike2.sonpy import son
from son import son
from mpl_toolkits.axes_grid.axislines import Subplot

# path for debug purposes
os.chdir(os.path.expanduser('~' + os.sep + 'Documents' + os.sep + 'weiss_lab' + os.sep + 'B63_experiments' + os.sep + '2011_01_07'))


def hideaxs(axes):
# this weird Subplot imported from the toolkits let you indivdually set the axis lines to be invisible
# now I am hiding all of the axis lines
    axes.axis["right"].set_visible(False)
    axes.axis["top"].set_visible(False)
    axes.axis["bottom"].set_visible(False)
    axes.axis["left"].set_visible(False)
    axes.patch.set_alpha(0) # set the background of the plotting axes to be transparent 

def smatrixedge(ncols, nrows, sindx, edge='b', byrow=False):
    ## edge should equal 'b', 'l', 't', 'r', for bottow, left, top, right.
    ## if matrix is made byrow = True, than single indexs(sindx) will
    ## not jibe with the order that the matrix was orginally filled, to
    ## work around I do some fancy divison, / is floor division, so
    ## s / ncols + 1 will be the row index and s % ncols is
    ## the col index, expanding this now to know if I am at any edge

    if(byrow):
        rindx = sindx/ncols+1 ## int/int is floor division
        cindx = sindx%ncols    ## int%int is modulo 
        if (cindx==0):
            rindx = rindx-1; cindx = ncols
        else:
            cindx = sindx/nrows+1
            rindx = sindx%nrows
            if (rindx==0):
                cindx = cindx-1; rindx = nrows
                
    if edge =='b':
        if rindx==nrows:
            return (True)
        else:
            return (False)
    if edge == 'l':
        if cindx==1:
            return (True)
        else: return (False)
    if edge == 't':
        if rindx==1:
            return (True)
        else:
            return (False)
    if edge == 'r':
        if cindx==ncols:
            return (True)
        else: 
            return (False)
class comp_cc:
    def __init__(self,cntrlfname,expfname,chan_nums, chanlims):
        self.cntrlfname = cntrlfname
        self.expfname = expfname
        self.chans = chan_nums
        self.chanlims = chanlims
        self.get_data()
        self.cntrlaxes = []
        self.expaxes = []
        self.mk_axes()
        self.setlims()

    def get_data(self):
        self.cntrldata = []
        self.expdata = []
        for i in self.chans:
            self.cntrldata.append(son.Channel(i,self.cntrlfname).data())
            self.expdata.append(son.Channel(i,self.expfname).data())

    def mk_axes_order(self, pair = False):
        '''either splits number of columns in the plotting into top and bottom, or if pair = True, interleaves columns'''
        length = self.plot_cols
        cntrl = np.r_[1:(length/2)+1]
        exp = np.r_[(length/2) + 1 : length + 1]
        if pair == True:
            self.cntrlord = 2*(np.r_[1:len(cntrl)+1])-1
            self.expord = 2*(np.r_[1:len(exp)+1])
        else:
            self.cntrlord = cntrl
            self.expord = exp

    def setlims(self):
        ''' chan lims must be an array of tuples'''
        for cond in range(2):
            for block in range(self.numblocks):
                for chan in self.chans:
                    chanindx = self.chans.index(chan)
                    self.set_which_subplot(chan,cond,block)
                    self.currentsubplot.set_ylim(self.chanlims[chanindx])  
                         
    def mk_axes(self,overdraw = False, pair = False):
        if self.cntrlaxes.__len__()!=0:
            return
        
        self.fig = plt.figure()
        self.plot_rows = len(self.chans)
        self.numblocks = self.cntrldata[0].shape[0]
        self.overdraw = overdraw
        if overdraw == False:
            self.plot_cols = self.numblocks * 2
        else:
            self.plot_cols = self.numblocks
        self.mk_axes_order(pair)
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

    def plot_all(self):
        for cond in range(2):
            for chan in self.chans:
                for block in range(self.numblocks):
                    self.set_which_subplot(chan, cond, block)
                    print(str(chan) + str(cond) + str(block))
                    print(self.currentsubplot.__repr__())
                    lnwdth = 0.5
                    if cond == 0:
                        linclr = 'black'
                    else:
                        linclr = 'blue'
                    self.currentsubplot.plot(self.pltdata,color = linclr, linewidth = lnwdth)
                    hideaxs(self.currentsubplot)

#    def mk_scale_bars(self)



###read data from spk2.smr
testclass = comp_cc('2011_01_07_0005.mpd', '2011_01_07_0006.mpd', [7,8] , [(-60,20),(0,2)] )
testclass.plot_all()
testclass.setlims()
testclass.fig.savefig('notworking.svg')

