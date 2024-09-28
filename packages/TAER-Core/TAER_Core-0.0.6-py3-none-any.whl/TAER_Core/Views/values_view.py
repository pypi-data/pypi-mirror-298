import wx
x=super
s=False
I=str
D=True
e=wx.LEFT
Q=wx.ALIGN_CENTER_VERTICAL
P=wx.TOP
m=wx.ALIGN_CENTER
u=wx.TE_PROCESS_ENTER
V=wx.TE_CENTRE
z=wx.TextCtrl
S=wx.CENTER
o=wx.StaticText
Y=wx.ID_APPLY
J=wx.Button
j=wx.ALIGN_RIGHT
f=wx.ALIGN_CENTER_HORIZONTAL
W=wx.GridSizer
l=wx.Panel
M=wx.EXPAND
B=wx.ALL
n=wx.HORIZONTAL
h=wx.VERTICAL
U=wx.BoxSizer
b=wx.NullColour
E=wx.Size
w=wx.MAXIMIZE_BOX
i=wx.RESIZE_BORDER
q=wx.DEFAULT_FRAME_STYLE
F=wx.NewId
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class d(AuxViewBase):
 def __init__(R,p,title):
  x().__init__(parent=p,id=F(),title=title,style=q^i^w,)
  R.SetMinSize(E(0,0))
  R.__create_layout()
 def __create_layout(R):
  R.SetBackgroundColour(b)
  R.vsizer=U(h)
  R.hsizer=U(n)
  R.vsizer.Add(R.hsizer,0,B,5)
  R.panel_values=H(R)
  R.hsizer.Add(R.panel_values,0,M)
  R.SetSizerAndFit(R.vsizer)
  R.Layout()
 def O(R,values):
  R.panel_values.update_values(values)
  R.Fit()
 def t(R):
  R.panel_values.to_default_color()
 def C(R,state):
  R.panel_values.Enable(state)
class H(l):
 def __init__(R,p):
  l.__init__(R,p)
  R.__create_layout()
  R.values_widgets={}
  R.init_flag=s
 def __create_layout(R):
  R.SetBackgroundColour(b)
  R.hbox=U(n)
  R.vbox=U(h)
  R.hbox.Add(R.vbox,0,B,1)
  R.grid_register=W(2,0,0)
  R.vbox.Add(R.grid_register,0,f|B,5)
  R.sizer_buttons=U(n)
  R.vbox.Add(R.sizer_buttons,0,j|B,5)
  R.button_apply=J(R,Y,"Apply")
  R.sizer_buttons.Add(R.button_apply,0,B,5)
  R.SetSizer(R.hbox)
  R.Layout()
 def __init_values(R,values):
  for G in values.values():
   N=o(R,label=G.label,style=S)
   t1=z(R,value=I(G.value),style=V|u)
   R.values_widgets[G.label]=t1
   R.grid_register.Add(N,0,m|P,5)
   R.grid_register.Add(t1,0,Q|j|e|P,5)
 def O(R,values):
  if R.init_flag:
   for k in values.values():
    R.values_widgets[k.label].SetValue(I(k.value))
  else:
   R.__init_values(values)
   R.init_flag=D
  R.c()
 def K(R,y):
  y.SetBackgroundColour((128,255,0,50))
 def c(R):
  [y.SetBackgroundColour(b)for y in R.values_widgets.values()]
  R.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
