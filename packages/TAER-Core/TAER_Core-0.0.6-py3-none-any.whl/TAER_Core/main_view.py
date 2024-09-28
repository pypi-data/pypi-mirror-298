import sys
lj=None
lt=sorted
lo=str
lV=True
lX=False
ls=property
lF=format
import os
DI=os.getcwd
Dm=os.path
from importlib.metadata import version
import wx
ld=wx.Image
lJ=wx.Colour
lD=wx.TextAttr
Dp=wx.CallAfter
DC=wx.NORMAL
Dv=wx.MODERN
DR=wx.Font
DP=wx.TextCtrl
Dg=wx.TE_NOHIDESEL
Dy=wx.TE_WORDWRAP
Dc=wx.TE_RICH
Df=wx.TE_READONLY
DS=wx.TE_MULTILINE
Dq=wx.ALIGN_CENTER_HORIZONTAL
Dz=wx.ALIGN_CENTER_VERTICAL
Di=wx.SHAPED
DL=wx.NOT_FOUND
DK=wx.Button
DG=wx.RIGHT
DM=wx.LEFT
DY=wx.BOTTOM
DH=wx.GridSizer
Da=wx.StaticBoxSizer
Dn=wx.ALL
DE=wx.RA_VERTICAL
Dh=wx.RadioBox
Dk=wx.Panel
DA=wx.ImageFromBuffer
DU=wx.EXPAND
DF=wx.HORIZONTAL
Ds=wx.VERTICAL
DX=wx.BoxSizer
DV=wx.NullColour
Do=wx.Size
Dt=wx.App
Dj=wx.Frame
import threading
le=threading.Lock
import re
lQ=re.IGNORECASE
lB=re.MULTILINE
lx=re.compile
import logging
lb=logging.LogRecord
lr=logging.Formatter
lu=logging.getLogger
import cv2 as cv
lT=cv.COLOR_BGR2RGB
lO=cv.cvtColor
from lW import(ValuesView,DeviceInfoView,HistogramView,SerialView,ChipRegisterView,AdcView,BufferedCanvas,MainMenuBar,)
lw=BufferedCanvas.__init__
from logging import StreamHandler
lN=StreamHandler.__init__
import TAER_Core
lm=TAER_Core.Libs
lW=TAER_Core.Views
from lm.config import ViewConfig
import TAER_Add_Ons
lI=TAER_Add_Ons.__file__
class Db(Dj):
 def __init__(D):
  D.app=Dt()
  l=D.__get_current_version()
  Dj.__init__(D,lj,title=f"pyAER {tag}")
 def P(D):
  D.config_data=d()
  D.SetMinSize(Do(D.config_data.main_panel_size.w,D.config_data.main_panel_size.h))
  D.__create_layout()
  D.__init_logic()
 def __create_layout(D):
  D.SetBackgroundColour(DV)
  D.menu_bar=e(D)
  D.SetMenuBar(D.menu_bar)
  D.main_box=DX(Ds)
  D.hbox=DX(DF)
  D.panel_control=x(D)
  D.panel_image=B(D)
  D.logging_panel=Q(D)
  D.hbox.Add(D.panel_control,1,DU)
  D.hbox.Add(D.panel_image,3,DU)
  D.main_box.Add(D.hbox,2,DU)
  D.main_box.Add(D.logging_panel,1,DU)
  D.SetSize(Do(D.config_data.main_panel_size.w,D.config_data.main_panel_size.h))
  D.SetSizer(D.main_box)
  D.Layout()
  D.__init_other_frames()
 def __init_other_frames(D):
  D.edit_register_device_frame=u(D,"Registers")
  D.edit_register_chip_frame=r(D)
  D.edit_dac_frame=u(D,"DACs")
  D.device_info_frame=b(D)
  D.image_histogram_frame=O(D)
  D.serial_control_frame=T(D)
  D.adc_control_frame=w(D)
 def __init_logic(D):
  D.imgLock=le()
 def __write_version_file(D,filepath):
  N=git.Repo(Dm.dirname(__file__))
  W=lt(N.tags,key=lambda t:t.commit.committed_datetime)
  l=lo(W[-1])+"\n"
  with v(filepath,"w")as f:
   f.write(l)
 def __read_version_file(D,filepath):
  l=""
  with v(filepath,"r")as f:
   l=f.readline()
  return l
 def __get_current_version(D):
  return version("TAER_Core")
 def R(D):
  D.app.MainLoop()
 def v(D):
  D.Layout()
  D.CenterOnScreen()
  D.Show()
 def C(D,destroy=lV):
  if destroy:
   D.Destroy()
  else:
   D.Hide()
 def p(D):
  m=D.__get_logger_keys()
  I=DN(D.logging_panel.logging_box)
  for j in m:
   t=lu(j)
   t.addHandler(I)
 def __get_logger_keys(D):
  o=Dm.join(DI(),"config","loggers.conf")
  if Dm.exists(o):
   V=o
  else:
   V=Dm.join(Dm.dirname(lI),"config","loggers.conf")
  with v(V,"r")as f:
   X=f.read()
   s=r"(?<=keys=)(.*)"
   F=lx(s,lB|lQ)
   U=F.search(X)
   return U.groups()[0].split(",")
 def Dl(D,state):
  for A in D.menu_bar.menu_device.GetMenuItems():
   A.Enable(state)
  for A in D.menu_bar.menu_edit.GetMenuItems():
   A.Enable(state)
  for A in D.menu_bar.menu_tools.GetMenuItems():
   A.Enable(state)
  D.panel_control.Enable(state)
  D.edit_register_device_frame.set_menus_state(state)
 def DJ(D,state):
  k=D.panel_control
  if state:
   k.button_start_stop.SetLabel("Start")
   k.button_capture.Enable(lV)
  else:
   k.button_start_stop.SetLabel("Stop")
   k.button_capture.Enable(lX)
 def Dd(D,mode):
  D.panel_control.set_selected_mode(mode)
 @ls
 def De(D):
  with D.imgLock:
   return D.panel_image.img_ctrl.img
 @De.setter
 def De(D,value):
  with D.imgLock:
   h,w=value.shape[:2] 
   h=lO(value,lT)
   D.panel_image.img_ctrl.img=DA(w,h,h)
  D.panel_image.img_ctrl.update()
