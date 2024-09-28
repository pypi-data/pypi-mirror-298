import wx
ࣆ=super
𤏡=False
䱟=True
𐩯=str
𞹏=wx.EVT_TEXT
ﬠ=wx.RIGHT
𐡬=wx.LEFT
ߔ=wx.CANCEL
𭙝=wx.OK
ﲉ=wx.BOTTOM
𐳣=wx.TOP
𰻾=wx.ALIGN_CENTER_HORIZONTAL
𞡨=wx.Size
儿=wx.CB_SORT
ﵐ=wx.CB_READONLY
峗=wx.CB_DROPDOWN
𐭊=wx.CB_SIMPLE
ﲪ=wx.ComboBox
𐦏=wx.ALIGN_CENTER_VERTICAL
𐿬=wx.VERTICAL
𧼇=wx.HORIZONTAL
𛈥=wx.BoxSizer
𐿦=wx.NullColour
鍇=wx.RESIZE_BORDER
𐩰=wx.STAY_ON_TOP
𞺁=wx.CAPTION
𨿶=wx.Dialog
import os
ﭽ=os.scandir
𥸑=os.path
import sys
import TAER_Add_Ons
𐴚=TAER_Add_Ons.__file__
class 𞢰(𨿶):
 ﺵ=𥸑.join(𥸑.dirname(𐴚),("chip_configs"))
 def __init__(𨈾,봦):
  𘚏=(𞺁|𐩰)^鍇
  ࣆ().__init__(봦,style=𘚏,title="Select chip configuration")
  𨈾.__get_config_filenames()
  𨈾.__create_layout()
  𨈾.CentreOnScreen()
 def __create_layout(𨈾):
  𨈾.SetBackgroundColour(𐿦)
  𨈾.hsizer=𛈥(𧼇)
  𨈾.vsizer=𛈥(𐿬)
  𨈾.hsizer.Add(𨈾.vsizer,0,𐦏)
  𨈾.combobox_select_config=ﲪ(𨈾,choices=𨈾.choices_names,style=𐭊|峗|ﵐ|儿,size=𞡨(-1,25),)
  𨈾.vsizer.Add(𨈾.combobox_select_config,1,𰻾|𐳣|ﲉ,20,)
  𨈾.button_sizer=𨈾.CreateStdDialogButtonSizer(𭙝^ߔ)
  𨈾.button_ok=𨈾.FindWindow(𨈾.GetAffirmativeId())
  𨈾.button_ok.Enable(𤏡)
  𨈾.vsizer.Add(𨈾.button_sizer,0,𰻾|ﲉ|𐡬|ﬠ,20,)
  𨈾.combobox_select_config.Bind(𞹏,lambda evt:evt.GetEventObject().GetParent().button_ok.Enable(䱟),)
  𨈾.SetSizerAndFit(𨈾.hsizer)
  𨈾.Layout()
 def __get_config_filenames(𨈾):
  𨈾.config_paths={}
  𨈾.choices_names=[]
  for 鴊 in ﭽ(𨈾.CONFIGS_PATH):
   if 鴊.is_file()and 鴊.name.endswith(".yaml"):
    䕫=𥸑.splitext(鴊.name)[0]
    𨈾.config_paths[䕫]=鴊
    𨈾.choices_names.append(䕫)
 def 𓏆(𨈾)->𐩯:
  䦃=𨈾.combobox_select_config.GetSelection()
  䕫=𨈾.combobox_select_config.GetString(䦃)
  return 𨈾.config_paths[䕫].path
# Created by pyminifier (https://github.com/liftoff/pyminifier)
