import wx
d=super
R=True
t=False
v=hasattr
r=pow
O=wx.TE_PROCESS_ENTER
Y=wx.TE_CENTRE
A=wx.CheckBox
J=wx.ALIGN_CENTRE_VERTICAL
p=wx.LEFT
F=wx.CENTER
G=wx.StaticText
y=wx.BOTH
N=wx.FlexGridSizer
P=wx.StaticBoxSizer
l=wx.ID_APPLY
a=wx.Button
j=wx.ALIGN_RIGHT
x=wx.ALL
K=wx.EXPAND
M=wx.VERTICAL
D=wx.HORIZONTAL
q=wx.BoxSizer
e=wx.NullColour
m=wx.MAXIMIZE_BOX
h=wx.DEFAULT_FRAME_STYLE
b=wx.NewId
o=wx.lib
import o.scrolledpanel
import o.intctrl as wxInt
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class z(AuxViewBase):
 def __init__(X,c):
  d().__init__(parent=c,id=b(),title="Chip registers",style=h^m,)
  X.SetMaxClientSize((600,800))
  X.__create_layout()
 def __create_layout(X):
  X.SetBackgroundColour(e)
  X.hsizer=q(D)
  X.vsizer=q(M)
  X.hsizer.Add(X.vsizer,1,K|x,5)
  X.panel_values=s(X)
  X.vsizer.Add(X.panel_values,1,K|x)
  X.sizer_buttons=q(D)
  X.vsizer.Add(X.sizer_buttons,0,j|x,5)
  X.button_apply=a(X,l,"Apply")
  X.sizer_buttons.Add(X.button_apply,0,x,10)
  X.SetAutoLayout(R)
  X.SetSizerAndFit(X.hsizer)
  X.Layout()
 def I(X,values):
  X.panel_values.update_values(values)
  X.Fit()
class s(o.scrolledpanel.ScrolledPanel):
 def __init__(X,*args,**kw):
  d().__init__(*args,**kw)
  X.SetMinClientSize((400,400))
  X.SetMaxClientSize((600,1000))
  X.SetAutoLayout(R)
  X.SetupScrolling()
  X.__create_layout()
  X.init_flag=t
  X.values_widgets={}
 def __create_layout(X):
  X.SetBackgroundColour(e)
  X.hbox=q(D)
  X.vbox=q(M)
  X.hbox.Add(X.vbox,1,K|x,1)
  X.SetSizer(X.hbox)
  X.Layout()
 def __init_values(X,values):
  for S in values.values():
   f=P(D,X,S.label)
   E=N(cols=2,vgap=3,hgap=10)
   E.SetFlexibleDirection(y)
   f.Add(E,1,x|K,5)
   if v(S,"signals"):
    for B in S.signals.values():
     V=G(X,label=B.label,style=F)
     E.Add(V,1,x|K|p|J,5,)
     if B.nbits==1:
      t1=A(X)
      E.Add(t1,1,x|p|J,2)
     else:
      i=r(2,B.nbits)-1
      t1=wxInt.IntCtrl(X,style=Y|O,min=0,max=i,limited=R,)
      E.Add(t1,1,x|K|J,1)
     X.values_widgets[B.label]=t1
   else:
    V=G(X,label="Value",style=F)
    E.Add(V,1,x|K|p|J,5)
    i=r(2,8)-1
    t1=wxInt.IntCtrl(X,style=Y|O,min=0,max=i,limited=R,)
    E.Add(t1,1,x|K|J,1)
    X.values_widgets[S.label]=t1
   X.vbox.Add(f,0,K|x,5)
  X.Fit()
 def I(X,values):
  if X.init_flag:
   for _,S in values.items():
    for _,B in S.signals.items():
     T=S.get_signal(B.label)
     X.values_widgets[B.label].SetValue(T)
  else:
   X.__init_values(values)
   X.init_flag=R
  X.n()
 def u(X,H):
  H.SetBackgroundColour((128,255,0,50))
 def n(X):
  [H.SetBackgroundColour(e)for H in X.values_widgets.values()]
  X.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