class x(Dk):
 def __init__(D,E):
  Dk.__init__(D,E)
  D.parent=E
  D.__create_layout()
 def __create_layout(D):
  D.SetBackgroundColour(DV)
  n=D.parent.config_data.control_panel.modes
  a=[mode[0]for mode in n]
  D.vbox=DX(Ds)
  D.modes_box=Dh(D,label="Select mode:",choices=a,style=DE,)
  D.vbox.Add(D.modes_box,0,DU|Dn,20)
  D.control_box=Da(DF,D,"Sensor Control")
  D.control_grid=DH(2,0,0)
  D.control_box.Add(D.control_grid,0,Dn,5)
  D.Dx()
  D.vbox.Add(D.control_box,0,DU|DY|DM|DG,20)
  D.SetSizerAndFit(D.vbox)
  D.Layout()
 def Dx(D):
  Y=D.control_grid
  M=DK(D,label="Start")
  Y.Add(M,0,Dn,5)
  D.button_start_stop=M
  M=DK(D,label="Capture")
  Y.Add(M,0,Dn,5)
  D.button_capture=M
  M=DK(D,label="Reset device")
  Y.Add(M,0,Dn,5)
  D.button_reset=M
  M=DK(D,label="Reset AER")
  Y.Add(M,0,Dn,5)
  D.button_reset_periphery=M
  M=DK(D,label="Reset Chip")
  Y.Add(M,0,Dn,5)
  D.button_reset_chip=M
 def DB(D,mode):
  n=D.modes_box.FindString(mode)
  if n is not DL:
   D.modes_box.SetSelection(n)
class B(Dk):
 def __init__(D,E):
  Dk.__init__(D,E)
  D.parent=E
  D.__create_layout()
 def __create_layout(D):
  D.SetBackgroundColour(DV)
  D.img_ctrl=G(D)
  D.vsizer=DX(Ds)
  D.hsizer=DX(DF)
  D.hsizer.Add(D.img_ctrl,1,Di|Dz|Dn,10)
  D.vsizer.Add(D.hsizer,1,Di|Dq|Dn,10)
  D.SetSizer(D.vsizer)
  D.Layout()
class Q(Dk):
 def __init__(D,E):
  Dk.__init__(D,E)
  D.SetMinSize(Do(100,200))
  D.__create_layout()
 def __create_layout(D):
  D.SetBackgroundColour(DV)
  D.sizer=DX()
  K=DS|Df|Dc|Dy|Dg
  D.logging_box=DP(D,style=K)
  i=DR(10,Dv,DC,DC,lX,"Consolas")
  D.logging_box.SetFont(i)
  D.logging_box.SetMinSize(Do(100,20))
  D.sizer.Add(D.logging_box,1,DU|Dn,10)
  D.SetSizer(D.sizer)
class DN(StreamHandler):
 def __init__(D,z:DP):
  lN(D)
  D.txt_control=z
  D.__config()
 def __config(D):
  q="[%(asctime)s.%(msecs)03d] %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
  lF=lr(q,datefmt="%H:%M:%S")
  D.setFormatter(lF)
  S=D.txt_control.GetDefaultStyle().TextColour
  D.color_default=S
 def DQ(D,record:lb):
  Dp(D.Du,record)
 def Du(D,record:lb):
  f=D.lF(record)
  L=D.__get_text_style(record.levelname)
  D.txt_control.SetDefaultStyle(L)
  D.txt_control.AppendText(f+"\n")
  D.flush()
 def __get_text_style(D,x:lo)->lD:
  return{"DEBUG":lD(D.color_default),"INFO":lD(lJ(82,190,128)),"WARNING":lD(lJ(244,208,63)),"ERROR":lD(lJ(236,112,99)),"CRITICAL":lD(lJ(176,58,46)),}[x]
class G(BufferedCanvas):
 def __init__(D,E):
  D.parent=E
  D.__create_layout()
 def __create_layout(D):
  c=D.parent.GetParent().config_data.image_panel_size
  D.img=ld(c.w,c.h)
  y=Do(c.w,c.h)
  lw(D,D.parent,size=y)
  D.Fit()
 def Dr(D,dc):
  W,H=D.GetClientSize()
  if W>0 and H>0:
   D.bitmap=D.img.Scale(W,H).ConvertToBitmap()
   dc.DrawBitmap(D.bitmap,0,0)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
