import wx
j=super
i=wx.ALIGN_LEFT
U=wx.RIGHT
P=wx.ALIGN_RIGHT
p=wx.LEFT
F=wx.CENTER
a=wx.StaticText
C=wx.ALIGN_CENTER_HORIZONTAL
A=wx.ALL
T=wx.GridSizer
x=wx.VERTICAL
u=wx.HORIZONTAL
J=wx.BoxSizer
H=wx.NullColour
b=wx.MAXIMIZE_BOX
O=wx.RESIZE_BORDER
S=wx.DEFAULT_FRAME_STYLE
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class s(AuxViewBase):
 def __init__(v,Q):
  j().__init__(parent=Q,title="Device info",style=S^O^b,)
  v.__create_layout()
 def __create_layout(v):
  v.SetBackgroundColour(H)
  v.hsizer=J(u)
  v.vsizer=J(x)
  v.grid=T(2,5,0)
  v.hsizer.Add(v.vsizer,0,A,1)
  v.vsizer.Add(v.grid,0,C|A,20)
  v.__create_info_table()
  v.SetSizerAndFit(v.hsizer)
  v.Layout()
 def __create_info_table(v):
  v.txt_label_vendor=a(v,style=F,label="Vendor:")
  v.txt_value_vendor=a(v,style=p)
  v.grid.Add(v.txt_label_vendor,0,P|U,10)
  v.grid.Add(v.txt_value_vendor,0,i)
  v.txt_label_model=a(v,style=F,label="Model:")
  v.txt_value_model=a(v,style=p)
  v.grid.Add(v.txt_label_model,0,P|U,10)
  v.grid.Add(v.txt_value_model,0,i)
  v.txt_label_sn=a(v,style=F,label="Serial number:")
  v.txt_value_sn=a(v,style=p)
  v.grid.Add(v.txt_label_sn,0,P|U,10)
  v.grid.Add(v.txt_value_sn,0,i)
  v.txt_label_dev_version=a(v,style=F,label="Device version:")
  v.txt_value_dev_version=a(v,style=p)
  v.grid.Add(v.txt_label_dev_version,0,P|U,10)
  v.grid.Add(v.txt_value_dev_version,0,i)
 def G(v,info):
  v.txt_value_vendor.SetLabel(info.vendor)
  v.txt_value_model.SetLabel(info.product_name)
  v.txt_value_sn.SetLabel(info.serial_number)
  v.txt_value_dev_version.SetLabel(info.dev_version)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
