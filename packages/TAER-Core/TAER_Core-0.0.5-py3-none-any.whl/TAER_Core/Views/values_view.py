import wx
B=super
u=False
o=str
q=True
V=wx.LEFT
Y=wx.ALIGN_CENTER_VERTICAL
F=wx.TOP
b=wx.ALIGN_CENTER
k=wx.TE_PROCESS_ENTER
a=wx.TE_CENTRE
e=wx.TextCtrl
s=wx.CENTER
v=wx.StaticText
r=wx.ID_APPLY
f=wx.Button
T=wx.ALIGN_RIGHT
N=wx.ALIGN_CENTER_HORIZONTAL
y=wx.GridSizer
W=wx.Panel
z=wx.EXPAND
C=wx.ALL
D=wx.HORIZONTAL
d=wx.VERTICAL
A=wx.BoxSizer
J=wx.NullColour
O=wx.Size
E=wx.MAXIMIZE_BOX
S=wx.RESIZE_BORDER
w=wx.DEFAULT_FRAME_STYLE
L=wx.NewId
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class j(AuxViewBase):
 def __init__(M,l,title):
  B().__init__(parent=l,id=L(),title=title,style=w^S^E,)
  M.SetMinSize(O(0,0))
  M.__create_layout()
 def __create_layout(M):
  M.SetBackgroundColour(J)
  M.vsizer=A(d)
  M.hsizer=A(D)
  M.vsizer.Add(M.hsizer,0,C,5)
  M.panel_values=G(M)
  M.hsizer.Add(M.panel_values,0,z)
  M.SetSizerAndFit(M.vsizer)
  M.Layout()
 def h(M,values):
  M.panel_values.update_values(values)
  M.Fit()
 def I(M):
  M.panel_values.to_default_color()
 def K(M,state):
  M.panel_values.Enable(state)
class G(W):
 def __init__(M,l):
  W.__init__(M,l)
  M.__create_layout()
  M.values_widgets={}
  M.init_flag=u
 def __create_layout(M):
  M.SetBackgroundColour(J)
  M.hbox=A(D)
  M.vbox=A(d)
  M.hbox.Add(M.vbox,0,C,1)
  M.grid_register=y(2,0,0)
  M.vbox.Add(M.grid_register,0,N|C,5)
  M.sizer_buttons=A(D)
  M.vbox.Add(M.sizer_buttons,0,T|C,5)
  M.button_apply=f(M,r,"Apply")
  M.sizer_buttons.Add(M.button_apply,0,C,5)
  M.SetSizer(M.hbox)
  M.Layout()
 def __init_values(M,values):
  for g in values.values():
   X=v(M,label=g.label,style=s)
   t1=e(M,value=o(g.value),style=a|k)
   M.values_widgets[g.label]=t1
   M.grid_register.Add(X,0,b|F,5)
   M.grid_register.Add(t1,0,Y|T|V|F,5)
 def h(M,values):
  if M.init_flag:
   for R in values.values():
    M.values_widgets[R.label].SetValue(o(R.value))
  else:
   M.__init_values(values)
   M.init_flag=q
  M.p()
 def Q(M,n):
  n.SetBackgroundColour((128,255,0,50))
 def p(M):
  [n.SetBackgroundColour(J)for n in M.values_widgets.values()]
  M.Refresh()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
