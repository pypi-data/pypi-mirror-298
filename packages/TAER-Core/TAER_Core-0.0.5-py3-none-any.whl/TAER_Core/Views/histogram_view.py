import matplotlib
g=super
j=False
m=None
r=True
d=max
F=min
n=len
hL=hasattr
hA=int
hM=zip
S=matplotlib.backends
K=matplotlib.figure
D=matplotlib.use
D("WXAgg")
from K import Figure
from S.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import wx
w=wx.RIGHT
i=wx.BOTTOM
y=wx.StaticText
c=wx.Button
W=wx.StaticBoxSizer
U=wx.GROW
V=wx.TOP
p=wx.LEFT
v=wx.Panel
H=wx.EXPAND
X=wx.ALL
e=wx.HORIZONTAL
J=wx.VERTICAL
z=wx.BoxSizer
E=wx.NullColour
u=wx.Size
T=wx.MAXIMIZE_BOX
O=wx.RESIZE_BORDER
b=wx.DEFAULT_FRAME_STYLE
R=wx.lib
import R.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class k(AuxViewBase):
 def __init__(L,h):
  g().__init__(parent=h,title="Histogram",style=b^O^T,)
  L.SetMinSize(u(0,0))
  L.__create_layout()
  L.scale_flag=j
 def __create_layout(L):
  L.SetBackgroundColour(E)
  L.vsizer=z(J)
  L.hsizer=z(e)
  L.vsizer.Add(L.hsizer,0,X,5)
  L.panel_histogram_plot=A(L)
  L.hsizer.Add(L.panel_histogram_plot,0,H)
  L.SetSizerAndFit(L.vsizer)
  L.Layout()
 def o(L,hist):
  if hist!=m and L.IsShown():
   M=hist.value[0]
   l=hist.value[1]
   L.panel_histogram_plot.update(M,l)
   L.Refresh()
 def x(L):
  L.scale_flag=r
 def q(L):
  d=L.panel_histogram_plot.txt_bin_max.GetValue()
  F=L.panel_histogram_plot.txt_bin_min.GetValue()
  P=L.panel_histogram_plot.txt_bin_step.GetValue()
  return d,F,P
class A(v):
 def __init__(L,h):
  v.__init__(L,h)
  L.__create_layout()
 def __create_layout(L):
  L.SetBackgroundColour(E)
  L.figure=I(figsize=[3.2,2.4])
  L.canvas=Q(L,-1,L.figure)
  L.axes=L.figure.add_subplot(111)
  L.sizer_main=z(J)
  L.sizer_main.Add(L.canvas,1,p|V|U)
  L.sizer_buttons=W(e,L,"Settings")
  L.sizer_main.Add(L.sizer_buttons,0,H|V,10)
  L.button_scale=c(L,label="Scale")
  L.button_scale.Enable(j)
  L.sizer_buttons.Add(L.button_scale,1,H|X,5)
  L.sizer_bins=W(e,L,"Bins definition")
  B=z(J)
  N=y(L,label="Minimum",style=p)
  B.Add(N,0,H|i,1)
  L.txt_bin_min=wxInt.IntCtrl(L,F=0,d=65535,limited=r)
  B.Add(L.txt_bin_min,1,H)
  L.sizer_bins.Add(B,0,H|i|p|w,5)
  B=z(J)
  N=y(L,label="Maximum",style=p)
  B.Add(N,0,H|i,1)
  L.txt_bin_max=wxInt.IntCtrl(L,F=0,d=65535,limited=r)
  B.Add(L.txt_bin_max,1,H)
  L.sizer_bins.Add(B,0,H|i|p|w,5)
  B=z(J)
  N=y(L,label="Number of bins",style=p)
  B.Add(N,0,H|i,1)
  L.txt_bin_step=wxInt.IntCtrl(L,F=0,d=1000,limited=r)
  B.Add(L.txt_bin_step,1,H)
  L.sizer_bins.Add(B,0,H|i|p|w,5)
  L.sizer_buttons.Add(L.sizer_bins,3,H)
  L.SetSizerAndFit(L.sizer_main)
  L.Layout()
 def Y(L,count,l):
  if n(count)<=0 or n(l)<=0:
   return
  if not hL(L,"bar_plot")or L.GetParent().scale_flag:
   L.button_scale.Enable(r)
   L.axes.cla()
   _,_,L.bar_plot=L.axes.hist(l[:-1],l,weights=count)
   L.axes.relim()
   L.txt_bin_max.ChangeValue(hA(l[-1]))
   L.txt_bin_min.ChangeValue(hA(l[0]))
   L.txt_bin_step.ChangeValue(n(l))
   L.GetParent().scale_flag=j
  else:
   G=L.bar_plot
   for a,f in hM(count,G.patches):
    f.set_height(a)
   L.axes.autoscale_view()
  L.canvas.draw()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
