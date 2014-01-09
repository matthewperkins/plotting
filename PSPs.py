import csv
import pdb
import matplotlib.pyplot as plt
import numpy as np

# use this hack to add custom modules in myown locale
import sys
import os
processing_path = os.path.expanduser('~') +  os.sep + 'Documents' + os.sep + 'weiss_lab' + os.sep + 'Pyprocessing'
sys.path.append(processing_path)
plotting_path = os.path.expanduser('~') +  os.sep + 'Documents' + os.sep + 'weiss_lab' + os.sep + 'Pyprocessing'
sys.path.append(plotting_path)

from matts_toolkit import match_lead_zeros, latex_escape

class PSPreader():
    def __init__(self, filename):
        self.fid = file(filename, 'rb')
        self.filename = filename
        self.exp_date = filename[0:10]
        self.file_number = filename[11:15]

    def __repr__(self):
        print '\n\tfilename: %s, \n\t\texperiment date: %s, \n\t\tfile number: %s' % (self.filename, self.exp_date, self.file_number)

    def get_data(self):
        self.csv_reader = csv.reader(self.fid)
        if self.csv_reader.next()[0]=='FileFormatVersion':
            self.csv_version = int(self.csv_reader.next()[0])
            if self.csv_version!=0:
                print 'this scipt is meant to read v0 csv files'
        else:
            print 'this file is not as expected'
        if self.csv_reader.next()[0]=='PreSynapticCell':
            self.pre_synaptic_cell = self.csv_reader.next()[0]
        else:
            print 'need a presynaptic cell'
        if self.csv_reader.next()[0]=='PostSynapticCell':
            self.post_synaptic_cell = self.csv_reader.next()[0]
        else:
            print 'need a postsynaptic cell'
        self.data = {}
        for rownum, row in enumerate(self.csv_reader):
            label = row[0]
            data = self.csv_reader.next()
            self.data[label] = np.array(map(lambda str: float(str), data))

class PSPplotter():
    def __init__(self, filename):
        self.filename = filename
        self.reader = PSPreader(filename)
        self.reader.get_data()
        self.data = self.reader.data
        self.PSP_height = self.data['PostSynVoltageHeightPSP']
        self.postsyn_Vm = self.data['PostSynVoltagePrePSP']
        self.presyn_spk_times = self.data['PreSynSpkTimes']

    def __repr__(self):
        print 'plotter for this reader: %s' %s (self.reader.__repr__())
        
    def plot_psp_size_vs_num(self, special_notes = ''):
        ys = self.PSP_height
        xs = np.r_[1:ys.size+1]
        self.psp_vs_num_fig = self.generic_plot(xs,ys, special_notes = special_notes)
        self.add_ax0_labls(self.psp_vs_num_fig, 'PSP number', 'Post Syn PSP Size')
        self.psp_vs_num_fig.savename = self.mksavename('vsNum')

    def plot_psp_size_vs_postVm(self, special_notes =''):
        ys = self.PSP_height
        xs = self.postsyn_Vm
        self.psp_vs_postVm_fig = self.generic_plot(xs,ys,special_notes = special_notes)
        self.add_ax0_labls(self.psp_vs_postVm_fig, 'Post Syn Vm', 'Post Syn PSP Size')
        self.psp_vs_postVm_fig.savename = self.mksavename('vsPostVm')
        print self.psp_vs_postVm_fig.savename

    def plot_psp_size_vs_time(self, special_notes = ''):
        ys = self.PSP_height
        xs = self.presyn_spk_times
        self.psp_vs_time_fig = self.generic_plot(xs,ys,special_notes = special_notes)
        self.add_ax0_labls(self.psp_vs_time_fig, 'time sec', 'Post Syn PSP Size')
        self.psp_vs_time_fig.savename = self.mksavename('vsTime')

    def generic_plot(self, xs, ys, special_notes =''):
        fig = plt.figure()
        ax = plt.axes()
        ax.plot(xs,ys, linestyle ='', marker = 'o', color = 'black')
        fig.suptitle('Pre Synaptic cell:'+self.reader.pre_synaptic_cell+'Post Synaptic Cell'+self.reader.post_synaptic_cell+'exp:'+latex_escape(self.reader.exp_date)+' '+special_notes)
        fig.add_axes(ax)
        return fig
    
    def add_ax0_labls(self, fig, xlab, ylab):
        ax = fig.axes[0]
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)

    def mksavename(self, appendstr):
        basename = os.path.basename(self.reader.filename)
        basename = basename.split(os.extsep)[0]
        return basename+'_'+appendstr

    def make_all_save_all(self,special_notes = '', filetype = 'svg'):
        self.plot_psp_size_vs_time(special_notes = special_notes)
        self.plot_psp_size_vs_num(special_notes = special_notes)
        self.plot_psp_size_vs_postVm(special_notes = special_notes)
        self.psp_vs_time_fig.savefig(self.psp_vs_time_fig.savename+os.extsep+filetype)
        self.psp_vs_postVm_fig.savefig(self.psp_vs_postVm_fig.savename+os.extsep+filetype)
        self.psp_vs_num_fig.savefig(self.psp_vs_num_fig.savename+os.extsep+filetype)
        

# can never remember how to do composition
# class cc_trace(sonmod.Channel):
#     def __init__(self, channum, filename, smplrate):
#         sonchannel = sonmod.Channel(channum,filename)
#         sondata = sonchannel.data()

