import re
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.axislines import Subplot

#say which data to import, assume axon text files
class atfimport:
    def __init__(self,str):
        self.filename = str
        self.open()
        self.parseatf()

    def open(self):
        self.file = file(self.filename, 'rt')
        self.lines = self.makelineskips()
        self.filelen = len(self.lines)


    def makelineskips(self):
      self.file.seek(0)
      linlen = 0
      offset = []
      for line in self.file:
          linlen = len(line)+linlen
          offset.append(linlen)
      
      return offset

    def skipto(self,linenum):
        if linenum==0:
            self.file.seek(0)
        else:
            self.file.seek(self.lines[linenum-1])
        
    def parseatf(self):
        self.skipto(0)
        line0 = self.file.readline()
        if (line0=='ATF\t1.0\r\n'):
            line = self.file.readline()
            line = line.strip('\r\n')
            line = line.split('\t')
            self.numheaders =  int(line[0].strip(' ')) + 3
            self.datalen = self.filelen - self.numheaders
            self.numcols = int(line[1])
            for x in range(self.numheaders):
                tmpline = self.file.readline()
                if (re.search('Signals=', tmpline)):
                    tmpline = tmpline.strip('\r\n')
                    tmpline = tmpline.split('\t')
                    self.signals = map(lambda signal: signal.strip('"'), tmpline)[1:]
            self.skipto(self.numheaders)
            self.data = np.zeros([self.datalen,self.numcols],dtype='float64')
            linecounter = 0
            for line in self.file:
                line = line.strip('\r\n')
                self.data[linecounter] = line.split('\t')
                linecounter = linecounter + 1
        else: return ('this is not the right kind of Axon Text File, I don\'t think')

def plottraces(atfobj):

    # plt.figure creates a matplotlib.figure.Figure instance
    fig = plt.figure()
    rect = fig.patch # a rectangle instance
    rect.set_alpha(0) # set the background of the figure to be transparent

    #use the weird Subplot imported from the toolkits to make your axes container?
    #then add this axes to to figure explicitly
    ax1 = Subplot(fig,111)
    ax1.patch.set_alpha(0) # set the background of the plotting axes to be transparent 
    fig.add_subplot(ax1)

    # this weird Subplot imported from the toolkits let you indivdually set the axis lines to be invisible
    # now I am hiding all of the axis lines
    ax1.axis["right"].set_visible(False)
    ax1.axis["top"].set_visible(False)
    ax1.axis["bottom"].set_visible(False)
    ax1.axis["left"].set_visible(False)

    ax1.plot(atfobj.data[:,1],color = 'black')
    ax1.plot(atfobj.data[:,2]+0.06, color = 'blue')
    return fig

###main
test1 = atfimport('posts-1.atf')

mpl.rcParams['path.simplify'] = True
simplifyseq = [0,0.01,0.1,0.2,0.5]

for thresh in simplifyseq:
    mpl.rcParams['path.simplify_threshold'] = thresh
    fig = plottraces(test1)
    fig.savefig('heppp_thrsh_' + str(thresh) + '_.svg')
