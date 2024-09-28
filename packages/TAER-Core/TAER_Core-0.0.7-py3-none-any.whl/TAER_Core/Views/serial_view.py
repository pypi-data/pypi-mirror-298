import wx
H=super
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class E(AuxViewBase):
 def __init__(V,A):
  H().__init__(parent=A,title="SERIAL debugger",style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX,)
  V.SetMinSize(wx.Size(0,0))
  V.__create_layout()
 def __create_layout(V):
  V.SetBackgroundColour(wx.NullColour)
  V.vsizer=wx.BoxSizer(wx.VERTICAL)
  V.hsizer=wx.BoxSizer(wx.HORIZONTAL)
  V.vsizer.Add(V.hsizer,0,wx.ALL,5)
  V.panel_serial_control=b(V)
  V.hsizer.Add(V.panel_serial_control,0,wx.EXPAND)
  V.SetSizerAndFit(V.vsizer)
  V.Layout()
class b(wx.Panel):
 def __init__(V,A):
  wx.Panel.__init__(V,A)
  V.__create_layout()
 def __create_layout(V):
  t=wx.StaticText(V,label="SERIAL TX data",style=wx.CENTER)
  V.serial_tx_box=wx.TextCtrl(V,value="",style=wx.TE_CENTER)
  X=wx.StaticText(V,label="SERIAL RX data",style=wx.CENTER)
  V.serial_rx_box=wx.TextCtrl(V,value="",style=wx.TE_CENTER|wx.TE_READONLY)
  V.btn_write=wx.Button(V,wx.ID_ANY,"Write SERIAL")
  V.vsizer=wx.BoxSizer(wx.VERTICAL)
  V.main_grid=wx.GridSizer(2,0,0)
  V.main_grid.Add(t,0,wx.ALIGN_CENTER|wx.TOP,5)
  V.main_grid.Add(V.serial_tx_box,0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.TOP,5,)
  V.main_grid.Add(X,0,wx.ALIGN_CENTER|wx.TOP,5)
  V.main_grid.Add(V.serial_rx_box,0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.LEFT|wx.TOP,5,)
  V.vsizer.Add(V.main_grid,0,wx.ALL,1)
  V.vsizer.Add(V.btn_write,0,wx.ALIGN_RIGHT|wx.ALL,5)
  V.SetSizer(V.vsizer)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