class PSPcomparer(PSPreader, PSPplotter):
    def __init__(self, cntrlf, expf, recovf):
        self.reader = PSPreader
        self.ploter = PSPplotter
        self.cntrl = self.reader(cntrlf)
        self.exp = self.reader(expf)
        self.recov = self.reader(recovf)
        map(lambda condition: condition.get_data(), [self.cntrl, self.exp, self.recov])
        self.pretty_numbers = match_lead_zeros([self.cntrl.file_number, self.exp.file_number, self.recov.file_number], suffix = '')

    def __repr__(self):
        print 'compare\n  control:',; self.cntrl.__repr__()
        print '  experiment:',; self.exp.__repr__()
        print '  recovery:',; self.recov.__repr__()

    def filter_data(self, timefilter = (0,0)):
        filterlist = []
        fltr_list = [self.cntrl.data, self.exp.data, self.recov.data]
        start = timefilter[0]
        endt = timefilter[1]
        self.filterlist = []
        for i , reader in enumerate([self.cntrl, self.exp, self.recov]):
            times = reader.data['PreSynSpkTimes']
            greater = np.nonzero(times>start)[0]
            less = np.nonzero(times<endt)[0]
            found = np.intersect1d(greater,less)
            self.filterlist.append(found)
            for key in reader.data.keys():
                fltr_list[i][key] = reader.data[key][found] #this only works with np array, should probably be in reader.

    def plot_psp_vs_postVm(self, xlim = (0,0), ylim =  (0,0), special_notes =''):
        self.psp_vs_postVm_fig = plt.figure()
        ax = plt.axes()
        self.psp_vs_postVm_fig.add_axes(ax)
        colors = ['black','red','green']
        labels = ['control', 'postEN', 'recovery']
        labels = map(lambda label, number: label + ' ' + number, labels, self.pretty_numbers)
        for i, data in enumerate([self.cntrl.data, self.exp.data, self.recov.data]):
            ys = data['PostSynVoltageHeightPSP']
            xs = data['PostSynVoltagePrePSP']
            ax.plot(xs, ys, linestyle = '', marker = 'o', color = colors[i], label = labels[i])
            ax.set_xlabel('Vm Post Syn Cell, just before PSP')
            ax.set_ylabel('Size of PSP')
        self.psp_vs_postVm_fig.suptitle('Pre Syn:' + self.cntrl.pre_synaptic_cell + ' Post Syn:' + self.cntrl.post_synaptic_cell + ' exp:' + self.cntrl.filename[0:10].replace('_','\_')+' '+special_notes)
        if xlim!=(0,0):
            ax.set_xlim(xlim)
        if ylim!=(0,0):
            ax.set_ylim(ylim)
        ax.legend()
        

class PSPcomparer_multi(PSPreader, PSPplotter):
    def __init__(self, cntrlfs ,expfs,recovfs):
        self.reader = PSPreader
        self.ploter = PSPplotter
        self.cntrlfs = cntrlfs
        self.expfs = expfs
        self.recovfs = recovfs
        self.contrls = []
        self.exps = []
        self.recovs = []
        self.conditions = [self.contrls, self.exps, self.recovs]
        for i, condition in enumerate([self.cntrlfs, self.expfs, self.recovfs]):
            for file in condition:
                self.conditions[i].append(self.reader(file))
                self.conditions[i][-1].get_data()
        self.cntrllabel = self.contrls[0].file_number+'-'+self.contrls[-1].file_number
        self.explabel = self.exps[0].file_number+'-'+self.exps[-1].file_number
        self.recovlabel = self.recovs[0].file_number+'-'+self.recovs[-1].file_number

    def __repr__(self):
        print 'no reprint yet',

    def filter_data(self, timefilter = (0,0)):
        filterlist = []
        fltr_list = [self.cntrl.data, self.exp.data, self.recov.data]
        start = timefilter[0]
        endt = timefilter[1]
        self.filterlist = []
        for i , reader in enumerate([self.cntrl, self.exp, self.recov]):
            times = reader.data['PreSynSpkTimes']
            greater = np.nonzero(times>start)[0]
            less = np.nonzero(times<endt)[0]
            found = np.intersect1d(greater,less)
            self.filterlist.append(found)
            for key in reader.data.keys():
                fltr_list[i][key] = reader.data[key][found] #this only works with np array, should probably be in reader.

    def plot_psp_vs_postVm(self, xlim = (0,0), ylim =  (0,0), special_notes =''):
        self.psp_vs_postVm_fig = plt.figure()
        ax = plt.axes()
        self.psp_vs_postVm_fig.add_axes(ax)
        colors = ['black','red','green']
        labels = ['control', 'postEN', 'recovery']
        for i, readerlist in enumerate(self.conditions):
            for areader in readerlist:
                ys = areader.data['PostSynVoltageHeightPSP']
                xs = areader.data['PostSynVoltagePrePSP']
                ax.plot(xs, ys, linestyle = '', marker = 'o', color = colors[i], label = labels[i])
                ax.set_xlabel('Vm Post Syn Cell, just before PSP')
                ax.set_ylabel('Size of PSP')
        if xlim!=(0,0):
            ax.set_xlim(xlim)
        if ylim!=(0,0):
            ax.set_ylim(ylim)
        pdb.set_trace()
        ax.legend()
        
