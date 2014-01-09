import os
import sys
import numpy as np
import pdb

#setables
cntrl = '2011_02_08_0024_B63L_to_B31-32R_PSP.csv'
postEn = '2011_02_08_0035_B63L_to_B31-32R_PSP.csv'
recov = '2011_02_08_0041_B63L_to_B31-32R_PSP.csv'

sys.path.append(os.path.expanduser('~') + '/Documents/weiss_lab/Pyplotting/')
import PSPs

for csvfile in [cntrl, postEn, recov]:
    pp = PSPs.PSPplotter(csvfile)
    pp.make_all_save_all(filetype = 'png')

pc = PSPs.PSPcomparer(cntrl, postEn, recov)
pc.filter_data(timefilter = (0,18))
pc.plot_psp_vs_postVm(xlim = (-80,-50), ylim = (0,15))
pc.psp_vs_postVm_fig.savefig('cntrl('+pc.cntrl.file_number+')-postEN('+pc.exp.file_number+')-recov('+pc.recov.file_number+')-b63-to-b31-psp.svg')
