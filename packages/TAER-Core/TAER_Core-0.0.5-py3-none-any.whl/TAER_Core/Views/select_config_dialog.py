import wx
V=super
m=False
G=True
T=str
N=wx.EVT_TEXT
D=wx.RIGHT
b=wx.LEFT
k=wx.CANCEL
u=wx.OK
f=wx.BOTTOM
y=wx.TOP
R=wx.ALIGN_CENTER_HORIZONTAL
X=wx.Size
H=wx.CB_SORT
z=wx.CB_READONLY
l=wx.CB_DROPDOWN
e=wx.CB_SIMPLE
O=wx.ComboBox
A=wx.ALIGN_CENTER_VERTICAL
Q=wx.VERTICAL
q=wx.HORIZONTAL
C=wx.BoxSizer
w=wx.NullColour
p=wx.RESIZE_BORDER
Y=wx.STAY_ON_TOP
F=wx.CAPTION
P=wx.Dialog
import os
c=os.scandir
E=os.path
import sys
import TAER_Add_Ons
L=TAER_Add_Ons.__file__
class W(P):
 x=E.join(E.dirname(L),("chip_configs"))
 def __init__(v,h):
  i=(F|Y)^p
  V().__init__(h,style=i,title="Select chip configuration")
  v.__get_config_filenames()
  v.__create_layout()
  v.CentreOnScreen()
 def __create_layout(v):
  v.SetBackgroundColour(w)
  v.hsizer=C(q)
  v.vsizer=C(Q)
  v.hsizer.Add(v.vsizer,0,A)
  v.combobox_select_config=O(v,choices=v.choices_names,style=e|l|z|H,size=X(-1,25),)
  v.vsizer.Add(v.combobox_select_config,1,R|y|f,20,)
  v.button_sizer=v.CreateStdDialogButtonSizer(u^k)
  v.button_ok=v.FindWindow(v.GetAffirmativeId())
  v.button_ok.Enable(m)
  v.vsizer.Add(v.button_sizer,0,R|f|b|D,20,)
  v.combobox_select_config.Bind(N,lambda evt:evt.GetEventObject().GetParent().button_ok.Enable(G),)
  v.SetSizerAndFit(v.hsizer)
  v.Layout()
 def __get_config_filenames(v):
  v.config_paths={}
  v.choices_names=[]
  for a in c(v.CONFIGS_PATH):
   if a.is_file()and a.name.endswith(".yaml"):
    K=E.splitext(a.name)[0]
    v.config_paths[K]=a
    v.choices_names.append(K)
 def r(v)->T:
  j=v.combobox_select_config.GetSelection()
  K=v.combobox_select_config.GetString(j)
  return v.config_paths[K].path
# Created by pyminifier (https://github.com/liftoff/pyminifier)
