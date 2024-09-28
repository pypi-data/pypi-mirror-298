import wx
ڋ=super
𐲤=wx.ALIGN_LEFT
𐳅=wx.RIGHT
𐰷=wx.ALIGN_RIGHT
ﲔ=wx.LEFT
𫛬=wx.CENTER
𒆶=wx.StaticText
ࠃ=wx.ALIGN_CENTER_HORIZONTAL
梺=wx.ALL
𞺔=wx.GridSizer
왿=wx.VERTICAL
ﱒ=wx.HORIZONTAL
剩=wx.BoxSizer
𞠦=wx.NullColour
𐤑=wx.MAXIMIZE_BOX
𤶢=wx.RESIZE_BORDER
𛀐=wx.DEFAULT_FRAME_STYLE
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class 㧊(AuxViewBase):
 def __init__(𰰛,𦹛):
  ڋ().__init__(parent=𦹛,title="Device info",style=𛀐^𤶢^𐤑,)
  𰰛.__create_layout()
 def __create_layout(𰰛):
  𰰛.SetBackgroundColour(𞠦)
  𰰛.hsizer=剩(ﱒ)
  𰰛.vsizer=剩(왿)
  𰰛.grid=𞺔(2,5,0)
  𰰛.hsizer.Add(𰰛.vsizer,0,梺,1)
  𰰛.vsizer.Add(𰰛.grid,0,ࠃ|梺,20)
  𰰛.__create_info_table()
  𰰛.SetSizerAndFit(𰰛.hsizer)
  𰰛.Layout()
 def __create_info_table(𰰛):
  𰰛.txt_label_vendor=𒆶(𰰛,style=𫛬,label="Vendor:")
  𰰛.txt_value_vendor=𒆶(𰰛,style=ﲔ)
  𰰛.grid.Add(𰰛.txt_label_vendor,0,𐰷|𐳅,10)
  𰰛.grid.Add(𰰛.txt_value_vendor,0,𐲤)
  𰰛.txt_label_model=𒆶(𰰛,style=𫛬,label="Model:")
  𰰛.txt_value_model=𒆶(𰰛,style=ﲔ)
  𰰛.grid.Add(𰰛.txt_label_model,0,𐰷|𐳅,10)
  𰰛.grid.Add(𰰛.txt_value_model,0,𐲤)
  𰰛.txt_label_sn=𒆶(𰰛,style=𫛬,label="Serial number:")
  𰰛.txt_value_sn=𒆶(𰰛,style=ﲔ)
  𰰛.grid.Add(𰰛.txt_label_sn,0,𐰷|𐳅,10)
  𰰛.grid.Add(𰰛.txt_value_sn,0,𐲤)
  𰰛.txt_label_dev_version=𒆶(𰰛,style=𫛬,label="Device version:")
  𰰛.txt_value_dev_version=𒆶(𰰛,style=ﲔ)
  𰰛.grid.Add(𰰛.txt_label_dev_version,0,𐰷|𐳅,10)
  𰰛.grid.Add(𰰛.txt_value_dev_version,0,𐲤)
 def ﯕ(𰰛,info):
  𰰛.txt_value_vendor.SetLabel(info.vendor)
  𰰛.txt_value_model.SetLabel(info.product_name)
  𰰛.txt_value_sn.SetLabel(info.serial_number)
  𰰛.txt_value_dev_version.SetLabel(info.dev_version)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
