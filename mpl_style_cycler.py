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
import pdb

class cycling_dict(OrderedDict):
    ''' specialized dictionary for creating style cycles
    for matplotlib plotting, keys should be Line2D properties'''
    def __init__(self, *args, **kwds):
        super(cycling_dict, self).__init__(*args, **kwds)
        self._mk_itrs()
        self._itr_order = self.keys()
        self._initial_par_set = True

    def _reset_itrs(self):
        # to reset to top of cycle
        del self._key_list_ro_itr
        self._initial_par_set = True
        self._mk_itrs()

    # # over ride setitem so that iterator are created with each change
    def __setitem__(self, k, v):
        super(cycling_dict, self).__setitem__(k,v)
        self._mk_itrs()

    def _mk_itrs(self):
        # step 1: make an iter out of each value, so that next can be called on each value.
        
        # step 2: make an iter for the entire dictionary, that is a
        # set of nested value iterators

        # step 3: create order so that the dictionary wide iter increments in a useful way

        # step 1:
        # create for each list specificied by key make a rollover iter
        # borrowed from itertools examples
        def _rollover_iter(iterable):
            # cycle('ABCD') --> A B C D A B C D A B C D ...
            # lists with a single item cycle and never rollover
            # if len(iterable)==1:
            #     saved = iterable[0]
            #     yield (0, saved)
            #     while saved:
            #         yield (0, saved)
            # list with multiple items cycle and rollover
            saved = []
            rollover = 0
            for element in iterable:
                yield (rollover, element)
                saved.append(element)
            while saved:
                rollover = 1
                for element in saved:
                    yield (rollover, element)
                    rollover = 0
            
        self._key_list_ro_itr = {}
        for k,v in self.iteritems():
            if type(v)!=type([]):
                self._key_list_ro_itr[k] = _rollover_iter([v])
            else:
                self._key_list_ro_itr[k] = _rollover_iter(v)

    def _set_order(self, nested_key_list):
        # to do: rework this so that can pass in tuples that will be
        # simultaneously incremented

        self._itr_order = []
        for k in nested_key_list:
            if k in self._key_list_ro_itr.keys():
                self._itr_order.append(k)
        for k in self._key_list_ro_itr.keys():
            if k not in nested_key_list:
                self._itr_order.append(k)

    def _next_par_set(self, ord_num = 0):
        if self._initial_par_set:
            self._result = {}
            for k in self.keys():
                ro, self._result[k] = self._key_list_ro_itr[k].next()
            self._initial_par_set = False
            return self._result.copy()
        else:
            k = self._itr_order[ord_num]
            ro, self._result[k] = self._key_list_ro_itr[k].next()
            if ro:
                next_ord = ord_num+1
                if next_ord==len(self._itr_order):
                    next_ord = 0
                self._next_par_set(ord_num = next_ord)
                return self._result
            return self._result.copy()

MHP_default = simple_style_dict  = {\
               'marker':['s','o','v', '^', '>', '<'],
               'markerfacecolor':['None','Black'],
               'color':'Black',
               'markeredgewidth':0.8,
               'markersize':7,
               'markeredgecolor':'Black',
               'alpha':0.6,
               }
    
MHP_styler = cycling_dict(MHP_default)
MHP_styler._set_order([\
        'markerfacecolor',
        'marker',
        ])

## an example:
if __name__=='__main__':
    for i in np.linspace(0,100,16):
        plt.plot(np.random.normal(i,1,100), **MHP_styler._next_par_set())
