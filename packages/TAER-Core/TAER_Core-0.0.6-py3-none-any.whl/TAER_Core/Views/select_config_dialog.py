import wx
c=super
Q=False
t=True
J=str
e=wx.EVT_TEXT
k=wx.RIGHT
P=wx.LEFT
f=wx.CANCEL
l=wx.OK
A=wx.BOTTOM
x=wx.TOP
R=wx.ALIGN_CENTER_HORIZONTAL
K=wx.Size
I=wx.CB_SORT
q=wx.CB_READONLY
H=wx.CB_DROPDOWN
v=wx.CB_SIMPLE
d=wx.ComboBox
L=wx.ALIGN_CENTER_VERTICAL
X=wx.VERTICAL
n=wx.HORIZONTAL
b=wx.BoxSizer
Y=wx.NullColour
F=wx.RESIZE_BORDER
r=wx.STAY_ON_TOP
m=wx.CAPTION
B=wx.Dialog
import os
u=os.scandir
y=os.path
import sys
import TAER_Add_Ons
V=TAER_Add_Ons.__file__
class a(B):
 M=y.join(y.dirname(V),("chip_configs"))
 def __init__(E,U):
  T=(m|r)^F
  c().__init__(U,style=T,title="Select chip configuration")
  E.__get_config_filenames()
  E.__create_layout()
  E.CentreOnScreen()
 def __create_layout(E):
  E.SetBackgroundColour(Y)
  E.hsizer=b(n)
  E.vsizer=b(X)
  E.hsizer.Add(E.vsizer,0,L)
  E.combobox_select_config=d(E,choices=E.choices_names,style=v|H|q|I,size=K(-1,25),)
  E.vsizer.Add(E.combobox_select_config,1,R|x|A,20,)
  E.button_sizer=E.CreateStdDialogButtonSizer(l^f)
  E.button_ok=E.FindWindow(E.GetAffirmativeId())
  E.button_ok.Enable(Q)
  E.vsizer.Add(E.button_sizer,0,R|A|P|k,20,)
  E.combobox_select_config.Bind(e,lambda evt:evt.GetEventObject().GetParent().button_ok.Enable(t),)
  E.SetSizerAndFit(E.hsizer)
  E.Layout()
 def __get_config_filenames(E):
  E.config_paths={}
  E.choices_names=[]
  for G in u(E.CONFIGS_PATH):
   if G.is_file()and G.name.endswith(".yaml"):
    s=y.splitext(G.name)[0]
    E.config_paths[s]=G
    E.choices_names.append(s)
 def j(E)->J:
  h=E.combobox_select_config.GetSelection()
  s=E.combobox_select_config.GetString(h)
  return E.config_paths[s].path
# Created by pyminifier (https://github.com/liftoff/pyminifier)
