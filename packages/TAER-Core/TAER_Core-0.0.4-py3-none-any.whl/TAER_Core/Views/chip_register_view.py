import wx
㫍=super
ڇ=True
𨻫=False
𤵄=hasattr
赈=pow
𠣵=wx.TE_PROCESS_ENTER
ﱻ=wx.TE_CENTRE
𘄤=wx.CheckBox
𞹛=wx.ALIGN_CENTRE_VERTICAL
召=wx.LEFT
𞸻=wx.CENTER
㦧=wx.StaticText
臘=wx.BOTH
ݙ=wx.FlexGridSizer
𥓟=wx.StaticBoxSizer
ࡡ=wx.ID_APPLY
𐢁=wx.Button
ꊂ=wx.ALIGN_RIGHT
𐭕=wx.ALL
뱀=wx.EXPAND
𫰁=wx.VERTICAL
𗃹=wx.HORIZONTAL
ﶜ=wx.BoxSizer
𪠘=wx.NullColour
𞢶=wx.MAXIMIZE_BOX
𐰆=wx.DEFAULT_FRAME_STYLE
𞠋=wx.NewId
𐐣=wx.lib
import 𐐣.scrolledpanel
import 𐐣.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class 𞤄(AuxViewBase):
 def __init__(䭏,ࣀ):
  㫍().__init__(parent=ࣀ,id=𞠋(),title="Chip registers",style=𐰆^𞢶,)
  䭏.SetMaxClientSize((600,800))
  䭏.__create_layout()
 def __create_layout(䭏):
  䭏.SetBackgroundColour(𪠘)
  䭏.hsizer=ﶜ(𗃹)
  䭏.vsizer=ﶜ(𫰁)
  䭏.hsizer.Add(䭏.vsizer,1,뱀|𐭕,5)
  䭏.panel_values=𰫭(䭏)
  䭏.vsizer.Add(䭏.panel_values,1,뱀|𐭕)
  䭏.sizer_buttons=ﶜ(𗃹)
  䭏.vsizer.Add(䭏.sizer_buttons,0,ꊂ|𐭕,5)
  䭏.button_apply=𐢁(䭏,ࡡ,"Apply")
  䭏.sizer_buttons.Add(䭏.button_apply,0,𐭕,10)
  䭏.SetAutoLayout(ڇ)
  䭏.SetSizerAndFit(䭏.hsizer)
  䭏.Layout()
 def 𦃅(䭏,values):
  䭏.panel_values.update_values(values)
  䭏.Fit()
class 𰫭(𐐣.scrolledpanel.ScrolledPanel):
 def __init__(䭏,*args,**kw):
  㫍().__init__(*args,**kw)
  䭏.SetMinClientSize((400,400))
  䭏.SetMaxClientSize((600,1000))
  䭏.SetAutoLayout(ڇ)
  䭏.SetupScrolling()
  䭏.__create_layout()
  䭏.init_flag=𨻫
  䭏.values_widgets={}
 def __create_layout(䭏):
  䭏.SetBackgroundColour(𪠘)
  䭏.hbox=ﶜ(𗃹)
  䭏.vbox=ﶜ(𫰁)
  䭏.hbox.Add(䭏.vbox,1,뱀|𐭕,1)
  䭏.SetSizer(䭏.hbox)
  䭏.Layout()
 def __init_values(䭏,values):
  for ﶋ in values.values():
   ﻯ=𥓟(𗃹,䭏,ﶋ.label)
   䄝=ݙ(cols=2,vgap=3,hgap=10)
   䄝.SetFlexibleDirection(臘)
   ﻯ.Add(䄝,1,𐭕|뱀,5)
   if 𤵄(ﶋ,"signals"):
    for 헁 in ﶋ.signals.values():
     𮧼=㦧(䭏,label=헁.label,style=𞸻)
     䄝.Add(𮧼,1,𐭕|뱀|召|𞹛,5,)
     if 헁.nbits==1:
      𐳙=𘄤(䭏)
      䄝.Add(𐳙,1,𐭕|召|𞹛,2)
     else:
      𞺘=赈(2,헁.nbits)-1
      𐳙=wxInt.IntCtrl(䭏,style=ﱻ|𠣵,min=0,max=𞺘,limited=ڇ,)
      䄝.Add(𐳙,1,𐭕|뱀|𞹛,1)
     䭏.values_widgets[헁.label]=𐳙
   else:
    𮧼=㦧(䭏,label="Value",style=𞸻)
    䄝.Add(𮧼,1,𐭕|뱀|召|𞹛,5)
    𞺘=赈(2,8)-1
    𐳙=wxInt.IntCtrl(䭏,style=ﱻ|𠣵,min=0,max=𞺘,limited=ڇ,)
    䄝.Add(𐳙,1,𐭕|뱀|𞹛,1)
    䭏.values_widgets[ﶋ.label]=𐳙
   䭏.vbox.Add(ﻯ,0,뱀|𐭕,5)
  䭏.Fit()
 def 𦃅(䭏,values):
  if 䭏.init_flag:
   for _,ﶋ in values.items():
    for _,헁 in ﶋ.signals.items():
     𦦨=ﶋ.get_signal(헁.label)
     䭏.values_widgets[헁.label].SetValue(𦦨)
  else:
   䭏.__init_values(values)
   䭏.init_flag=ڇ
  䭏.ﳖ()
 def 帰(䭏,𰞻):
  𰞻.SetBackgroundColour((128,255,0,50))
 def ﳖ(䭏):
  [𰞻.SetBackgroundColour(𪠘)for 𰞻 in 䭏.values_widgets.values()]
  䭏.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
