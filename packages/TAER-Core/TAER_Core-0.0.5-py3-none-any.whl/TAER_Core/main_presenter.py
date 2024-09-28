import sys
PS=True
PE=False
Pm=None
Pp=hasattr
Pg=str
Pz=id
Pv=int
PC=isinstance
Ph=round
Pu=Exception
PN=float
Pw=open
YK=sys.version
import os
Ya=os.makedirs
Yf=os.getcwd
Yn=os.path
import pickle
YI=pickle.load
Yd=pickle.HIGHEST_PROTOCOL
YX=pickle.dump
import logging
YA=logging.getLogger
YW=logging.config
import YW
import threading
Yb=threading.Thread
import time
YU=time.sleep
Yt=time.time
import numpy as np
YD=np.histogram
Ys=np.linspace
import wx
PY=wx.FD_FILE_MUST_EXIST
Yk=wx.FD_OPEN
Yi=wx.ID_CANCEL
Ye=wx.FD_CHANGE_DIR
YR=wx.FD_OVERWRITE_PROMPT
YV=wx.FD_SAVE
YH=wx.FileDialog
YQ=wx.CheckBox
YL=wx.CallAfter
YF=wx.version
Yc=wx.ID_OK
Yl=wx.lib
import Yl.intctrl as wxInt
from TAER_Core.main_model import MainModel
from TAER_Core.main_view import MainView
from TAER_Core.Views import SelectConfigDialog
from TAER_Core.Controllers import*
from TAER_Core.Libs import Config
PM=Config.CONFIG_PATH
import TAER_Add_Ons
Pj=TAER_Add_Ons.__file__
PG=TAER_Add_Ons.Initializers
PO=TAER_Add_Ons.Tools
from PO import*
from PO.tool_base import ToolBase
Po=ToolBase.__subclasses__
from PG import*
from PG.initializer_base import InitializerBase
Pq=InitializerBase.__subclasses__
class Yr:
 def __init__(Y,P:MainModel,M:MainView,O:MainInteractor):
  Y.model=P
  Y.view=M
  Y.interactor=O
 def __install_interactors(Y,O):
  O.install(Y,Y.view)
  O=InteractorEditMenuBase()
  M=Y.view.edit_register_device_frame
  O.install(Y.delegates_edit_register_device,M)
  O=InteractorEditRegisterChip()
  M=Y.view.edit_register_chip_frame
  O.install(Y.delegates_edit_register_chip,M)
  O=InteractorEditMenuBase()
  M=Y.view.edit_dac_frame
  O.install(Y.delegates_edit_dac,M)
 def __config(Y):
  Y.__config_logging()
  Y.__config_logic()
  Y.__config_model()
  Y.__config_initializer()
  Y.__config_tools()
  Y.__config_view()
  Y.__config_delegates()
 def __config_logging(Y):
  G=Yn.join(Yf(),"config","loggers.conf")
  if Yn.exists(G):
   j=G
  else:
   j=Yn.join(Yn.dirname(Pj),"config","loggers.conf")
  o=Yn.join(Yf(),"logs")
  Ya(o,exist_ok=PS)
  YW.fileConfig(j)
  Y.logger=YA(__name__)
 def __config_logic(Y):
  Y.stop_flag=PS
  Y.stop_cature_flag=PS
  Y.one_shot_flag=PE
  Y.img_thread_handler=Pm
  Y.adc_thread_handler=Pm
 def __config_model(Y):
  Y.model.config()
 def __config_view(Y):
  Y.view.config()
  Y.view.init_log_box()
  Y.view.menu_bar.configure_tools(Y.tools.keys())
  Y.__update_view_on_gui_thread("init")
 def __config_delegates(Y):
  M=Y.view
  Y.delegates_main=S(Y,M,Y.model)
  Y.delegates_edit_register_device=E(Y,Y.view.edit_register_device_frame,Y.model)
  Y.delegates_edit_register_chip=m(Y,Y.view.edit_register_chip_frame,Y.model)
  Y.delegates_edit_dac=E(Y,Y.view.edit_dac_frame,Y.model)
  Y.model.device.register_on_connection_change_callback(Y.delegates_main.on_connection_change)
  Y.model.register_on_model_update_cb(Y.Yo)
 def __config_tools(Y):
  Y.tools={}
  p=Po()
  for g in p:
   z=g(Y.model,Y.view)
   if z.is_enabled:
    Y.tools[z.name]=z
   else:
    z=Pm
 def __config_initializer(Y):
  v=Y.model.Yy
  p=Pq()
  Y.initializer=Pm
  for g in p:
   C=g(Y.model)
   if C.chip_name==v:
    Y.initializer=C
    if Pp(Y.initializer,"gen_serial_frame"):
     Y.model.gen_serial_frame=Y.initializer.gen_serial_frame
    if Pp(Y.initializer,"parse_serial_frame"):
     Y.model.parse_serial_frame=Y.initializer.parse_serial_frame
   else:
    C=Pm
  if Y.initializer is Pm:
   Y.logger.warning("Default initializer loaded. Configured initializer not found.")
   Y.initializer=h(Y.model)
 def YM(Y):
  u=Y.__show_select_config_dialog()
  if u!="":
   PM=u
   Y.__config()
   Y.view.Pw()
   Y.__install_interactors(Y.interactor)
   del Y.interactor
   Y.stop_flag=PE
   Y.model.device.start()
   Y.__print_welcome_message()
   Y.initializer.on_start_app()
   Y.view.start_event_loop()
  else:
   Y.view.close()
 def YO(Y):
  Y.initializer.on_close_app()
  Y.YG()
 def YG(Y):
  Y.model.device.stop()
  Y.Yp()
  Y.Yz()
  Y.stop_flag=PS
 def __show_select_config_dialog(Y)->Pg:
  with SelectConfigDialog(Y.view)as dlg:
   if dlg.ShowModal()==Yc:
    return dlg.get_choice_selected()
   else:
    return ""
 def __print_welcome_message(Y):
  Y.logger.info("pyAER")
  Y.logger.info("Python %s",YK)
  Y.logger.info("wxPython %s",YF())
 def Yj(Y):
  YL(Y.__update_image_on_gui_thread)
 def __update_image_on_gui_thread(Y):
  Y.view.image=Y.model.main_img
  Y.view.image_histogram_frame.update_histogram(Y.model.img_histogram)
 def Yo(Y,Pz=""):
  YL(Y.__update_view_on_gui_thread,Pz)
 def __update_view_on_gui_thread(Y,Pz):
  if(Pz=="init" or(Pz=="" and Y.view.IsShown())or Y.view.GetId()==Pz):
   Y.view.set_menus_state(Y.model.device.is_connected)
  M=Y.view.edit_register_device_frame
  if Pz=="init" or(Pz=="" and M.IsShown())or M.GetId()==Pz:
   N=Y.model.dev_reg_db
   Y.view.edit_register_device_frame.update_values(N.get_item_list())
  M=Y.view.edit_register_chip_frame
  if Pz=="init" or(Pz=="" and M.IsShown())or M.GetId()==Pz:
   N=Y.model.chip_reg_db
   Y.view.edit_register_chip_frame.update_values(N.get_item_list())
  M=Y.view.edit_dac_frame
  if Pz=="init" or(Pz=="" and M.IsShown())or M.GetId()==Pz:
   w=Y.model.dacs_db
   Y.view.edit_dac_frame.update_values(w.get_item_list())
  M=Y.view.adc_control_frame
  if Pz=="init" or(Pz=="" and M.IsShown())or M.GetId()==Pz:
   x=Y.model.adc_db
   Y.view.adc_control_frame.update_values(x.get_item_list(),Y.model.adc_tmeas)
  for _,B in Y.tools.items():
   if B.is_shown()and Pz=="":
    B.Yo()
 def Yq(Y,Pz):
  if Pz==Y.view.edit_register_device_frame.GetId():
   Y.logger.info("Update registers")
   M=Y.view.edit_register_device_frame
   r=M.panel_values.values_widgets
   K={}
   for n,widget in r.items():
    K[n]=Pv(widget.GetValue(),0)
   Y.model.write_dev_registers(K)
  if Pz==Y.view.edit_dac_frame.GetId():
   Y.logger.info("Update DACs")
   M=Y.view.edit_dac_frame
   r=M.panel_values.values_widgets
   f={}
   for n,widget in r.items():
    f[n]=Pv(widget.GetValue(),0)
   Y.model.write_dacs(f)
  if Pz==Y.view.edit_register_chip_frame.GetId():
   r=Y.view.edit_register_chip_frame.panel_values.values_widgets
   for a,widget in r.items():
    if PC(widget,wxInt.IntCtrl):
     X=widget.GetValue()
     Y.model.write_signal(a,X)
    elif PC(widget,YQ):
     X=widget.GetValue()
     if X:
      X=1
     else:
      X=0
     Y.model.write_signal(a,X)
  Y.logger.info("Updated.")
 def YS(Y):
  if Y.img_thread_handler is Pm:
   Y.one_shot_flag=PS
   Y.img_thread_handler=Yb(target=Y.__img_thread)
   Y.img_thread_handler.start()
 def YE(Y):
  if Y.stop_cature_flag:
   Y.Ym()
  else:
   Y.Yp()
 def Ym(Y):
  Y.stop_cature_flag=PE
  Y.view.set_capture_mode(Y.stop_cature_flag)
  Y.img_thread_handler=Yb(target=Y.__img_thread)
  Y.img_thread_handler.start()
 def Yp(Y):
  Y.stop_cature_flag=PS
  Y.view.set_capture_mode(Y.stop_cature_flag)
  if Y.img_thread_handler!=Pm:
   if Y.img_thread_handler.is_alive():
    Y.img_thread_handler.join()
 def __img_thread(Y):
  I=not Y.stop_cature_flag or Y.one_shot_flag and not Y.stop_flag
  Y.initializer.on_init_capture()
  if Y.model.FR_raw_mode_en:
   Y.__continuous_FR_raw_loop(I)
  elif Y.model.TFS_raw_mode_en:
   Y.__continuous_TFS_raw_loop(I)
  else:
   Y.__standard_loop(I)
  Y.initializer.on_end_capture()
  Y.img_thread_handler=Pm
  Y.logger.debug("Image thread finished")
 def __continuous_FR_raw_loop(Y,I):
  Y.initializer.on_before_capture()
  Y.model.device.actions.events_done()
  Y.model.device.actions.start_capture()
  W=(Y.model.read_dev_register("N_EVENTS")//4)*32
  while I:
   A=Y.YC(Y.model.device.actions.events_done,Y.model.YT,)
   if not A:
    Y.logger.error("Image readout timeout.")
   else:
    t1=Yt()
    Y.logger.info(f"Events: {self.model.device.actions.get_evt_count()}")
    J=Y.model.read_raw_data(W)
    Y.initializer.on_after_capture(J)
    Y.Yj()
    if J.size>0:
     y=0.125*W/(J[-1]-J[1])
     Y.logger.info("New data appended. Event rate :"+Pg(Ph(y,2))+"Meps/s.")
    T,b=Y.model.device.actions.check_addr_ram()
    t=b-T
    if t>2*W:
     Y.logger.warning("WARNING! Data is arriving faster that time required for writting.")
    Y.logger.info("Execution time: "+Pg(Ph(Yt()-t1,3)))
   if Y.stop_flag:
    break
   elif Y.one_shot_flag:
    Y.one_shot_flag=PE
    break
   I=(not Y.stop_cature_flag or Y.one_shot_flag and not Y.stop_flag)
  Y.model.device.actions.stop_capture()
  Y.model.device.actions.reset_fifo()
  Y.model.device.actions.reset_ram()
  Y.model.device.actions.reset_aer()
 def __continuous_TFS_raw_loop(Y,I):
  Y.initializer.on_before_capture()
  Y.model.device.actions.events_done()
  while I:
   Y.model.device.actions.start_capture()
   A=Y.YC(Y.model.device.actions.is_captured,Y.model.YT,)
   if not A:
    Y.logger.error("Image readout timeout.")
   else:
    t1=Yt()
    Y.model.device.actions.stop_capture()
    W=(Y.model.device.actions.get_evt_count()//4)*32
    J=Y.model.read_raw_data(W)
    Y.initializer.on_after_capture(J)
    Y.Yj()
    if J.size>0:
     y=0.125*W/(J[-1]-J[1])
     Y.logger.info("New data appended. Event rate :"+Pg(Ph(y,2))+"Meps/s.")
    T,b=Y.model.device.actions.check_addr_ram()
    t=b-T
    if t>2*W:
     Y.logger.warning("WARNING! Data is arriving faster that time required for writting.")
    Y.logger.info("Execution time: "+Pg(Ph(Yt()-t1,3)))
   if Y.stop_flag:
    break
   elif Y.one_shot_flag:
    Y.one_shot_flag=PE
    break
   I=(not Y.stop_cature_flag or Y.one_shot_flag and not Y.stop_flag)
  Y.model.device.actions.stop_capture()
  Y.model.device.actions.reset_fifo()
  Y.model.device.actions.reset_ram()
  Y.model.device.actions.reset_aer()
 def __standard_loop(Y,I):
  U=Y.model.dev_reg_db.get_item_by_address(0x06).value
  if U==0:
   U=1
  while I:
   t1=Yt()
   Y.initializer.on_before_capture()
   Y.model.device.actions.start_capture()
   A=Y.YC(Y.model.device.actions.is_captured,Y.model.YT,)
   Y.model.device.actions.stop_capture()
   if not A:
    Y.logger.error("Image readout timeout.")
   else:
    J=Y.model.read_image(U)
    Y.initializer.on_after_capture(J)
    try:
     Y.Yv()
    except Pu as e:
     Y.logger.error(e)
    Y.Yj()
   if Y.stop_flag:
    break
   elif Y.one_shot_flag:
    Y.one_shot_flag=PE
    break
   I=(not Y.stop_cature_flag or Y.one_shot_flag and not Y.stop_flag)
   Y.logger.debug(f"Time: {(time.time()-t1)*1000} ms")
 def Yg(Y):
  if Y.adc_thread_handler is Pm:
   Y.flag_adc_run=PS
   Y.adc_thread_handler=Yb(target=Y.__adc_thread)
   Y.adc_thread_handler.start()
  for s in Y.model.adc_db.d_item.values():
   s.reset_data()
 def Yz(Y):
  Y.flag_adc_run=PE
  if Y.adc_thread_handler is not Pm:
   if Y.adc_thread_handler.is_alive():
    Y.adc_thread_handler.join()
   Y.adc_thread_handler=Pm
 def Yv(Y):
  if Y.view.image_histogram_frame.IsShown():
   Y.__process_img_histogram()
 def YC(Y,somepredicate,timeout,period=0.25,*args,**kwargs):
  D=Yt()+timeout
  while Yt()<D:
   if somepredicate(*args,**kwargs):
    return PS
   YU(period)
  return PE
 def Yh(Y):
  J=(Y.view.serial_control_frame.panel_serial_control.serial_tx_box.GetValue())
  l=[Pv(num,0)for num in J.replace(" ","").split(",")]
  Y.logger.debug(f"Serial data sent: {serial_data_tx}")
  Y.model.device.actions.write_serial(l) 
  c=(Y.model.device.actions.read_serial()) 
  Y.logger.debug(f"Serial data read: {serial_data_rx}")
  if c is not Pm:
   Y.view.serial_control_frame.panel_serial_control.serial_rx_box.SetValue(Pg(", ".join(Pg(s)for s in c)))
  else:
   Y.view.serial_control_frame.panel_serial_control.serial_rx_box.SetValue("No RX data received.")
 def Yu(Y):
  Y.model.adc_tmeas=PN(Y.view.adc_control_frame.panel_menu.sampletime_textbox.GetValue())
 def YN(Y):
  x=Y.model.adc_db
  Y.view.adc_control_frame.update_panels(x.get_item_list())
 def Yw(Y,mode):
  Y.model.set_mode(mode)
 def Yx(Y):
  F=Y.model.get_preset()
  with YH(Y.view,"Save preset as...",wildcard="Preset files (*.preset)|*.preset",style=YV|YR|Ye,)as fileDialog:
   if fileDialog.ShowModal()!=Yi:
    Q=fileDialog.GetPath()
    if not Q.endswith(".preset"):
     Q=Q+".preset"
    with Pw(Q,"wb")as fp:
     YX(F,fp,Yd)
 def YB(Y):
  H=Pm
  with YH(Y.view,"Load preset",wildcard="Preset files (*.preset)|*.preset",style=Yk|PY|Ye,)as fileDialog:
   if fileDialog.ShowModal()!=Yi:
    V=fileDialog.GetPath()
    with Pw(V,"rb")as fp:
     H=YI(fp)
  if H is not Pm:
   Y.model.set_preset(H)
   Y.view.set_mode(H["mode"])
 def __process_img_histogram(Y):
  X=Y.model.main_img_data.flatten()
  R=Y.model.img_histogram
  e=Ys(R.min,R.max,R.bins)
  i=YD(X,e)
  Y.model.img_histogram.value=i
 def __adc_thread(Y):
  t0=Yt()
  Pz=Y.view.adc_control_frame.GetId()
  while Y.flag_adc_run:
   for k in Y.model.adc_db.d_item.values():
    t1=Yt()
    YP=Y.model.device.actions.read_adc(k.device_id,k.channel)
    k.add_data(t1-t0,YP)
   Y.Yo(Pz)
   if Y.flag_adc_run:
    YU(Y.model.adc_tmeas)
  Y.logger.debug("ADC thread finished")
# Created by pyminifier (https://github.com/liftoff/pyminifier)
