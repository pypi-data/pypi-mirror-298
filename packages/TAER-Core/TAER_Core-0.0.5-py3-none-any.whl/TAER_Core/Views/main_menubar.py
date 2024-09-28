import wx
x=wx.CONFIG_USE_RELATIVE_PATH
H=wx.CONFIG_USE_SUBDIR
L=wx.CONFIG_USE_LOCAL_FILE
c=wx.Config
l=wx.FH_PATH_SHOW_ALWAYS
i=wx.FileHistory
C=wx.NewId
A=wx.MenuItem
J=wx.Menu
P=wx.MenuBar
class d(P):
 def __init__(U,w):
  P.__init__(U)
  U.view=w
  U.__add_menus()
 def __add_menus(U):
  U.menu_device=S()
  U.Append(U.menu_device,"&Device")
  U.menu_edit=g()
  U.Append(U.menu_edit,"&Edit")
  U.menu_image=X()
  U.Append(U.menu_image,"&Image")
  U.menu_tools=F()
  U.Append(U.menu_tools,"&Tools")
 def v(U,tools):
  U.menu_tools.configure_tools(tools)
class g(J):
 def __init__(U):
  J.__init__(U)
  U.__config()
 def __config(U):
  U.item_save_preset=A(U,C(),"&Save preset as...")
  U.Append(U.item_save_preset)
  U.item_load_preset=A(U,C(),"&Load preset...")
  U.Append(U.item_load_preset)
  U.item_reg_dev=A(U,C(),"&Device registers")
  U.Append(U.item_reg_dev)
  U.item_reg_chip=A(U,C(),"&Chip registers")
  U.Append(U.item_reg_chip)
  U.item_dac=A(U,C(),"&DACs")
  U.Append(U.item_dac)
class S(J):
 def __init__(U):
  J.__init__(U)
  U.__config()
 def __config(U):
  U.item_info=A(U,C(),"&Info")
  U.Append(U.item_info)
  U.item_program=A(U,C(),"&Program...")
  U.Append(U.item_program)
  U.program_history=i()
  U.program_history.SetMenuPathStyle(l)
  U.program_history_config=c("pyAER",localFilename="./tmp/.pyAER_recent_files",style=L|H|x,)
  U.program_history.Load(U.program_history_config)
  U.item_program_history=J()
  U.program_history.UseMenu(U.item_program_history)
  U.program_history.AddFilesToMenu()
  U.AppendSubMenu(U.item_program_history,"Recent binary files")
class X(J):
 def __init__(U):
  J.__init__(U)
  U.__config()
 def __config(U):
  U.item_histogram=A(U,C(),"&Histogram")
  U.Append(U.item_histogram)
class F(J):
 def __init__(U):
  J.__init__(U)
  U.__config()
 def __config(U):
  U.items={}
  T="Write SPI"
  U.items[T]=A(U,C(),f"&{item_name}")
  U.Append(U.items[T])
  T="ADCs"
  U.items[T]=A(U,C(),f"&{item_name}")
  U.Append(U.items[T])
  T="Execute test"
  U.items[T]=A(U,C(),f"&{item_name}")
  U.Append(U.items[T])
 def v(U,tools):
  for j in tools:
   T=j
   U.items[T]=A(U,C(),f"&{item_name}")
   U.Append(U.items[T])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
