import wx
仒=super
𢹜=False
댵=str
鳖=True
𞡛=wx.LEFT
鱧=wx.ALIGN_CENTER_VERTICAL
𐲢=wx.TOP
𡝁=wx.ALIGN_CENTER
ﱇ=wx.TE_PROCESS_ENTER
ﰧ=wx.TE_CENTRE
𐡊=wx.TextCtrl
𐬚=wx.CENTER
ࠆ=wx.StaticText
𭄏=wx.ID_APPLY
萄=wx.Button
ߓ=wx.ALIGN_RIGHT
𐠥=wx.ALIGN_CENTER_HORIZONTAL
𤀮=wx.GridSizer
𭽽=wx.Panel
弾=wx.EXPAND
𐡊=wx.ALL
𐣬=wx.HORIZONTAL
𐢆=wx.VERTICAL
𐭨=wx.BoxSizer
胚=wx.NullColour
𒂆=wx.Size
𢫃=wx.MAXIMIZE_BOX
𞡀=wx.RESIZE_BORDER
𐬒=wx.DEFAULT_FRAME_STYLE
𑜀=wx.NewId
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class ﴎ(AuxViewBase):
 def __init__(𥑮,𐤪,title):
  仒().__init__(parent=𐤪,id=𑜀(),title=title,style=𐬒^𞡀^𢫃,)
  𥑮.SetMinSize(𒂆(0,0))
  𥑮.__create_layout()
 def __create_layout(𥑮):
  𥑮.SetBackgroundColour(胚)
  𥑮.vsizer=𐭨(𐢆)
  𥑮.hsizer=𐭨(𐣬)
  𥑮.vsizer.Add(𥑮.hsizer,0,𐡊,5)
  𥑮.panel_values=ھ(𥑮)
  𥑮.hsizer.Add(𥑮.panel_values,0,弾)
  𥑮.SetSizerAndFit(𥑮.vsizer)
  𥑮.Layout()
 def ﴔ(𥑮,values):
  𥑮.panel_values.update_values(values)
  𥑮.Fit()
 def 𬖗(𥑮):
  𥑮.panel_values.to_default_color()
 def 뵴(𥑮,state):
  𥑮.panel_values.Enable(state)
class ھ(𭽽):
 def __init__(𥑮,𐤪):
  𭽽.__init__(𥑮,𐤪)
  𥑮.__create_layout()
  𥑮.values_widgets={}
  𥑮.init_flag=𢹜
 def __create_layout(𥑮):
  𥑮.SetBackgroundColour(胚)
  𥑮.hbox=𐭨(𐣬)
  𥑮.vbox=𐭨(𐢆)
  𥑮.hbox.Add(𥑮.vbox,0,𐡊,1)
  𥑮.grid_register=𤀮(2,0,0)
  𥑮.vbox.Add(𥑮.grid_register,0,𐠥|𐡊,5)
  𥑮.sizer_buttons=𐭨(𐣬)
  𥑮.vbox.Add(𥑮.sizer_buttons,0,ߓ|𐡊,5)
  𥑮.button_apply=萄(𥑮,𭄏,"Apply")
  𥑮.sizer_buttons.Add(𥑮.button_apply,0,𐡊,5)
  𥑮.SetSizer(𥑮.hbox)
  𥑮.Layout()
 def __init_values(𥑮,values):
  for צּ in values.values():
   𞢠=ࠆ(𥑮,label=צּ.label,style=𐬚)
   𐡰=𐡊(𥑮,value=댵(צּ.value),style=ﰧ|ﱇ)
   𥑮.values_widgets[צּ.label]=𐡰
   𥑮.grid_register.Add(𞢠,0,𡝁|𐲢,5)
   𥑮.grid_register.Add(𐡰,0,鱧|ߓ|𞡛|𐲢,5)
 def ﴔ(𥑮,values):
  if 𥑮.init_flag:
   for ﹳ in values.values():
    𥑮.values_widgets[ﹳ.label].SetValue(댵(ﹳ.value))
  else:
   𥑮.__init_values(values)
   𥑮.init_flag=鳖
  𥑮.掯()
 def 𮇹(𥑮,ﻴ):
  ﻴ.SetBackgroundColour((128,255,0,50))
 def 掯(𥑮):
  [ﻴ.SetBackgroundColour(胚)for ﻴ in 𥑮.values_widgets.values()]
  𥑮.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
