# want to make a cycler for my line styles, so that repeated plots are
# easy to distinguish in black/white printing
# make a list of dictionarys, each dictionary will be have plot kwargs

# The kwargs are Line2D properties:
# agg_filter	:	unknown
# alpha		:	float (0.0 transparent through 1.0 opaque)         
# animated	:	[True | False]         
# antialiased or aa	:	[True | False]         
# axes		:	an :class:`~matplotlib.axes.Axes` instance         
# clip_box	:	a :class:`matplotlib.transforms.Bbox` instance         
# clip_on	:	[True | False]         
# clip_path	:	[ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
# color or c	:	any matplotlib color         
# contains	:	a callable function         
# dash_capstyle	:	['butt' | 'round' | 'projecting']         
# dash_joinstyle:	['miter' | 'round' | 'bevel']         
# dashes	:	sequence of on/off ink in points         
# data		:	2D array (rows are x, y) or two 1D arrays         
# drawstyle	:	[ 'default' | 'steps' | 'steps-pre' | 'steps-mid' | 'steps-post' ]         
# figure	:	a :class:`matplotlib.figure.Figure` instance         
# fillstyle	:	['full' | 'left' | 'right' | 'bottom' | 'top' | 'none']         
# gid		:	an id string         
# label		:	string or anything printable with '%s' conversion.         
# linestyle or ls	:	[ ``'-'`` | ``'--'`` | ``'-.'`` | ``':'`` | ``'None'`` | ``' '`` | ``''`` ]         and any drawstyle in combination with a linestyle, e.g. ``'steps--'``.         
# linewidth or lw	:	float value in points         
# lod		:	[True | False]         
# marker	:	[ ``7`` | ``4`` | ``5`` | ``6`` | ``'o'`` | ``'D'`` | ``'h'`` | ``'H'`` | ``'_'`` | ``''`` | ``'None'`` | ``None`` | ``' '`` | ``'8'`` | ``'p'`` | ``','`` | ``'+'`` | ``'.'`` | ``'s'`` | ``'*'`` | ``'d'`` | ``3`` | ``0`` | ``1`` | ``2`` | ``'1'`` | ``'3'`` | ``'4'`` | ``'2'`` | ``'v'`` | ``'<'`` | ``'>'`` | ``'^'`` | ``'|'`` | ``'x'`` | ``'$...$'`` | *tuple* | *Nx2 array* ]
# markeredgecolor or mec	:	any matplotlib color         
# markeredgewidth or mew	:	float value in points         
# markerfacecolor or mfc	:	any matplotlib color         
# markerfacecoloralt or mfcalt	:	any matplotlib color         
# markersize or ms	:	float         
# markevery	:	None | integer | (startind, stride)
# picker	:	float distance in points or callable pick function         ``fn(artist, event)``         
# pickradius	:	float distance in points         
# rasterized	:	[True | False | None]         
# snap		:	unknown
# solid_capstyle:	['butt' | 'round' |  'projecting']         
# solid_joinstyle	:	['miter' | 'round' | 'bevel']         
# transform	:	a :class:`matplotlib.transforms.Transform` instance         
# url		:	a url string         
# visible	:	[True | False]         
# xdata		:	1D array         
# ydata		:	1D array         
# zorder	:	any number         

from itertools import cycle, chain, repeat, groupby, product
from collections import OrderedDict

class cycling_dict(OrderedDict):
    ''' specialized dictionary for creating style cycles
    for matplotlib plotting, keys should be Line2D properties'''
    # to do, add a way to manipulate the order that each property gets
    # incremented
    def __init__(self, *args, **kwds):
        super(cycling_dict, self).__init__(*args, **kwds)
        for k,v in self.iteritems():
            if type(v)!=type([]):
                self[k]=[v]
        self._mk_cycle()

    def _mk_cycle(self):
        self._val_iter = product(*self.values())
        cycle_len = 0
        while 1:
            try:
                self._val_iter.next()
                cycle_len+=1
            except StopIteration:
                break 
        self._cycle_len = cycle_len
        self._val_iter = product(*self.values())
        self._val_cycle = cycle(self._val_iter)

    def cycle(self):
        while 1:
            yield dict(zip(self.keys(), self._val_cycle.next()))

    

MHP_default = simple_style_dict  = {\
               'color':'Black',
               'markeredgewidth':1
               'markersize':4,
               'markeredgecolor':['Black'],
               'markerfacecolor':['Black','White'],
               'marker':['s','o','*','D'],
               }
    
MHP_styler = cycling_dict(MHP_default)
MHP_style_loop = styler.cycle()

## an example:
if __name__=='__main__':
    simple_style_dict  = {\
               'color':'Black',
               'markeredgewidth':2,
               'markeredgecolor':['Black'],
               'markerfacecolor':['Black','White'],
               'marker':['s','o','*','D'],
               }
    
    styler = cycling_dict(simple_style_dict)
    style_loop = styler.cycle()
    for i in np.linspace(0,100,10):
        plt.plot(np.random.normal(i,1,100), markersize = 20, **style_loop.next())
