import wx
l=super
F=wx.LEFT
H=wx.ALIGN_RIGHT
y=wx.ALIGN_CENTER_VERTICAL
m=wx.TOP
D=wx.ALIGN_CENTER
q=wx.GridSizer
r=wx.ID_ANY
g=wx.Button
W=wx.TE_READONLY
k=wx.TE_CENTER
e=wx.TextCtrl
w=wx.CENTER
V=wx.StaticText
S=wx.Panel
c=wx.EXPAND
T=wx.ALL
b=wx.HORIZONTAL
a=wx.VERTICAL
N=wx.BoxSizer
P=wx.NullColour
i=wx.Size
j=wx.MAXIMIZE_BOX
p=wx.RESIZE_BORDER
n=wx.DEFAULT_FRAME_STYLE
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class Y(AuxViewBase):
 def __init__(E,I):
  l().__init__(parent=I,title="SERIAL debugger",style=n^p^j,)
  E.SetMinSize(i(0,0))
  E.__create_layout()
 def __create_layout(E):
  E.SetBackgroundColour(P)
  E.vsizer=N(a)
  E.hsizer=N(b)
  E.vsizer.Add(E.hsizer,0,T,5)
  E.panel_serial_control=Q(E)
  E.hsizer.Add(E.panel_serial_control,0,c)
  E.SetSizerAndFit(E.vsizer)
  E.Layout()
class Q(S):
 def __init__(E,I):
  S.__init__(E,I)
  E.__create_layout()
 def __create_layout(E):
  X=V(E,label="SERIAL TX data",style=w)
  E.serial_tx_box=e(E,value="",style=k)
  C=V(E,label="SERIAL RX data",style=w)
  E.serial_rx_box=e(E,value="",style=k|W)
  E.btn_write=g(E,r,"Write SERIAL")
  E.vsizer=N(a)
  E.main_grid=q(2,0,0)
  E.main_grid.Add(X,0,D|m,5)
  E.main_grid.Add(E.serial_tx_box,0,y|H|F|m,5,)
  E.main_grid.Add(C,0,D|m,5)
  E.main_grid.Add(E.serial_rx_box,0,y|H|F|m,5,)
  E.vsizer.Add(E.main_grid,0,T,1)
  E.vsizer.Add(E.btn_write,0,H|T,5)
  E.SetSizer(E.vsizer)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
