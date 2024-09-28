import matplotlib
k=super
W=False
b=None
n=True
u=max
m=min
Q=len
F=hasattr
g=int
H=zip
matplotlib.use("WXAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import wx
import wx.lib.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class o(AuxViewBase):
 def __init__(x,M):
  k().__init__(parent=M,title="Histogram",style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX,)
  x.SetMinSize(wx.Size(0,0))
  x.__create_layout()
  x.scale_flag=W
 def __create_layout(x):
  x.SetBackgroundColour(wx.NullColour)
  x.vsizer=wx.BoxSizer(wx.VERTICAL)
  x.hsizer=wx.BoxSizer(wx.HORIZONTAL)
  x.vsizer.Add(x.hsizer,0,wx.ALL,5)
  x.panel_histogram_plot=z(x)
  x.hsizer.Add(x.panel_histogram_plot,0,wx.EXPAND)
  x.SetSizerAndFit(x.vsizer)
  x.Layout()
 def J(x,hist):
  if hist!=b and x.IsShown():
   e=hist.value[0]
   V=hist.value[1]
   x.panel_histogram_plot.update(e,V)
   x.Refresh()
 def a(x):
  x.scale_flag=n
 def s(x):
  u=x.panel_histogram_plot.txt_bin_max.GetValue()
  m=x.panel_histogram_plot.txt_bin_min.GetValue()
  j=x.panel_histogram_plot.txt_bin_step.GetValue()
  return u,m,j
class z(wx.Panel):
 def __init__(x,M):
  wx.Panel.__init__(x,M)
  x.__create_layout()
 def __create_layout(x):
  x.SetBackgroundColour(wx.NullColour)
  x.figure=X(figsize=[3.2,2.4])
  x.canvas=B(x,-1,x.figure)
  x.axes=x.figure.add_subplot(111)
  x.sizer_main=wx.BoxSizer(wx.VERTICAL)
  x.sizer_main.Add(x.canvas,1,wx.LEFT|wx.TOP|wx.GROW)
  x.sizer_buttons=wx.StaticBoxSizer(wx.HORIZONTAL,x,"Settings")
  x.sizer_main.Add(x.sizer_buttons,0,wx.EXPAND|wx.TOP,10)
  x.button_scale=wx.Button(x,label="Scale")
  x.button_scale.Enable(W)
  x.sizer_buttons.Add(x.button_scale,1,wx.EXPAND|wx.ALL,5)
  x.sizer_bins=wx.StaticBoxSizer(wx.HORIZONTAL,x,"Bins definition")
  t=wx.BoxSizer(wx.VERTICAL)
  U=wx.StaticText(x,label="Minimum",style=wx.LEFT)
  t.Add(U,0,wx.EXPAND|wx.BOTTOM,1)
  x.txt_bin_min=wxInt.IntCtrl(x,m=0,u=65535,limited=n)
  t.Add(x.txt_bin_min,1,wx.EXPAND)
  x.sizer_bins.Add(t,0,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT,5)
  t=wx.BoxSizer(wx.VERTICAL)
  U=wx.StaticText(x,label="Maximum",style=wx.LEFT)
  t.Add(U,0,wx.EXPAND|wx.BOTTOM,1)
  x.txt_bin_max=wxInt.IntCtrl(x,m=0,u=65535,limited=n)
  t.Add(x.txt_bin_max,1,wx.EXPAND)
  x.sizer_bins.Add(t,0,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT,5)
  t=wx.BoxSizer(wx.VERTICAL)
  U=wx.StaticText(x,label="Number of bins",style=wx.LEFT)
  t.Add(U,0,wx.EXPAND|wx.BOTTOM,1)
  x.txt_bin_step=wxInt.IntCtrl(x,m=0,u=1000,limited=n)
  t.Add(x.txt_bin_step,1,wx.EXPAND)
  x.sizer_bins.Add(t,0,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT,5)
  x.sizer_buttons.Add(x.sizer_bins,3,wx.EXPAND)
  x.SetSizerAndFit(x.sizer_main)
  x.Layout()
 def D(x,count,V):
  if Q(count)<=0 or Q(V)<=0:
   return
  if not F(x,"bar_plot")or x.GetParent().scale_flag:
   x.button_scale.Enable(n)
   x.axes.cla()
   _,_,x.bar_plot=x.axes.hist(V[:-1],V,weights=count)
   x.axes.relim()
   x.txt_bin_max.ChangeValue(g(V[-1]))
   x.txt_bin_min.ChangeValue(g(V[0]))
   x.txt_bin_step.ChangeValue(Q(V))
   x.GetParent().scale_flag=W
  else:
   c=x.bar_plot
   for p,G in H(count,c.patches):
    G.set_height(p)
   x.axes.autoscale_view()
  x.canvas.draw()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
