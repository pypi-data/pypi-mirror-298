import wx
class O(wx.MenuBar):
 def __init__(s,w):
  wx.MenuBar.__init__(s)
  s.view=w
  s.__add_menus()
 def __add_menus(s):
  s.menu_device=G()
  s.Append(s.menu_device,"&Device")
  s.menu_edit=b()
  s.Append(s.menu_edit,"&Edit")
  s.menu_image=q()
  s.Append(s.menu_image,"&Image")
  s.menu_tools=K()
  s.Append(s.menu_tools,"&Tools")
 def D(s,tools):
  s.menu_tools.configure_tools(tools)
class b(wx.Menu):
 def __init__(s):
  wx.Menu.__init__(s)
  s.__config()
 def __config(s):
  s.item_save_preset=wx.MenuItem(s,wx.NewId(),"&Save preset as...")
  s.Append(s.item_save_preset)
  s.item_load_preset=wx.MenuItem(s,wx.NewId(),"&Load preset...")
  s.Append(s.item_load_preset)
  s.item_reg_dev=wx.MenuItem(s,wx.NewId(),"&Device registers")
  s.Append(s.item_reg_dev)
  s.item_reg_chip=wx.MenuItem(s,wx.NewId(),"&Chip registers")
  s.Append(s.item_reg_chip)
  s.item_dac=wx.MenuItem(s,wx.NewId(),"&DACs")
  s.Append(s.item_dac)
class G(wx.Menu):
 def __init__(s):
  wx.Menu.__init__(s)
  s.__config()
 def __config(s):
  s.item_info=wx.MenuItem(s,wx.NewId(),"&Info")
  s.Append(s.item_info)
  s.item_program=wx.MenuItem(s,wx.NewId(),"&Program...")
  s.Append(s.item_program)
  s.program_history=wx.FileHistory()
  s.program_history.SetMenuPathStyle(wx.FH_PATH_SHOW_ALWAYS)
  s.program_history_config=wx.Config("pyAER",localFilename="./tmp/.pyAER_recent_files",style=wx.CONFIG_USE_LOCAL_FILE|wx.CONFIG_USE_SUBDIR|wx.CONFIG_USE_RELATIVE_PATH,)
  s.program_history.Load(s.program_history_config)
  s.item_program_history=wx.Menu()
  s.program_history.UseMenu(s.item_program_history)
  s.program_history.AddFilesToMenu()
  s.AppendSubMenu(s.item_program_history,"Recent binary files")
class q(wx.Menu):
 def __init__(s):
  wx.Menu.__init__(s)
  s.__config()
 def __config(s):
  s.item_histogram=wx.MenuItem(s,wx.NewId(),"&Histogram")
  s.Append(s.item_histogram)
class K(wx.Menu):
 def __init__(s):
  wx.Menu.__init__(s)
  s.__config()
 def __config(s):
  s.items={}
  Q="Write SPI"
  s.items[Q]=wx.MenuItem(s,wx.NewId(),f"&{item_name}")
  s.Append(s.items[Q])
  Q="ADCs"
  s.items[Q]=wx.MenuItem(s,wx.NewId(),f"&{item_name}")
  s.Append(s.items[Q])
  Q="Execute test"
  s.items[Q]=wx.MenuItem(s,wx.NewId(),f"&{item_name}")
  s.Append(s.items[Q])
 def D(s,tools):
  for d in tools:
   Q=d
   s.items[Q]=wx.MenuItem(s,wx.NewId(),f"&{item_name}")
   s.Append(s.items[Q])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
