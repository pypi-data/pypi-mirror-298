import wx
O=wx.CONFIG_USE_RELATIVE_PATH
A=wx.CONFIG_USE_SUBDIR
o=wx.CONFIG_USE_LOCAL_FILE
w=wx.Config
b=wx.FH_PATH_SHOW_ALWAYS
c=wx.FileHistory
I=wx.NewId
P=wx.MenuItem
M=wx.Menu
t=wx.MenuBar
class H(t):
 def __init__(G,x):
  t.__init__(G)
  G.view=x
  G.__add_menus()
 def __add_menus(G):
  G.menu_device=E()
  G.Append(G.menu_device,"&Device")
  G.menu_edit=q()
  G.Append(G.menu_edit,"&Edit")
  G.menu_image=N()
  G.Append(G.menu_image,"&Image")
  G.menu_tools=g()
  G.Append(G.menu_tools,"&Tools")
 def h(G,tools):
  G.menu_tools.configure_tools(tools)
class q(M):
 def __init__(G):
  M.__init__(G)
  G.__config()
 def __config(G):
  G.item_save_preset=P(G,I(),"&Save preset as...")
  G.Append(G.item_save_preset)
  G.item_load_preset=P(G,I(),"&Load preset...")
  G.Append(G.item_load_preset)
  G.item_reg_dev=P(G,I(),"&Device registers")
  G.Append(G.item_reg_dev)
  G.item_reg_chip=P(G,I(),"&Chip registers")
  G.Append(G.item_reg_chip)
  G.item_dac=P(G,I(),"&DACs")
  G.Append(G.item_dac)
class E(M):
 def __init__(G):
  M.__init__(G)
  G.__config()
 def __config(G):
  G.item_info=P(G,I(),"&Info")
  G.Append(G.item_info)
  G.item_program=P(G,I(),"&Program...")
  G.Append(G.item_program)
  G.program_history=c()
  G.program_history.SetMenuPathStyle(b)
  G.program_history_config=w("pyAER",localFilename="./tmp/.pyAER_recent_files",style=o|A|O,)
  G.program_history.Load(G.program_history_config)
  G.item_program_history=M()
  G.program_history.UseMenu(G.item_program_history)
  G.program_history.AddFilesToMenu()
  G.AppendSubMenu(G.item_program_history,"Recent binary files")
class N(M):
 def __init__(G):
  M.__init__(G)
  G.__config()
 def __config(G):
  G.item_histogram=P(G,I(),"&Histogram")
  G.Append(G.item_histogram)
class g(M):
 def __init__(G):
  M.__init__(G)
  G.__config()
 def __config(G):
  G.items={}
  Q="Write SPI"
  G.items[Q]=P(G,I(),f"&{item_name}")
  G.Append(G.items[Q])
  Q="ADCs"
  G.items[Q]=P(G,I(),f"&{item_name}")
  G.Append(G.items[Q])
  Q="Execute test"
  G.items[Q]=P(G,I(),f"&{item_name}")
  G.Append(G.items[Q])
 def h(G,tools):
  for S in tools:
   Q=S
   G.items[Q]=P(G,I(),f"&{item_name}")
   G.Append(G.items[Q])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
