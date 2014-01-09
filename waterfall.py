class AdvncingXs:
    # iterator for shifting xs (for waterfall plots)
    def __init__(self, YsArray, XsArray=[], AdvcFunc=lambda x:x):
        self.advcfunc = AdvcFunc
        self.shape = YsArray.shape
        self._row_indx = 0
        
        ### define the 'next' method for iteration here, to avoid if
        ### statements on each loop through
        if XsArray == []:
            num_row_ys = self.shape[-1]
            self._xs = np.r_[0:num_row_ys]
            self.next = self._next
        elif XsArray.size>0:
            self._xs = XsArray
            self.next = self._next_with_XsArray

    def _next_with_XsArray(self):
        try:
            indx = self._row_indx
            xs = self._xs[self._row_indx]
            self._row_indx += 1
            return (xs + self.advcfunc(indx))
        except IndexError:
            self._row_indx = 0
            raise StopIteration

    def _next(self):
        try:
            indx = self._row_indx
            self._row_indx += 1
            return (self._xs + self.advcfunc(indx))
        except IndexError:
            self._row_indx = 0
            raise StopIteration

    def __iter__(self):
        return self


################################# to make a waterfall use is a bit
################################# kludgy right now
### sample code below
if __name__=='__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    # data is 108 sweeps of eyelid data, each sweep is 2500 points
    f = file('./test/waterfall_eyelid.dat', 'rb')
    data_array = np.fromfile(f, dtype = np.int16)
    data_array = data_array.reshape((108, -1))


    ## prep for the waterfall plot
    num_row_d = data_array.shape[1]
    xs = AdvncingXs(data_array, AdvcFunc = lambda x: 20*x)
    y_offset = 50

    # to plot this data back to front, but maintain time order, reverse
    # data and plot from the top
    data_array = data_array[::-1]
    for i, row in enumerate(data_array):
        ii = num_row_d - i
        plt.plot(xs.next(), row+(y_offset*ii), '-b')
    plt.show()
