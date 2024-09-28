import wx
j=super
u=wx.LEFT
f=wx.ALIGN_RIGHT
N=wx.ALIGN_CENTER_VERTICAL
U=wx.TOP
r=wx.ALIGN_CENTER
Y=wx.GridSizer
w=wx.ID_ANY
a=wx.Button
L=wx.TE_READONLY
g=wx.TE_CENTER
i=wx.TextCtrl
b=wx.CENTER
t=wx.StaticText
o=wx.Panel
l=wx.EXPAND
J=wx.ALL
X=wx.HORIZONTAL
K=wx.VERTICAL
e=wx.BoxSizer
E=wx.NullColour
s=wx.Size
M=wx.MAXIMIZE_BOX
c=wx.RESIZE_BORDER
I=wx.DEFAULT_FRAME_STYLE
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class F(AuxViewBase):
 def __init__(S,R):
  j().__init__(parent=R,title="SERIAL debugger",style=I^c^M,)
  S.SetMinSize(s(0,0))
  S.__create_layout()
 def __create_layout(S):
  S.SetBackgroundColour(E)
  S.vsizer=e(K)
  S.hsizer=e(X)
  S.vsizer.Add(S.hsizer,0,J,5)
  S.panel_serial_control=q(S)
  S.hsizer.Add(S.panel_serial_control,0,l)
  S.SetSizerAndFit(S.vsizer)
  S.Layout()
class q(o):
 def __init__(S,R):
  o.__init__(S,R)
  S.__create_layout()
 def __create_layout(S):
  v=t(S,label="SERIAL TX data",style=b)
  S.serial_tx_box=i(S,value="",style=g)
  D=t(S,label="SERIAL RX data",style=b)
  S.serial_rx_box=i(S,value="",style=g|L)
  S.btn_write=a(S,w,"Write SERIAL")
  S.vsizer=e(K)
  S.main_grid=Y(2,0,0)
  S.main_grid.Add(v,0,r|U,5)
  S.main_grid.Add(S.serial_tx_box,0,N|f|u|U,5,)
  S.main_grid.Add(D,0,r|U,5)
  S.main_grid.Add(S.serial_rx_box,0,N|f|u|U,5,)
  S.vsizer.Add(S.main_grid,0,J,1)
  S.vsizer.Add(S.btn_write,0,f|J,5)
  S.SetSizer(S.vsizer)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
