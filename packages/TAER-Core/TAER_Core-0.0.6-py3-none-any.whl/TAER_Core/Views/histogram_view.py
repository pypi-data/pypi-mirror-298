import matplotlib
d=super
t=False
x=None
S=True
E=max
l=min
J=len
aP=hasattr
au=int
ap=zip
G=matplotlib.backends
F=matplotlib.figure
h=matplotlib.use
h("WXAgg")
from F import Figure
from G.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import wx
s=wx.RIGHT
B=wx.BOTTOM
q=wx.StaticText
f=wx.Button
i=wx.StaticBoxSizer
y=wx.GROW
o=wx.TOP
V=wx.LEFT
A=wx.Panel
W=wx.EXPAND
j=wx.ALL
k=wx.HORIZONTAL
O=wx.VERTICAL
D=wx.BoxSizer
Y=wx.NullColour
n=wx.Size
g=wx.MAXIMIZE_BOX
K=wx.RESIZE_BORDER
U=wx.DEFAULT_FRAME_STYLE
z=wx.lib
import z.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class M(AuxViewBase):
 def __init__(P,a):
  d().__init__(parent=a,title="Histogram",style=U^K^g,)
  P.SetMinSize(n(0,0))
  P.__create_layout()
  P.scale_flag=t
 def __create_layout(P):
  P.SetBackgroundColour(Y)
  P.vsizer=D(O)
  P.hsizer=D(k)
  P.vsizer.Add(P.hsizer,0,j,5)
  P.panel_histogram_plot=u(P)
  P.hsizer.Add(P.panel_histogram_plot,0,W)
  P.SetSizerAndFit(P.vsizer)
  P.Layout()
 def r(P,hist):
  if hist!=x and P.IsShown():
   p=hist.value[0]
   w=hist.value[1]
   P.panel_histogram_plot.update(p,w)
   P.Refresh()
 def R(P):
  P.scale_flag=S
 def b(P):
  E=P.panel_histogram_plot.txt_bin_max.GetValue()
  l=P.panel_histogram_plot.txt_bin_min.GetValue()
  C=P.panel_histogram_plot.txt_bin_step.GetValue()
  return E,l,C
class u(A):
 def __init__(P,a):
  A.__init__(P,a)
  P.__create_layout()
 def __create_layout(P):
  P.SetBackgroundColour(Y)
  P.figure=L(figsize=[3.2,2.4])
  P.canvas=X(P,-1,P.figure)
  P.axes=P.figure.add_subplot(111)
  P.sizer_main=D(O)
  P.sizer_main.Add(P.canvas,1,V|o|y)
  P.sizer_buttons=i(k,P,"Settings")
  P.sizer_main.Add(P.sizer_buttons,0,W|o,10)
  P.button_scale=f(P,label="Scale")
  P.button_scale.Enable(t)
  P.sizer_buttons.Add(P.button_scale,1,W|j,5)
  P.sizer_bins=i(k,P,"Bins definition")
  v=D(O)
  H=q(P,label="Minimum",style=V)
  v.Add(H,0,W|B,1)
  P.txt_bin_min=wxInt.IntCtrl(P,l=0,E=65535,limited=S)
  v.Add(P.txt_bin_min,1,W)
  P.sizer_bins.Add(v,0,W|B|V|s,5)
  v=D(O)
  H=q(P,label="Maximum",style=V)
  v.Add(H,0,W|B,1)
  P.txt_bin_max=wxInt.IntCtrl(P,l=0,E=65535,limited=S)
  v.Add(P.txt_bin_max,1,W)
  P.sizer_bins.Add(v,0,W|B|V|s,5)
  v=D(O)
  H=q(P,label="Number of bins",style=V)
  v.Add(H,0,W|B,1)
  P.txt_bin_step=wxInt.IntCtrl(P,l=0,E=1000,limited=S)
  v.Add(P.txt_bin_step,1,W)
  P.sizer_bins.Add(v,0,W|B|V|s,5)
  P.sizer_buttons.Add(P.sizer_bins,3,W)
  P.SetSizerAndFit(P.sizer_main)
  P.Layout()
 def I(P,count,w):
  if J(count)<=0 or J(w)<=0:
   return
  if not aP(P,"bar_plot")or P.GetParent().scale_flag:
   P.button_scale.Enable(S)
   P.axes.cla()
   _,_,P.bar_plot=P.axes.hist(w[:-1],w,weights=count)
   P.axes.relim()
   P.txt_bin_max.ChangeValue(au(w[-1]))
   P.txt_bin_min.ChangeValue(au(w[0]))
   P.txt_bin_step.ChangeValue(J(w))
   P.GetParent().scale_flag=t
  else:
   T=P.bar_plot
   for e,c in ap(count,T.patches):
    c.set_height(e)
   P.axes.autoscale_view()
  P.canvas.draw()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
