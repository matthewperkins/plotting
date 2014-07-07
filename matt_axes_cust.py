import matplotlib.pyplot as plt
import matplotlib.ticker as tckr

def reasonable_ticks(ax):
    ax.locator_params(nbins=5, axis = 'x')
    ax.locator_params(nbins=5, axis = 'y')
    # my_x_ticker = tckr.MaxNLocator(nbins = 4)
    # my_y_ticker = tckr.MaxNLocator(nbins = 4)
    # xaxis = ax.get_xaxis()
    # yaxis = ax.get_yaxis()
    # xaxis.set_major_locator(my_x_ticker)
    # yaxis.set_major_locator(my_y_ticker)

def nice_spines(ax):
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            pass
            # spine.set_position(('outward',4)) # outward by 4 points
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def iV_spines(ax):
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            spine.set_position(('data',0.0)) # 
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')


def ramp_spines(ax):
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            spine.set_position(('data',0.0)) # 
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def fI_ax_labels(ax):
    ax.set_xlabel('nA')
    ax.set_ylabel('spikes')

def fI_ify(ax):
    fI_ax_labels(ax)
    nice_spines(ax)
    reasonable_ticks(ax)

def clean_axes(ax, left_most = True, bottom_most = True):
    from matplotlib.pyplot import setp
    ax.patch.set_alpha(0)
    ax.get_figure().patch.set_alpha(0)
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom']:
            spine.set_position(('outward',0)) # outward by 0 points
        elif loc in ['right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    # turn off ticks where there is no spine
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    if bottom_most==False:
        setp(ax.get_xticklabels(), visible = False)
    elif bottom_most==True:
        setp(ax.get_xticklabels(), visible = True)
    if left_most==False:
        setp(ax.get_yticklabels(), visible = False)
    elif left_most==True:
        setp(ax.get_yticklabels(), visible = True)
    reasonable_ticks(ax)

def trace_axes(ax):
    from matplotlib.pyplot import setp
    for loc, spine in ax.spines.iteritems():
        spine.set_color('none') # don't draw spine
    setp(ax.get_xticklabels(), visible = False)
    setp(ax.get_yticklabels(), visible = False)

def tiny_axes(ax):
    params = {'axes.labelsize': 10,
              'text.fontsize': 10,
              'legend.fontsize': 10,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8}
    plt.rcParams.update(params)
    clean_axes(ax)

def set_axes_size_inches(ax, len_width_tpl):
    '''probably only works for figures with a single axes'''
    fig = ax.get_figure()
    figbbox = fig.get_window_extent()
    axbbox = ax.get_window_extent()
    width_frac = axbbox.width / figbbox.width
    height_frac = axbbox.height / figbbox.height
    width_in, height_in = len_width_tpl
    fig.set_size_inches( (width_in / width_frac , height_in / height_frac) )
    return

def set_axes_size_inches(ax, len_width_tpl):
    '''probably only works for figures with a single axes'''
    fig = ax.get_figure()
    figbbox = fig.get_window_extent()
    axbbox = ax.get_window_extent()
    width_frac = axbbox.width / figbbox.width
    height_frac = axbbox.height / figbbox.height
    width_in, height_in = len_width_tpl
    fig.set_size_inches( (width_in / width_frac , height_in / height_frac) )
    return

def set_ax_margin_inches(ax, *mar):
    '''probably only works for figures with a single axes mar as [b_in, l_in, t_in, r_in] ):'''
    b_in, l_in, t_in, r_in = mar
    fig = ax.get_figure()
    figwdth_in, fighght_in = fig.get_size_inches()
    figbbox = fig.get_window_extent()
    axbbox = ax.get_window_extent()
    axwdth_in = (axbbox.width / figbbox.width)*figwdth_in
    axhght_in = (axbbox.height / figbbox.height)*fighght_in
    new_fig_wdth_in = (l_in+r_in)+axwdth_in
    new_fig_hght_in = (b_in+t_in)+axhght_in
    fig.set_size_inches( (new_fig_wdth_in, new_fig_hght_in) )
    # ax pos is [left, bottom, width, height] in 0 -1 coords
    left = l_in/new_fig_wdth_in
    bottom = b_in/new_fig_hght_in
    width = axwdth_in/new_fig_wdth_in
    height = axhght_in/new_fig_hght_in
    ax.set_position([left, bottom, width, height])

def no_spines(ax):
    ax.patch.set_alpha(0)
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','bottom','right','top']:
            spine.set_color('none') # don't draw spine
        else:
            raise ValueError('unknown spine location: %s'%loc)
    # turn off ticks where there is no spine
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def only_btm_spine(ax):
    ax.patch.set_alpha(0)
    for loc, spine in ax.spines.iteritems():
        if loc in ['left','right','top']:
            spine.set_color('none') # don't draw spine
        elif loc=='bottom':
            spine.set_color('black')
        else:
            raise ValueError('unknown spine location: %s'%loc)
    # turn off ticks where there is no spine
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

def xscale(ax,
           xspn_data, xloc_axs = 0.8, xalgn = 'right',
           yspn_axs = 0.01, yloc_axs = 0.9, yalgn = 'top',
           unitstr = 'sec', lbl_pos = 'above', lbl_vis = True,
           lbl_pad_axs = 0.02, formt_labl = "%d %s",
           **kwargs):
    import matplotlib.transforms as transforms
    import matplotlib.patches as patches
    import numpy as np

    # lets make this simple, resizing plot after adding scale bars
    # could fuck this up
    xrng = np.diff(np.array(ax.get_xlim()))[0]
    yrng = np.diff(np.array(ax.get_ylim()))[0]
    xspn_axs = xspn_data / xrng

    # xstuff
    if xalgn=='left':
        xleft, xcntr, xright = (xloc_axs,
                                xloc_axs + xspn_axs/2.,
                                xloc_axs + xspn_axs)
    elif xalgn=='center':
        xleft, xcntr, xright = (xloc_axs - xspn_axs/2.,
                                xloc_axs,
                                xloc_axs + xspn_axs/2.)
    else:
        xleft, xcntr, xright = (xloc_axs - xspn_axs,
                                xloc_axs - xspn_axs/2.,
                                xloc_axs)

    # ystuff
    if yalgn=='top':
        ytop, ycntr, ybttm = (yloc_axs,
                              yloc_axs - yspn_axs/2.,
                              yloc_axs - yspn_axs)
    elif yalgn=='center':
        ytop, ycntr, ybttm = (yloc_axs + yspn_axs/2.,
                              yloc_axs,
                              yloc_axs - yspn_axs/2.)
    else:
        ytop, ycntr, ybttm = (yloc_axs - yspn_axs,
                              yloc_axs - yspn_axs/2.,
                              yloc_axs)

    if 'BAR' in kwargs.keys():
        barkwargs = kwargs.pop('BAR')
    else:
        barkwargs = {}
    rect = patches.Rectangle((xleft,ybttm),
                             width=xspn_axs, height=yspn_axs,
                         transform=ax.transAxes, **barkwargs)
    if lbl_vis:
        formtd_labl = formt_labl % (xspn_data, unitstr)
        if 'LBL' in kwargs.keys():
            lblkwargs = kwargs.pop('LBL')
        else:
            lblkwargs = {}
        if lbl_pos=='above':
            ax.text(xleft, ytop+lbl_pad_axs, formtd_labl,
                    transform=ax.transAxes, va = 'top', **lblkwargs)
        else:
            ax.text(xleft, ybttm-lbl_pad_axs, formtd_labl,
                    transform=ax.transAxes, va = 'bottom', **lblkwargs)
    ax.add_patch(rect)
    ax.figure.canvas.draw()
    return {'x':(xleft, xright),'y':(ytop,ybttm)}

def yscale(ax,
           yspn_data, yloc_axs = 0.88, yalgn = 'top',
           xspn_axs = 0.01, xloc_axs = 0.8, xalgn = 'right',
           unitstr = 'mV', lbl_pos = 'right', lbl_vis = True,
           lbl_pad_axs = 0.01, formt_labl = "%d %s",
           **kwargs):
    import matplotlib.transforms as transforms
    import matplotlib.patches as patches
    import numpy as np

    # lets make this simple, resizing plot after adding scale bars
    # could fuck this up
    xrng = np.diff(np.array(ax.get_xlim()))[0]
    yrng = np.diff(np.array(ax.get_ylim()))[0]
    yspn_axs = yspn_data / yrng

    # xstuff
    if xalgn=='left':
        xleft, xcntr, xright = (xloc_axs,
                                xloc_axs + xspn_axs/2.,
                                xloc_axs + xspn_axs)
    elif xalgn=='center':
        xleft, xcntr, xright = (xloc_axs - xspn_axs/2.,
                                xloc_axs,
                                xloc_axs + xspn_axs/2.)
    else:
        xleft, xcntr, xright = (xloc_axs - xspn_axs,
                                xloc_axs - xspn_axs/2.,
                                xloc_axs)

    # ystuff
    if yalgn=='top':
        ytop, ycntr, ybttm = (yloc_axs,
                              yloc_axs - yspn_axs/2.,
                              yloc_axs - yspn_axs)
    elif yalgn=='center':
        ytop, ycntr, ybttm = (yloc_axs + yspn_axs/2.,
                              yloc_axs,
                              yloc_axs - yspn_axs/2.)
    else:
        ytop, ycntr, ybttm = (yloc_axs - yspn_axs,
                              yloc_axs - yspn_axs/2.,
                              yloc_axs)

    if 'BAR' in kwargs.keys():
        barkwargs = kwargs.pop('BAR')
    else:
        barkwargs = {}
    rect = patches.Rectangle((xleft,ybttm),
                             width=xspn_axs, height=yspn_axs,
                         transform=ax.transAxes, **barkwargs)
    if lbl_vis:
        if 'LBL' in kwargs.keys():
            lblkwargs = kwargs.pop('LBL')
        else:
            lblkwargs = {}
        formtd_labl = formt_labl % (yspn_data, unitstr)
        if lbl_pos=='left':
            print(xleft, xcntr, xright)
            ax.text(xleft-xspn_axs-lbl_pad_axs, ycntr, formtd_labl,
                    transform=ax.transAxes, ha = 'right', **lblkwargs)
        else:
            print(xleft, xcntr, xright)
            ax.text(xright+xspn_axs+lbl_pad_axs, ycntr, formtd_labl,
                    transform=ax.transAxes, ha = 'left', **lblkwargs)
    ax.add_patch(rect)
    ax.figure.canvas.draw()
    return {'x':(xleft, xright),'y':(ytop,ybttm)}
