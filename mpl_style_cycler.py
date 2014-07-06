from itertools import product, izip
import numpy as np


keylist = ['marker',
           'markerfacecolor',
           'color',
           'linewidth',
           'markeredgewidth',
           'markersize',
           'markeredgecolor',
           'alpha']

pkeylist = [('marker','markerfacecolor'),
            'color',
            'linewidth',
            'markeredgewidth',
            'markersize',
            'markeredgecolor',
            'alpha']

style_dict = {\
    'marker':['s','o','v', '^', '>', '<'],
    'markerfacecolor':['None','Black'],
    'color':'Black',
    'linewidth':0.5,
    'markeredgewidth':0.5,
    'markersize':3.5,
    'markeredgecolor':'Black',
    'alpha':1,
    }

pstyle_dict = {\
    'marker':['s','o','v', '^', '>', '<'],
    'markerfacecolor':['None','Black','Blue','Red','Green','Yellow'],
    'color':'Black',
    'linewidth':0.5,
    'markeredgewidth':0.5,
    'markersize':3.5,
    'markeredgecolor':'Black',
    'alpha':1,
    }

########## check out my closures ##########
def style_cycler(keylist, style_dict):
    itr_style_dict = {}
    # reverse order of keylist, so top cycle first
    keylist.reverse()
    for (k,v) in style_dict.iteritems():
        itr_style_dict[k] = [v] if type(v) is not type([]) else v 

    simple_keys = np.array([type(k)==type('') for k in keylist])
    tpl_keys = np.array([type(k)==type(()) for k in keylist])
    if np.all(simple_keys):
        ITR =  product(*[itr_style_dict[k] for k in keylist])
    elif np.any(tpl_keys):
        pair_key_idxs = np.where(tpl_keys)[0]
        nrm_key_idxs = np.where(simple_keys)[0]
        itr = [None]*len(keylist)
        pair_key_itrs = []
        for i in pair_key_idxs:
            itr[i] = izip(*[itr_style_dict[k] for k in keylist[i]])
        for j in nrm_key_idxs:
            itr[j] = itr_style_dict[keylist[j]]
        ITR = product(*itr)

    def nv():
        values = ITR.next()
        d = dict(zip(keylist,values))
        for k in d.keys():
            if type(k) is type(()):
                v = d.pop(k)
                for i,sk in enumerate(k):
                    d[sk]=v[i]
        return d
    return nv
    
    



