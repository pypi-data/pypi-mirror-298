import sys
戼=None
䋂=sorted
裔=str
랞=True
ڮ=False
𐀤=property
𬡎=format
import os
𤘸=os.getcwd
𩙇=os.path
from importlib.metadata import version
import wx
ﵝ=wx.Image
𐺡=wx.Colour
ﺎ=wx.TextAttr
𐭀=wx.CallAfter
ﰫ=wx.NORMAL
ﻇ=wx.MODERN
庾=wx.Font
𐣱=wx.TextCtrl
𐠂=wx.TE_NOHIDESEL
𰤋=wx.TE_WORDWRAP
𪰼=wx.TE_RICH
ﻭ=wx.TE_READONLY
𐳣=wx.TE_MULTILINE
𐪐=wx.ALIGN_CENTER_HORIZONTAL
𥢩=wx.ALIGN_CENTER_VERTICAL
𐡐=wx.SHAPED
𢥚=wx.NOT_FOUND
𪻟=wx.Button
ښ=wx.RIGHT
𐳓=wx.LEFT
𮇑=wx.BOTTOM
𩒰=wx.GridSizer
𞤮=wx.StaticBoxSizer
𐦲=wx.ALL
𰩉=wx.RA_VERTICAL
𐦔=wx.RadioBox
𖡑=wx.Panel
𑣿=wx.ImageFromBuffer
𨶠=wx.EXPAND
𥛅=wx.HORIZONTAL
𐣭=wx.VERTICAL
וּ=wx.BoxSizer
椂=wx.NullColour
𥖍=wx.Size
ࣇ=wx.App
𗊛=wx.Frame
import threading
𞸲=threading.Lock
import re
𩰣=re.IGNORECASE
𐰶=re.MULTILINE
𮋄=re.compile
import logging
𞢏=logging.LogRecord
吥=logging.Formatter
𐰣=logging.getLogger
import cv2 as cv
ﰫ=cv.COLOR_BGR2RGB
燹=cv.cvtColor
from 𝒓 import(ValuesView,DeviceInfoView,HistogramView,SerialView,ChipRegisterView,AdcView,BufferedCanvas,MainMenuBar,)
𐤡=BufferedCanvas.__init__
from logging import StreamHandler
蜙=StreamHandler.__init__
import TAER_Core
𞸐=TAER_Core.Libs
𝒓=TAER_Core.Views
from 𞸐.config import ViewConfig
import TAER_Add_Ons
𫓡=TAER_Add_Ons.__file__
class ﻆ(𗊛):
 def __init__(𐰨):
  𐰨.app=ࣇ()
  卬=𐰨.__get_current_version()
  𗊛.__init__(𐰨,戼,title=f"pyAER {tag}")
 def ﳍ(𐰨):
  𐰨.config_data=ﳌ()
  𐰨.SetMinSize(𥖍(𐰨.config_data.main_panel_size.w,𐰨.config_data.main_panel_size.h))
  𐰨.__create_layout()
  𐰨.__init_logic()
 def __create_layout(𐰨):
  𐰨.SetBackgroundColour(椂)
  𐰨.menu_bar=𞤫(𐰨)
  𐰨.SetMenuBar(𐰨.menu_bar)
  𐰨.main_box=וּ(𐣭)
  𐰨.hbox=וּ(𥛅)
  𐰨.panel_control=ﮮ(𐰨)
  𐰨.panel_image=𞡎(𐰨)
  𐰨.logging_panel=ﵿ(𐰨)
  𐰨.hbox.Add(𐰨.panel_control,1,𨶠)
  𐰨.hbox.Add(𐰨.panel_image,3,𨶠)
  𐰨.main_box.Add(𐰨.hbox,2,𨶠)
  𐰨.main_box.Add(𐰨.logging_panel,1,𨶠)
  𐰨.SetSize(𥖍(𐰨.config_data.main_panel_size.w,𐰨.config_data.main_panel_size.h))
  𐰨.SetSizer(𐰨.main_box)
  𐰨.Layout()
  𐰨.__init_other_frames()
 def __init_other_frames(𐰨):
  𐰨.edit_register_device_frame=𞠗(𐰨,"Registers")
  𐰨.edit_register_chip_frame=𐬭(𐰨)
  𐰨.edit_dac_frame=𞠗(𐰨,"DACs")
  𐰨.device_info_frame=𞤎(𐰨)
  𐰨.image_histogram_frame=𐺤(𐰨)
  𐰨.serial_control_frame=𐰔(𐰨)
  𐰨.adc_control_frame=𐲈(𐰨)
 def __init_logic(𐰨):
  𐰨.imgLock=𞸲()
 def __write_version_file(𐰨,filepath):
  ﶖ=git.Repo(𩙇.dirname(__file__))
  𞠚=䋂(ﶖ.tags,key=lambda t:t.commit.committed_datetime)
  卬=裔(𞠚[-1])+"\n"
  with 𡘡(filepath,"w")as ݱ:
   ݱ.write(卬)
 def __read_version_file(𐰨,filepath):
  卬=""
  with 𡘡(filepath,"r")as ݱ:
   卬=ݱ.readline()
  return 卬
 def __get_current_version(𐰨):
  return version("TAER_Core")
 def ﰃ(𐰨):
  𐰨.app.MainLoop()
 def 𡘡(𐰨):
  𐰨.Layout()
  𐰨.CenterOnScreen()
  𐰨.Show()
 def 𪼚(𐰨,destroy=랞):
  if destroy:
   𐰨.Destroy()
  else:
   𐰨.Hide()
 def 𐢙(𐰨):
  搞=𐰨.__get_logger_keys()
  𐦃=ﰓ(𐰨.logging_panel.logging_box)
  for 龵 in 搞:
   𐭨=𐰣(龵)
   𐭨.addHandler(𐦃)
 def __get_logger_keys(𐰨):
  𧒫=𩙇.join(𤘸(),"config","loggers.conf")
  if 𩙇.exists(𧒫):
   𐴚=𧒫
  else:
   𐴚=𩙇.join(𩙇.dirname(𫓡),"config","loggers.conf")
  with 𡘡(𐴚,"r")as ݱ:
   𞡳=ݱ.read()
   𣁆=r"(?<=keys=)(.*)"
   𒃱=𮋄(𣁆,𐰶|𩰣)
   뱺=𒃱.search(𞡳)
   return 뱺.groups()[0].split(",")
 def 𞠯(𐰨,state):
  for 𬉐 in 𐰨.menu_bar.menu_device.GetMenuItems():
   𬉐.Enable(state)
  for 𬉐 in 𐰨.menu_bar.menu_edit.GetMenuItems():
   𬉐.Enable(state)
  for 𬉐 in 𐰨.menu_bar.menu_tools.GetMenuItems():
   𬉐.Enable(state)
  𐰨.panel_control.Enable(state)
  𐰨.edit_register_device_frame.set_menus_state(state)
 def 𢭭(𐰨,state):
  ꑲ=𐰨.panel_control
  if state:
   ꑲ.button_start_stop.SetLabel("Start")
   ꑲ.button_capture.Enable(랞)
  else:
   ꑲ.button_start_stop.SetLabel("Stop")
   ꑲ.button_capture.Enable(ڮ)
 def 𪽱(𐰨,mode):
  𐰨.panel_control.set_selected_mode(mode)
 @𐀤
 def ﻺ(𐰨):
  with 𐰨.imgLock:
   return 𐰨.panel_image.img_ctrl.img
 @ﻺ.setter
 def ﻺ(𐰨,value):
  with 𐰨.imgLock:
   𣾄,乻=value.shape[:2] 
   𐦔=燹(value,ﰫ)
   𐰨.panel_image.img_ctrl.img=𑣿(乻,𣾄,𐦔)
  𐰨.panel_image.img_ctrl.update()
