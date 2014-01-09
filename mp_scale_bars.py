from matplotlib.offsetbox import AnchoredOffsetbox
from matplotlib.font_manager import FontProperties as FP
import pdb
class AnchoredScaleBar(AnchoredOffsetbox):
    def __init__(self, transform, fig_transform,
                 sizex=0, sizey=0, labelx=None, labely=None, loc=4,
                 xbar_width = 2, ybar_width = 2,
                 pad=3, borderpad=0.1, xsep=3, ysep = 3, prop=None, textprops={'size':10}, **kwargs):
        """
        Draw a horizontal and/or vertical  bar with the size in data coordinate
        of the give axes. A label will be drawn underneath (center-aligned).
 
        - transform : the coordinate frame (typically axes.transData)
        - sizex,sizey : width of x,y bar, in data units. 0 to omit
        - labelx,labely : labels for x,y bars; None to omit
        - loc : position in containing axes
        - pad, borderpad : padding, in fraction of the legend font size (or prop)
        - sep : separation between labels and bars in points.
        - **kwargs : additional arguments passed to base class constructor
        """
        from matplotlib.patches import Rectangle
        from matplotlib.offsetbox import AuxTransformBox, VPacker, HPacker, TextArea, DrawingArea
        # new shit
        # try splitting the transform into X and Y so that
        import matplotlib.transforms as transforms
        xtransform = transforms.blended_transform_factory(transform, fig_transform)
        ytransform = transforms.blended_transform_factory(fig_transform, transform)
        # end new shit

        # bars = AuxTransformBox(xtransform)
        # if sizey:
        #     bars.add_artist(Rectangle((0,0), ybar_width, sizey,
        #                               fc="Black"))
        # if sizex:
        #     bars.add_artist(Rectangle((0,0), sizex, xbar_width,
        #                               fc="Black"))
 
        ybar_width /= 72.
        xbar_width /= 72.
        
        if sizey:
            ybar = AuxTransformBox(ytransform)
            ybar.add_artist(Rectangle((0,0), ybar_width, sizey, fc="Black"))
            bars = ybar
        if sizex:
            xbar = AuxTransformBox(xtransform)
            xbar.add_artist(Rectangle((0,0), sizex, xbar_width, fc="Black"))
            bars = xbar
        if sizex and sizey:
            bars = VPacker(children=[ybar, xbar], pad = 10, sep=ysep)
        if sizex and labelx:
            bars = VPacker(children=[bars, TextArea(labelx,
                                                    minimumdescent=False,
                                                    textprops = textprops)],
                           align="center", pad=0, sep=-3)
        if sizey and labely:
            bars = HPacker(children=[TextArea(labely,
                                              textprops = textprops), bars],
                            align="center", pad=0, sep=xsep)

        AnchoredOffsetbox.__init__(self, loc, pad=pad, borderpad=borderpad,
                                   child=bars, prop=prop, frameon=False, **kwargs)
 
def add_scalebar(ax, matchx=True, matchy=True, hidex=True, hidey=True, **kwargs):
    """ Add scalebars to axes
 
    Adds a set of scale bars to *ax*, matching the size to the ticks of the plot
    and optionally hiding the x and y axes
 
    - ax : the axis to attach ticks to
    - matchx,matchy : if True, set size of scale bars to spacing between ticks
                    if False, size should be set using sizex and sizey params
    - hidex,hidey : if True, hide x-axis and y-axis of parent
    - **kwargs : additional arguments passed to AnchoredScaleBars
 
    Returns created scalebar object
    """
    def f(axis):
        l = axis.get_majorticklocs()
        return len(l)>1 and (l[1] - l[0])
    
    if matchx:
        kwargs['sizex'] = f(ax.xaxis)
        kwargs['labelx'] = str(kwargs['sizex'])
    if matchy:
        kwargs['sizey'] = f(ax.yaxis)
        kwargs['labely'] = str(kwargs['sizey'])
        
    sb = AnchoredScaleBar(ax.transData, **kwargs)
    ax.add_artist(sb)
 
    if hidex : ax.xaxis.set_visible(False)
    if hidey : ax.yaxis.set_visible(False)
 
    # hide spines to
    for loc, spine in ax.spines.iteritems():
            spine.set_color('none')
    return sb

class DraggableScaleBar:
    lock = None  # only one can be animated at a time
    def __init__(self, anchoredscalebar):
        self.sb = anchoredscalebar
        self.press = None
        self.background = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.sb.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.sb.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.sb.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.sb.axes: return
        if DraggableScaleBar.lock is not None: return
        contains, attrd = self.sb.contains(event)
        if not contains: return
        if event.button==3:
            self.sb.set_visible(not(self.sb.get_visible()))
        bb = self.sb.get_bbox_to_anchor()
        print 'event contains', bb.extents
        [x0, y0], [x1, y1] = self.sb.axes.transData.inverted().transform(bb.get_points())
        self.press = x0, y0, x1, y1, event.xdata, event.ydata
        DraggableScaleBar.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.sb.figure.canvas
        axes = self.sb.axes
        self.sb.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.sb.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.sb)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if DraggableScaleBar.lock is not self:
            return
        if event.inaxes != self.sb.axes: return
        x0, y0, x1, y1, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.sb.set_bbox_to_anchor([x0+dx, y0+dy], transform = self.sb.axes.transData)

        canvas = self.sb.figure.canvas
        axes = self.sb.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.sb)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableScaleBar.lock is not self:
            return

        self.press = None
        DraggableScaleBar.lock = None

        # turn off the rect animation property and reset the background
        self.sb.set_animated(False)
        self.background = None

        # redraw the full figure
        self.sb.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.sb.figure.canvas.mpl_disconnect(self.cidpress)
        self.sb.figure.canvas.mpl_disconnect(self.cidrelease)
        self.sb.figure.canvas.mpl_disconnect(self.cidmotion)

def main():
    import matplotlib.pyplot as plt
    import numpy as np
    plt.plot(np.r_[0:100])
    ax = plt.gca()
    fig = plt.gcf()
    sb = AnchoredScaleBar(ax.transData, fig.dpi_scale_trans,
                        sizex = 10, sizey = 30,
                          labelx = '10\nsec', labely = '30\nmV',
                        bbox_to_anchor = (0.2,0.1),
                        xsep = 10, ysep = 3, pad = 3,
                        prop = FP(size=10),
                        textprops = {'size':20},
                        bbox_transform = ax.transAxes, borderpad=2)
    ax.add_artist(sb)
    dsb = DraggableScaleBar(sb)
    dsb.connect()
    plt.show()

if __name__=='__main__':
    main()
