import matplotlib.pyplot as plt

class GSPager(object):
    ASB = type(plt.axes())
    def __init__(self,nrow,ncol):
        from matplotlib.gridspec import GridSpec as GS
        self.figs = []
        self.axes = {}
        self._fn = None
        self._nrow = nrow
        self._ncol = ncol
        self._gs = GS(self._nrow,self._ncol)
        super(GSPager, self).__init__()

    def __getitem__(self,*indxs):
        import pdb
        irow = indxs[0][0]
        icol = indxs[0][1]
        assert icol<=self._ncol, "column out of range"
        fig_i = irow//self._nrow
        row_i  = irow%self._nrow
        if fig_i>10:
            raise IndexError("Seriously, you have more than ten figs?")
        while fig_i>len(self.figs)-1:
            self.figs.append(plt.figure())
            self.axes[self.figs[-1]]=[list([[]]*self._ncol) for r in range(self._nrow)]
        tmp_fig = self.figs[fig_i]
        if tmp_fig in self.axes.keys():
            if type(self.axes[tmp_fig][row_i][icol]) is GSPager.ASB:
                pass
            elif type(self.axes[tmp_fig][row_i][icol]) is list:
                self.axes[tmp_fig][row_i][icol] = tmp_fig.add_subplot(self._gs[row_i,icol])
            return self.axes[tmp_fig][row_i][icol]
        else:
            raise KeyError
