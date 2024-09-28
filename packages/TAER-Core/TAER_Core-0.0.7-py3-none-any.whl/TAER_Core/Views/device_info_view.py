import wx
j=super
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class p(AuxViewBase):
 def __init__(l,S):
  j().__init__(parent=S,title="Device info",style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX,)
  l.__create_layout()
 def __create_layout(l):
  l.SetBackgroundColour(wx.NullColour)
  l.hsizer=wx.BoxSizer(wx.HORIZONTAL)
  l.vsizer=wx.BoxSizer(wx.VERTICAL)
  l.grid=wx.GridSizer(2,5,0)
  l.hsizer.Add(l.vsizer,0,wx.ALL,1)
  l.vsizer.Add(l.grid,0,wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,20)
  l.__create_info_table()
  l.SetSizerAndFit(l.hsizer)
  l.Layout()
 def __create_info_table(l):
  l.txt_label_vendor=wx.StaticText(l,style=wx.CENTER,label="Vendor:")
  l.txt_value_vendor=wx.StaticText(l,style=wx.LEFT)
  l.grid.Add(l.txt_label_vendor,0,wx.ALIGN_RIGHT|wx.RIGHT,10)
  l.grid.Add(l.txt_value_vendor,0,wx.ALIGN_LEFT)
  l.txt_label_model=wx.StaticText(l,style=wx.CENTER,label="Model:")
  l.txt_value_model=wx.StaticText(l,style=wx.LEFT)
  l.grid.Add(l.txt_label_model,0,wx.ALIGN_RIGHT|wx.RIGHT,10)
  l.grid.Add(l.txt_value_model,0,wx.ALIGN_LEFT)
  l.txt_label_sn=wx.StaticText(l,style=wx.CENTER,label="Serial number:")
  l.txt_value_sn=wx.StaticText(l,style=wx.LEFT)
  l.grid.Add(l.txt_label_sn,0,wx.ALIGN_RIGHT|wx.RIGHT,10)
  l.grid.Add(l.txt_value_sn,0,wx.ALIGN_LEFT)
  l.txt_label_dev_version=wx.StaticText(l,style=wx.CENTER,label="Device version:")
  l.txt_value_dev_version=wx.StaticText(l,style=wx.LEFT)
  l.grid.Add(l.txt_label_dev_version,0,wx.ALIGN_RIGHT|wx.RIGHT,10)
  l.grid.Add(l.txt_value_dev_version,0,wx.ALIGN_LEFT)
 def y(l,info):
  l.txt_value_vendor.SetLabel(info.vendor)
  l.txt_value_model.SetLabel(info.product_name)
  l.txt_value_sn.SetLabel(info.serial_number)
  l.txt_value_dev_version.SetLabel(info.dev_version)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
