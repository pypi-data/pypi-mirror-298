import wx
N=super
n=wx.ALIGN_LEFT
E=wx.RIGHT
Y=wx.ALIGN_RIGHT
i=wx.LEFT
h=wx.CENTER
A=wx.StaticText
u=wx.ALIGN_CENTER_HORIZONTAL
W=wx.ALL
b=wx.GridSizer
V=wx.VERTICAL
C=wx.HORIZONTAL
Q=wx.BoxSizer
I=wx.NullColour
P=wx.MAXIMIZE_BOX
H=wx.RESIZE_BORDER
T=wx.DEFAULT_FRAME_STYLE
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class d(AuxViewBase):
 def __init__(F,w):
  N().__init__(parent=w,title="Device info",style=T^H^P,)
  F.__create_layout()
 def __create_layout(F):
  F.SetBackgroundColour(I)
  F.hsizer=Q(C)
  F.vsizer=Q(V)
  F.grid=b(2,5,0)
  F.hsizer.Add(F.vsizer,0,W,1)
  F.vsizer.Add(F.grid,0,u|W,20)
  F.__create_info_table()
  F.SetSizerAndFit(F.hsizer)
  F.Layout()
 def __create_info_table(F):
  F.txt_label_vendor=A(F,style=h,label="Vendor:")
  F.txt_value_vendor=A(F,style=i)
  F.grid.Add(F.txt_label_vendor,0,Y|E,10)
  F.grid.Add(F.txt_value_vendor,0,n)
  F.txt_label_model=A(F,style=h,label="Model:")
  F.txt_value_model=A(F,style=i)
  F.grid.Add(F.txt_label_model,0,Y|E,10)
  F.grid.Add(F.txt_value_model,0,n)
  F.txt_label_sn=A(F,style=h,label="Serial number:")
  F.txt_value_sn=A(F,style=i)
  F.grid.Add(F.txt_label_sn,0,Y|E,10)
  F.grid.Add(F.txt_value_sn,0,n)
  F.txt_label_dev_version=A(F,style=h,label="Device version:")
  F.txt_value_dev_version=A(F,style=i)
  F.grid.Add(F.txt_label_dev_version,0,Y|E,10)
  F.grid.Add(F.txt_value_dev_version,0,n)
 def g(F,info):
  F.txt_value_vendor.SetLabel(info.vendor)
  F.txt_value_model.SetLabel(info.product_name)
  F.txt_value_sn.SetLabel(info.serial_number)
  F.txt_value_dev_version.SetLabel(info.dev_version)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