class ﮮ(𖡑):
 def __init__(𐰨,𐨭):
  𖡑.__init__(𐰨,𐨭)
  𐰨.parent=𐨭
  𐰨.__create_layout()
 def __create_layout(𐰨):
  𐰨.SetBackgroundColour(椂)
  𐀸=𐰨.parent.config_data.control_panel.modes
  氕=[mode[0]for mode in 𐀸]
  𐰨.vbox=וּ(𐣭)
  𐰨.modes_box=𐦔(𐰨,label="Select mode:",choices=氕,style=𰩉,)
  𐰨.vbox.Add(𐰨.modes_box,0,𨶠|𐦲,20)
  𐰨.control_box=𞤮(𥛅,𐰨,"Sensor Control")
  𐰨.control_grid=𩒰(2,0,0)
  𐰨.control_box.Add(𐰨.control_grid,0,𐦲,5)
  𐰨.𐩳()
  𐰨.vbox.Add(𐰨.control_box,0,𨶠|𮇑|𐳓|ښ,20)
  𐰨.SetSizerAndFit(𐰨.vbox)
  𐰨.Layout()
 def 𐩳(𐰨):
  ޤ=𐰨.control_grid
  鼒=𪻟(𐰨,label="Start")
  ޤ.Add(鼒,0,𐦲,5)
  𐰨.button_start_stop=鼒
  鼒=𪻟(𐰨,label="Capture")
  ޤ.Add(鼒,0,𐦲,5)
  𐰨.button_capture=鼒
  鼒=𪻟(𐰨,label="Reset device")
  ޤ.Add(鼒,0,𐦲,5)
  𐰨.button_reset=鼒
  鼒=𪻟(𐰨,label="Reset AER")
  ޤ.Add(鼒,0,𐦲,5)
  𐰨.button_reset_periphery=鼒
  鼒=𪻟(𐰨,label="Reset Chip")
  ޤ.Add(鼒,0,𐦲,5)
  𐰨.button_reset_chip=鼒
 def 𨼩(𐰨,mode):
  𐼆=𐰨.modes_box.FindString(mode)
  if 𐼆 is not 𢥚:
   𐰨.modes_box.SetSelection(𐼆)
