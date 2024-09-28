import wx
J=super
E=False
u=True
M=str
import os
import sys
import TAER_Add_Ons
class I(wx.Dialog):
 O=os.path.join(os.path.dirname(TAER_Add_Ons.__file__),("chip_configs"))
 def __init__(m,j):
  a=(wx.CAPTION|wx.STAY_ON_TOP)^wx.RESIZE_BORDER
  J().__init__(j,style=a,title="Select chip configuration")
  m.__get_config_filenames()
  m.__create_layout()
  m.CentreOnScreen()
 def __create_layout(m):
  m.SetBackgroundColour(wx.NullColour)
  m.hsizer=wx.BoxSizer(wx.HORIZONTAL)
  m.vsizer=wx.BoxSizer(wx.VERTICAL)
  m.hsizer.Add(m.vsizer,0,wx.ALIGN_CENTER_VERTICAL)
  m.combobox_select_config=wx.ComboBox(m,choices=m.choices_names,style=wx.CB_SIMPLE|wx.CB_DROPDOWN|wx.CB_READONLY|wx.CB_SORT,size=wx.Size(-1,25),)
  m.vsizer.Add(m.combobox_select_config,1,wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.BOTTOM,20,)
  m.button_sizer=m.CreateStdDialogButtonSizer(wx.OK^wx.CANCEL)
  m.button_ok=m.FindWindow(m.GetAffirmativeId())
  m.button_ok.Enable(E)
  m.vsizer.Add(m.button_sizer,0,wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM|wx.LEFT|wx.RIGHT,20,)
  m.combobox_select_config.Bind(wx.EVT_TEXT,lambda evt:evt.GetEventObject().GetParent().button_ok.Enable(u),)
  m.SetSizerAndFit(m.hsizer)
  m.Layout()
 def __get_config_filenames(m):
  m.config_paths={}
  m.choices_names=[]
  for V in os.scandir(m.CONFIGS_PATH):
   if V.is_file()and V.name.endswith(".yaml"):
    L=os.path.splitext(V.name)[0]
    m.config_paths[L]=V
    m.choices_names.append(L)
 def F(m)->M:
  i=m.combobox_select_config.GetSelection()
  L=m.combobox_select_config.GetString(i)
  return m.config_paths[L].path
# Created by pyminifier (https://github.com/liftoff/pyminifier)
