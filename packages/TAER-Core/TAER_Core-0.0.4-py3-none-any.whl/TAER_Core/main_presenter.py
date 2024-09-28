import sys
𞺛=True
𞺓=False
𐡉=None
ﻀ=hasattr
ﳸ=str
𐲜=id
𐬗=int
己=isinstance
𐢍=round
ﰇ=Exception
𞹗=float
ﺧ=open
𦤎=sys.version
import os
𡰇=os.makedirs
𐤀=os.getcwd
ﱿ=os.path
import pickle
朁=pickle.load
𤎰=pickle.HIGHEST_PROTOCOL
跇=pickle.dump
import logging
豁=logging.getLogger
ᕰ=logging.config
import ᕰ
import threading
𞢗=threading.Thread
import time
ﺐ=time.sleep
𨈁=time.time
import numpy as np
𥕔=np.histogram
𞡨=np.linspace
import wx
𬎁=wx.FD_FILE_MUST_EXIST
坱=wx.FD_OPEN
ﹲ=wx.ID_CANCEL
𞹙=wx.FD_CHANGE_DIR
ﲓ=wx.FD_OVERWRITE_PROMPT
𤑦=wx.FD_SAVE
땀=wx.FileDialog
𡧩=wx.CheckBox
𗺰=wx.CallAfter
𢖍=wx.version
ᛀ=wx.ID_OK
𞸬=wx.lib
import 𞸬.intctrl as wxInt
from TAER_Core.main_model import MainModel
from TAER_Core.main_view import MainView
from TAER_Core.Views import SelectConfigDialog
from TAER_Core.Controllers import*
from TAER_Core.Libs import Config
珠=Config.CONFIG_PATH
import TAER_Add_Ons
𐠍=TAER_Add_Ons.__file__
𐬩=TAER_Add_Ons.Initializers
猠=TAER_Add_Ons.Tools
from 猠 import*
from 猠.tool_base import ToolBase
潀=ToolBase.__subclasses__
from 𐬩 import*
from 𐬩.initializer_base import InitializerBase
𪘕=InitializerBase.__subclasses__
class 𐬒:
 def __init__(꾍,讀:MainModel,𐰞:MainView,鲑:MainInteractor):
  꾍.model=讀
  꾍.view=𐰞
  꾍.interactor=鲑
 def __install_interactors(꾍,鲑):
  鲑.install(꾍,꾍.view)
  鲑=InteractorEditMenuBase()
  𐰞=꾍.view.edit_register_device_frame
  鲑.install(꾍.delegates_edit_register_device,𐰞)
  鲑=InteractorEditRegisterChip()
  𐰞=꾍.view.edit_register_chip_frame
  鲑.install(꾍.delegates_edit_register_chip,𐰞)
  鲑=InteractorEditMenuBase()
  𐰞=꾍.view.edit_dac_frame
  鲑.install(꾍.delegates_edit_dac,𐰞)
 def __config(꾍):
  꾍.__config_logging()
  꾍.__config_logic()
  꾍.__config_model()
  꾍.__config_initializer()
  꾍.__config_tools()
  꾍.__config_view()
  꾍.__config_delegates()
 def __config_logging(꾍):
  ﶧ=ﱿ.join(𐤀(),"config","loggers.conf")
  if ﱿ.exists(ﶧ):
   ࢾ=ﶧ
  else:
   ࢾ=ﱿ.join(ﱿ.dirname(𐠍),"config","loggers.conf")
  𐰪=ﱿ.join(𐤀(),"logs")
  𡰇(𐰪,exist_ok=𞺛)
  ᕰ.fileConfig(ࢾ)
  꾍.logger=豁(__name__)
 def __config_logic(꾍):
  꾍.stop_flag=𞺛
  꾍.stop_cature_flag=𞺛
  꾍.one_shot_flag=𞺓
  꾍.img_thread_handler=𐡉
  꾍.adc_thread_handler=𐡉
 def __config_model(꾍):
  꾍.model.config()
 def __config_view(꾍):
  꾍.view.config()
  꾍.view.init_log_box()
  꾍.view.menu_bar.configure_tools(꾍.tools.keys())
  꾍.__update_view_on_gui_thread("init")
 def __config_delegates(꾍):
  𐰞=꾍.view
  꾍.delegates_main=𐡓(꾍,𐰞,꾍.model)
  꾍.delegates_edit_register_device=𐰉(꾍,꾍.view.edit_register_device_frame,꾍.model)
  꾍.delegates_edit_register_chip=𐳋(꾍,꾍.view.edit_register_chip_frame,꾍.model)
  꾍.delegates_edit_dac=𐰉(꾍,꾍.view.edit_dac_frame,꾍.model)
  꾍.model.device.register_on_connection_change_callback(꾍.delegates_main.on_connection_change)
  꾍.model.register_on_model_update_cb(꾍.ﵩ)
 def __config_tools(꾍):
  꾍.tools={}
  𐪅=潀()
  for ࢬ in 𐪅:
   𐳟=ࢬ(꾍.model,꾍.view)
   if 𐳟.is_enabled:
    꾍.tools[𐳟.name]=𐳟
   else:
    𐳟=𐡉
 def __config_initializer(꾍):
  ﻩ=꾍.model.ﰌ
  𐪅=𪘕()
  꾍.initializer=𐡉
  for ࢬ in 𐪅:
   𡈍=ࢬ(꾍.model)
   if 𡈍.chip_name==ﻩ:
    꾍.initializer=𡈍
    if ﻀ(꾍.initializer,"gen_serial_frame"):
     꾍.model.gen_serial_frame=꾍.initializer.gen_serial_frame
    if ﻀ(꾍.initializer,"parse_serial_frame"):
     꾍.model.parse_serial_frame=꾍.initializer.parse_serial_frame
   else:
    𡈍=𐡉
  if 꾍.initializer is 𐡉:
   꾍.logger.warning("Default initializer loaded. Configured initializer not found.")
   꾍.initializer=𭝞(꾍.model)
 def 㑶(꾍):
  𐡦=꾍.__show_select_config_dialog()
  if 𐡦!="":
   珠=𐡦
   꾍.__config()
   꾍.view.ﺧ()
   꾍.__install_interactors(꾍.interactor)
   del 꾍.interactor
   꾍.stop_flag=𞺓
   꾍.model.device.start()
   꾍.__print_welcome_message()
   꾍.initializer.on_start_app()
   꾍.view.start_event_loop()
  else:
   꾍.view.close()
 def 𪛘(꾍):
  꾍.initializer.on_close_app()
  꾍.𐮌()
 def 𐮌(꾍):
  꾍.model.device.stop()
  꾍.𰄕()
  꾍.𐩳()
  꾍.stop_flag=𞺛
 def __show_select_config_dialog(꾍)->ﳸ:
  with SelectConfigDialog(꾍.view)as dlg:
   if dlg.ShowModal()==ᛀ:
    return dlg.get_choice_selected()
   else:
    return ""
 def __print_welcome_message(꾍):
  꾍.logger.info("pyAER")
  꾍.logger.info("Python %s",𦤎)
  꾍.logger.info("wxPython %s",𢖍())
 def 𐲁(꾍):
  𗺰(꾍.__update_image_on_gui_thread)
 def __update_image_on_gui_thread(꾍):
  꾍.view.image=꾍.model.main_img
  꾍.view.image_histogram_frame.update_histogram(꾍.model.img_histogram)
 def ﵩ(꾍,𐲜=""):
  𗺰(꾍.__update_view_on_gui_thread,𐲜)
 def __update_view_on_gui_thread(꾍,𐲜):
  if(𐲜=="init" or(𐲜=="" and 꾍.view.IsShown())or 꾍.view.GetId()==𐲜):
   꾍.view.set_menus_state(꾍.model.device.is_connected)
  𐰞=꾍.view.edit_register_device_frame
  if 𐲜=="init" or(𐲜=="" and 𐰞.IsShown())or 𐰞.GetId()==𐲜:
   ﵒ=꾍.model.dev_reg_db
   꾍.view.edit_register_device_frame.update_values(ﵒ.get_item_list())
  𐰞=꾍.view.edit_register_chip_frame
  if 𐲜=="init" or(𐲜=="" and 𐰞.IsShown())or 𐰞.GetId()==𐲜:
   ﵒ=꾍.model.chip_reg_db
   꾍.view.edit_register_chip_frame.update_values(ﵒ.get_item_list())
  𐰞=꾍.view.edit_dac_frame
  if 𐲜=="init" or(𐲜=="" and 𐰞.IsShown())or 𐰞.GetId()==𐲜:
   ﰦ=꾍.model.dacs_db
   꾍.view.edit_dac_frame.update_values(ﰦ.get_item_list())
  𐰞=꾍.view.adc_control_frame
  if 𐲜=="init" or(𐲜=="" and 𐰞.IsShown())or 𐰞.GetId()==𐲜:
   𐠠=꾍.model.adc_db
   꾍.view.adc_control_frame.update_values(𐠠.get_item_list(),꾍.model.adc_tmeas)
  for _,읮 in 꾍.tools.items():
   if 읮.is_shown()and 𐲜=="":
    읮.ﵩ()
 def 弮(꾍,𐲜):
  if 𐲜==꾍.view.edit_register_device_frame.GetId():
   꾍.logger.info("Update registers")
   𐰞=꾍.view.edit_register_device_frame
   𤚻=𐰞.panel_values.values_widgets
   𞡖={}
   for 𡓮,widget in 𤚻.items():
    𞡖[𡓮]=𐬗(widget.GetValue(),0)
   꾍.model.write_dev_registers(𞡖)
  if 𐲜==꾍.view.edit_dac_frame.GetId():
   꾍.logger.info("Update DACs")
   𐰞=꾍.view.edit_dac_frame
   𤚻=𐰞.panel_values.values_widgets
   ﯺ={}
   for 𡓮,widget in 𤚻.items():
    ﯺ[𡓮]=𐬗(widget.GetValue(),0)
   꾍.model.write_dacs(ﯺ)
  if 𐲜==꾍.view.edit_register_chip_frame.GetId():
   𤚻=꾍.view.edit_register_chip_frame.panel_values.values_widgets
   for ײַ,widget in 𤚻.items():
    if 己(widget,wxInt.IntCtrl):
     ﺰ=widget.GetValue()
     꾍.model.write_signal(ײַ,ﺰ)
    elif 己(widget,𡧩):
     ﺰ=widget.GetValue()
     if ﺰ:
      ﺰ=1
     else:
      ﺰ=0
     꾍.model.write_signal(ײַ,ﺰ)
  꾍.logger.info("Updated.")
 def 𠟣(꾍):
  if 꾍.img_thread_handler is 𐡉:
   꾍.one_shot_flag=𞺛
   꾍.img_thread_handler=𞢗(target=꾍.__img_thread)
   꾍.img_thread_handler.start()
 def 𛉎(꾍):
  if 꾍.stop_cature_flag:
   꾍.ﳭ()
  else:
   꾍.𰄕()
 def ﳭ(꾍):
  꾍.stop_cature_flag=𞺓
  꾍.view.set_capture_mode(꾍.stop_cature_flag)
  꾍.img_thread_handler=𞢗(target=꾍.__img_thread)
  꾍.img_thread_handler.start()
 def 𰄕(꾍):
  꾍.stop_cature_flag=𞺛
  꾍.view.set_capture_mode(꾍.stop_cature_flag)
  if 꾍.img_thread_handler!=𐡉:
   if 꾍.img_thread_handler.is_alive():
    꾍.img_thread_handler.join()
 def __img_thread(꾍):
  嬾=not 꾍.stop_cature_flag or 꾍.one_shot_flag and not 꾍.stop_flag
  꾍.initializer.on_init_capture()
  if 꾍.model.FR_raw_mode_en:
   꾍.__continuous_FR_raw_loop(嬾)
  elif 꾍.model.TFS_raw_mode_en:
   꾍.__continuous_TFS_raw_loop(嬾)
  else:
   꾍.__standard_loop(嬾)
  꾍.initializer.on_end_capture()
  꾍.img_thread_handler=𐡉
  꾍.logger.debug("Image thread finished")
 def __continuous_FR_raw_loop(꾍,嬾):
  꾍.initializer.on_before_capture()
  꾍.model.device.actions.events_done()
  꾍.model.device.actions.start_capture()
  ﺊ=(꾍.model.read_dev_register("N_EVENTS")//4)*32
  while 嬾:
   𐼛=꾍.𐩱(꾍.model.device.actions.events_done,꾍.model.𐰒,)
   if not 𐼛:
    꾍.logger.error("Image readout timeout.")
   else:
    𪦗=𨈁()
    꾍.logger.info(f"Events: {self.model.device.actions.get_evt_count()}")
    姌=꾍.model.read_raw_data(ﺊ)
    꾍.initializer.on_after_capture(姌)
    꾍.𐲁()
    if 姌.size>0:
     𐡵=0.125*ﺊ/(姌[-1]-姌[1])
     꾍.logger.info("New data appended. Event rate :"+ﳸ(𐢍(𐡵,2))+"Meps/s.")
    嬚,𐿢=꾍.model.device.actions.check_addr_ram()
    ࣁ=𐿢-嬚
    if ࣁ>2*ﺊ:
     꾍.logger.warning("WARNING! Data is arriving faster that time required for writting.")
    꾍.logger.info("Execution time: "+ﳸ(𐢍(𨈁()-𪦗,3)))
   if 꾍.stop_flag:
    break
   elif 꾍.one_shot_flag:
    꾍.one_shot_flag=𞺓
    break
   嬾=(not 꾍.stop_cature_flag or 꾍.one_shot_flag and not 꾍.stop_flag)
  꾍.model.device.actions.stop_capture()
  꾍.model.device.actions.reset_fifo()
  꾍.model.device.actions.reset_ram()
  꾍.model.device.actions.reset_aer()
 def __continuous_TFS_raw_loop(꾍,嬾):
  꾍.initializer.on_before_capture()
  꾍.model.device.actions.events_done()
  while 嬾:
   꾍.model.device.actions.start_capture()
   𐼛=꾍.𐩱(꾍.model.device.actions.is_captured,꾍.model.𐰒,)
   if not 𐼛:
    꾍.logger.error("Image readout timeout.")
   else:
    𪦗=𨈁()
    꾍.model.device.actions.stop_capture()
    ﺊ=(꾍.model.device.actions.get_evt_count()//4)*32
    姌=꾍.model.read_raw_data(ﺊ)
    꾍.initializer.on_after_capture(姌)
    꾍.𐲁()
    if 姌.size>0:
     𐡵=0.125*ﺊ/(姌[-1]-姌[1])
     꾍.logger.info("New data appended. Event rate :"+ﳸ(𐢍(𐡵,2))+"Meps/s.")
    嬚,𐿢=꾍.model.device.actions.check_addr_ram()
    ࣁ=𐿢-嬚
    if ࣁ>2*ﺊ:
     꾍.logger.warning("WARNING! Data is arriving faster that time required for writting.")
    꾍.logger.info("Execution time: "+ﳸ(𐢍(𨈁()-𪦗,3)))
   if 꾍.stop_flag:
    break
   elif 꾍.one_shot_flag:
    꾍.one_shot_flag=𞺓
    break
   嬾=(not 꾍.stop_cature_flag or 꾍.one_shot_flag and not 꾍.stop_flag)
  꾍.model.device.actions.stop_capture()
  꾍.model.device.actions.reset_fifo()
  꾍.model.device.actions.reset_ram()
  꾍.model.device.actions.reset_aer()
 def __standard_loop(꾍,嬾):
  𞢥=꾍.model.dev_reg_db.get_item_by_address(0x06).value
  if 𞢥==0:
   𞢥=1
  while 嬾:
   𪦗=𨈁()
   꾍.initializer.on_before_capture()
   꾍.model.device.actions.start_capture()
   𐼛=꾍.𐩱(꾍.model.device.actions.is_captured,꾍.model.𐰒,)
   꾍.model.device.actions.stop_capture()
   if not 𐼛:
    꾍.logger.error("Image readout timeout.")
   else:
    姌=꾍.model.read_image(𞢥)
    꾍.initializer.on_after_capture(姌)
    try:
     꾍.쭨()
    except ﰇ as e:
     꾍.logger.error(e)
    꾍.𐲁()
   if 꾍.stop_flag:
    break
   elif 꾍.one_shot_flag:
    꾍.one_shot_flag=𞺓
    break
   嬾=(not 꾍.stop_cature_flag or 꾍.one_shot_flag and not 꾍.stop_flag)
   꾍.logger.debug(f"Time: {(time.time()-t1)*1000} ms")
 def ﱓ(꾍):
  if 꾍.adc_thread_handler is 𐡉:
   꾍.flag_adc_run=𞺛
   꾍.adc_thread_handler=𞢗(target=꾍.__adc_thread)
   꾍.adc_thread_handler.start()
  for אַ in 꾍.model.adc_db.d_item.values():
   אַ.reset_data()
 def 𐩳(꾍):
  꾍.flag_adc_run=𞺓
  if 꾍.adc_thread_handler is not 𐡉:
   if 꾍.adc_thread_handler.is_alive():
    꾍.adc_thread_handler.join()
   꾍.adc_thread_handler=𐡉
 def 쭨(꾍):
  if 꾍.view.image_histogram_frame.IsShown():
   꾍.__process_img_histogram()
 def 𐩱(꾍,somepredicate,timeout,period=0.25,*args,**kwargs):
  ڛ=𨈁()+timeout
  while 𨈁()<ڛ:
   if somepredicate(*args,**kwargs):
    return 𞺛
   ﺐ(period)
  return 𞺓
 def 𐴎(꾍):
  姌=(꾍.view.serial_control_frame.panel_serial_control.serial_tx_box.GetValue())
  煦=[𐬗(num,0)for num in 姌.replace(" ","").split(",")]
  꾍.logger.debug(f"Serial data sent: {serial_data_tx}")
  꾍.model.device.actions.write_serial(煦) 
  𞹎=(꾍.model.device.actions.read_serial()) 
  꾍.logger.debug(f"Serial data read: {serial_data_rx}")
  if 𞹎 is not 𐡉:
   꾍.view.serial_control_frame.panel_serial_control.serial_rx_box.SetValue(ﳸ(", ".join(ﳸ(s)for s in 𞹎)))
  else:
   꾍.view.serial_control_frame.panel_serial_control.serial_rx_box.SetValue("No RX data received.")
 def ﮜ(꾍):
  꾍.model.adc_tmeas=𞹗(꾍.view.adc_control_frame.panel_menu.sampletime_textbox.GetValue())
 def 𐢑(꾍):
  𐠠=꾍.model.adc_db
  꾍.view.adc_control_frame.update_panels(𐠠.get_item_list())
 def 𐳕(꾍,mode):
  꾍.model.set_mode(mode)
 def 𧠢(꾍):
  𨦪=꾍.model.get_preset()
  with 땀(꾍.view,"Save preset as...",wildcard="Preset files (*.preset)|*.preset",style=𤑦|ﲓ|𞹙,)as fileDialog:
   if fileDialog.ShowModal()!=ﹲ:
    𞡊=fileDialog.GetPath()
    if not 𞡊.endswith(".preset"):
     𞡊=𞡊+".preset"
    with ﺧ(𞡊,"wb")as fp:
     跇(𨦪,fp,𤎰)
 def ཆ(꾍):
  𐰵=𐡉
  with 땀(꾍.view,"Load preset",wildcard="Preset files (*.preset)|*.preset",style=坱|𬎁|𞹙,)as fileDialog:
   if fileDialog.ShowModal()!=ﹲ:
    𪽼=fileDialog.GetPath()
    with ﺧ(𪽼,"rb")as fp:
     𐰵=朁(fp)
  if 𐰵 is not 𐡉:
   꾍.model.set_preset(𐰵)
   꾍.view.set_mode(𐰵["mode"])
 def __process_img_histogram(꾍):
  ﺰ=꾍.model.main_img_data.flatten()
  𐠧=꾍.model.img_histogram
  𞹝=𞡨(𐠧.min,𐠧.max,𐠧.bins)
  𞹗=𥕔(ﺰ,𞹝)
  꾍.model.img_histogram.value=𞹗
 def __adc_thread(꾍):
  ﲞ=𨈁()
  𐲜=꾍.view.adc_control_frame.GetId()
  while 꾍.flag_adc_run:
   for 𞤀 in 꾍.model.adc_db.d_item.values():
    𪦗=𨈁()
    ࠄ=꾍.model.device.actions.read_adc(𞤀.device_id,𞤀.channel)
    𞤀.add_data(𪦗-ﲞ,ࠄ)
   꾍.ﵩ(𐲜)
   if 꾍.flag_adc_run:
    ﺐ(꾍.model.adc_tmeas)
  꾍.logger.debug("ADC thread finished")
# Created by pyminifier (https://github.com/liftoff/pyminifier)