class 𞡎(𖡑):
 def __init__(𐰨,𐨭):
  𖡑.__init__(𐰨,𐨭)
  𐰨.parent=𐨭
  𐰨.__create_layout()
 def __create_layout(𐰨):
  𐰨.SetBackgroundColour(椂)
  𐰨.img_ctrl=𥧙(𐰨)
  𐰨.vsizer=וּ(𐣭)
  𐰨.hsizer=וּ(𥛅)
  𐰨.hsizer.Add(𐰨.img_ctrl,1,𐡐|𥢩|𐦲,10)
  𐰨.vsizer.Add(𐰨.hsizer,1,𐡐|𐪐|𐦲,10)
  𐰨.SetSizer(𐰨.vsizer)
  𐰨.Layout()
class ﵿ(𖡑):
 def __init__(𐰨,𐨭):
  𖡑.__init__(𐰨,𐨭)
  𐰨.SetMinSize(𥖍(100,200))
  𐰨.__create_layout()
 def __create_layout(𐰨):
  𐰨.SetBackgroundColour(椂)
  𐰨.sizer=וּ()
  𛉍=𐳣|ﻭ|𪰼|𰤋|𐠂
  𐰨.logging_box=𐣱(𐰨,style=𛉍)
  𧌜=庾(10,ﻇ,ﰫ,ﰫ,ڮ,"Consolas")
  𐰨.logging_box.SetFont(𧌜)
  𐰨.logging_box.SetMinSize(𥖍(100,20))
  𐰨.sizer.Add(𐰨.logging_box,1,𨶠|𐦲,10)
  𐰨.SetSizer(𐰨.sizer)
class ﰓ(StreamHandler):
 def __init__(𐰨,𭿐:𐣱):
  蜙(𐰨)
  𐰨.txt_control=𭿐
  𐰨.__config()
 def __config(𐰨):
  𐤄="[%(asctime)s.%(msecs)03d] %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
  𬡎=吥(𐤄,datefmt="%H:%M:%S")
  𐰨.setFormatter(𬡎)
  𗿵=𐰨.txt_control.GetDefaultStyle().TextColour
  𐰨.color_default=𗿵
 def ﵴ(𐰨,record:𞢏):
  𐭀(𐰨.ﴦ,record)
 def ﴦ(𐰨,record:𞢏):
  خ=𐰨.𬡎(record)
  ꝿ=𐰨.__get_text_style(record.levelname)
  𐰨.txt_control.SetDefaultStyle(ꝿ)
  𐰨.txt_control.AppendText(خ+"\n")
  𐰨.flush()
 def __get_text_style(𐰨,x:裔)->ﺎ:
  return{"DEBUG":ﺎ(𐰨.color_default),"INFO":ﺎ(𐺡(82,190,128)),"WARNING":ﺎ(𐺡(244,208,63)),"ERROR":ﺎ(𐺡(236,112,99)),"CRITICAL":ﺎ(𐺡(176,58,46)),}[x]
class 𥧙(BufferedCanvas):
 def __init__(𐰨,𐨭):
  𐰨.parent=𐨭
  𐰨.__create_layout()
 def __create_layout(𐰨):
  𰗊=𐰨.parent.GetParent().config_data.image_panel_size
  𐰨.img=ﵝ(𰗊.w,𰗊.h)
  憮=𥖍(𰗊.w,𰗊.h)
  𐤡(𐰨,𐰨.parent,size=憮)
  𐰨.Fit()
 def 쒇(𐰨,dc):
  𫏗,ࢼ=𐰨.GetClientSize()
  if 𫏗>0 and ࢼ>0:
   𐰨.bitmap=𐰨.img.Scale(𫏗,ࢼ).ConvertToBitmap()
   dc.DrawBitmap(𐰨.bitmap,0,0)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
