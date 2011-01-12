import os
import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from NeuroTools.spike2.sonpy import son
from mpl_toolkits.axes_grid.axislines import Subplot

# path for debug purposes
os.chdir(os.path.expanduser('~' + os.sep + 'Documents' + os.sep + 'weiss_lab' + os.sep + 'b63_experiments' + os.sep + '2011_01_07'))


def hideaxs(axes):
# this weird Subplot imported from the toolkits let you indivdually set the axis lines to be invisible
# now I am hiding all of the axis lines
    axes.axis["right"].set_visible(False)
    axes.axis["top"].set_visible(False)
    axes.axis["bottom"].set_visible(False)
    axes.axis["left"].set_visible(False)

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
                    self.currentsubplot.plot(self.pltdata)
                    hideaxs(self.currentsubplot)


        ### need to return a list, or array where each element has channum, condition, and blocknum that will feed set_which_subplot
        ### the order of these triples will needs to mesh with the byrow order that the subplots were created in.

        #     ax = Subplot(ncol,nrow, currentplot)
        #     ax.patch.set_alpha(0)
        #     fig.add_subplot(ax)

        # ax.plot(spkchancntrllist[j].data()[i], color = 'black', linewidth = 0.3)
        # ax.plot(spkchanexplist[j].data()[i], color = 'blue', linewidth = 0.3)
        # hideaxs(ax)
        
        
            

###read data from spk2.smr
testclass = comp_cc('2011_01_07_0005.mpd', '2011_01_07_0006.mpd',[7,8],[(-60,20),(0,2)])
#testclass.plot_all()
testclass.plot_all()
#testclass.setlims()
testclass.fig.savefig('notworking.png')

