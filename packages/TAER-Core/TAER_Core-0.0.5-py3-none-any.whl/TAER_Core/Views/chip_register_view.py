import wx
n=super
b=True
g=False
M=hasattr
u=pow
U=wx.TE_PROCESS_ENTER
l=wx.TE_CENTRE
R=wx.CheckBox
m=wx.ALIGN_CENTRE_VERTICAL
z=wx.LEFT
L=wx.CENTER
s=wx.StaticText
i=wx.BOTH
N=wx.FlexGridSizer
O=wx.StaticBoxSizer
r=wx.ID_APPLY
d=wx.Button
S=wx.ALIGN_RIGHT
K=wx.ALL
w=wx.EXPAND
p=wx.VERTICAL
v=wx.HORIZONTAL
P=wx.BoxSizer
G=wx.NullColour
q=wx.MAXIMIZE_BOX
k=wx.DEFAULT_FRAME_STYLE
o=wx.NewId
a=wx.lib
import a.scrolledpanel
import a.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class j(AuxViewBase):
 def __init__(y,F):
  n().__init__(parent=F,id=o(),title="Chip registers",style=k^q,)
  y.SetMaxClientSize((600,800))
  y.__create_layout()
 def __create_layout(y):
  y.SetBackgroundColour(G)
  y.hsizer=P(v)
  y.vsizer=P(p)
  y.hsizer.Add(y.vsizer,1,w|K,5)
  y.panel_values=e(y)
  y.vsizer.Add(y.panel_values,1,w|K)
  y.sizer_buttons=P(v)
  y.vsizer.Add(y.sizer_buttons,0,S|K,5)
  y.button_apply=d(y,r,"Apply")
  y.sizer_buttons.Add(y.button_apply,0,K,10)
  y.SetAutoLayout(b)
  y.SetSizerAndFit(y.hsizer)
  y.Layout()
 def Y(y,values):
  y.panel_values.update_values(values)
  y.Fit()
class e(a.scrolledpanel.ScrolledPanel):
 def __init__(y,*args,**kw):
  n().__init__(*args,**kw)
  y.SetMinClientSize((400,400))
  y.SetMaxClientSize((600,1000))
  y.SetAutoLayout(b)
  y.SetupScrolling()
  y.__create_layout()
  y.init_flag=g
  y.values_widgets={}
 def __create_layout(y):
  y.SetBackgroundColour(G)
  y.hbox=P(v)
  y.vbox=P(p)
  y.hbox.Add(y.vbox,1,w|K,1)
  y.SetSizer(y.hbox)
  y.Layout()
 def __init_values(y,values):
  for C in values.values():
   t=O(v,y,C.label)
   J=N(cols=2,vgap=3,hgap=10)
   J.SetFlexibleDirection(i)
   t.Add(J,1,K|w,5)
   if M(C,"signals"):
    for H in C.signals.values():
     X=s(y,label=H.label,style=L)
     J.Add(X,1,K|w|z|m,5,)
     if H.nbits==1:
      t1=R(y)
      J.Add(t1,1,K|z|m,2)
     else:
      c=u(2,H.nbits)-1
      t1=wxInt.IntCtrl(y,style=l|U,min=0,max=c,limited=b,)
      J.Add(t1,1,K|w|m,1)
     y.values_widgets[H.label]=t1
   else:
    X=s(y,label="Value",style=L)
    J.Add(X,1,K|w|z|m,5)
    c=u(2,8)-1
    t1=wxInt.IntCtrl(y,style=l|U,min=0,max=c,limited=b,)
    J.Add(t1,1,K|w|m,1)
    y.values_widgets[C.label]=t1
   y.vbox.Add(t,0,w|K,5)
  y.Fit()
 def Y(y,values):
  if y.init_flag:
   for _,C in values.items():
    for _,H in C.signals.items():
     E=C.get_signal(H.label)
     y.values_widgets[H.label].SetValue(E)
  else:
   y.__init_values(values)
   y.init_flag=b
  y.f()
 def T(y,B):
  B.SetBackgroundColour((128,255,0,50))
 def f(y):
  [B.SetBackgroundColour(G)for B in y.values_widgets.values()]
  y.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
