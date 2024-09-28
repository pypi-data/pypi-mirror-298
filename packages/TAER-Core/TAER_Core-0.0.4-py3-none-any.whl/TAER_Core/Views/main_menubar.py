import wx
ݦ=wx.CONFIG_USE_RELATIVE_PATH
颉=wx.CONFIG_USE_SUBDIR
ﻳ=wx.CONFIG_USE_LOCAL_FILE
𐴗=wx.Config
𐫃=wx.FH_PATH_SHOW_ALWAYS
ﲛ=wx.FileHistory
𱉄=wx.NewId
ݛ=wx.MenuItem
𡣖=wx.Menu
𡺘=wx.MenuBar
class 뱘(𡺘):
 def __init__(𰽼,𫒣):
  𡺘.__init__(𰽼)
  𰽼.view=𫒣
  𰽼.__add_menus()
 def __add_menus(𰽼):
  𰽼.menu_device=𖩂()
  𰽼.Append(𰽼.menu_device,"&Device")
  𰽼.menu_edit=ﷹ()
  𰽼.Append(𰽼.menu_edit,"&Edit")
  𰽼.menu_image=𞠭()
  𰽼.Append(𰽼.menu_image,"&Image")
  𰽼.menu_tools=ﰥ()
  𰽼.Append(𰽼.menu_tools,"&Tools")
 def 𐦍(𰽼,tools):
  𰽼.menu_tools.configure_tools(tools)
class ﷹ(𡣖):
 def __init__(𰽼):
  𡣖.__init__(𰽼)
  𰽼.__config()
 def __config(𰽼):
  𰽼.item_save_preset=ݛ(𰽼,𱉄(),"&Save preset as...")
  𰽼.Append(𰽼.item_save_preset)
  𰽼.item_load_preset=ݛ(𰽼,𱉄(),"&Load preset...")
  𰽼.Append(𰽼.item_load_preset)
  𰽼.item_reg_dev=ݛ(𰽼,𱉄(),"&Device registers")
  𰽼.Append(𰽼.item_reg_dev)
  𰽼.item_reg_chip=ݛ(𰽼,𱉄(),"&Chip registers")
  𰽼.Append(𰽼.item_reg_chip)
  𰽼.item_dac=ݛ(𰽼,𱉄(),"&DACs")
  𰽼.Append(𰽼.item_dac)
class 𖩂(𡣖):
 def __init__(𰽼):
  𡣖.__init__(𰽼)
  𰽼.__config()
 def __config(𰽼):
  𰽼.item_info=ݛ(𰽼,𱉄(),"&Info")
  𰽼.Append(𰽼.item_info)
  𰽼.item_program=ݛ(𰽼,𱉄(),"&Program...")
  𰽼.Append(𰽼.item_program)
  𰽼.program_history=ﲛ()
  𰽼.program_history.SetMenuPathStyle(𐫃)
  𰽼.program_history_config=𐴗("pyAER",localFilename="./tmp/.pyAER_recent_files",style=ﻳ|颉|ݦ,)
  𰽼.program_history.Load(𰽼.program_history_config)
  𰽼.item_program_history=𡣖()
  𰽼.program_history.UseMenu(𰽼.item_program_history)
  𰽼.program_history.AddFilesToMenu()
  𰽼.AppendSubMenu(𰽼.item_program_history,"Recent binary files")
class 𞠭(𡣖):
 def __init__(𰽼):
  𡣖.__init__(𰽼)
  𰽼.__config()
 def __config(𰽼):
  𰽼.item_histogram=ݛ(𰽼,𱉄(),"&Histogram")
  𰽼.Append(𰽼.item_histogram)
class ﰥ(𡣖):
 def __init__(𰽼):
  𡣖.__init__(𰽼)
  𰽼.__config()
 def __config(𰽼):
  𰽼.items={}
  埮="Write SPI"
  𰽼.items[埮]=ݛ(𰽼,𱉄(),f"&{item_name}")
  𰽼.Append(𰽼.items[埮])
  埮="ADCs"
  𰽼.items[埮]=ݛ(𰽼,𱉄(),f"&{item_name}")
  𰽼.Append(𰽼.items[埮])
  埮="Execute test"
  𰽼.items[埮]=ݛ(𰽼,𱉄(),f"&{item_name}")
  𰽼.Append(𰽼.items[埮])
 def 𐦍(𰽼,tools):
  for 𢦈 in tools:
   埮=𢦈
   𰽼.items[埮]=ݛ(𰽼,𱉄(),f"&{item_name}")
   𰽼.Append(𰽼.items[埮])
# Created by pyminifier (https://github.com/liftoff/pyminifier)
