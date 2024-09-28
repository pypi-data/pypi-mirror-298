""" Opal Kelly device class """
uJ=False
ub=None
uf=property
uj=bool
uV=True
ug=str
un=dict
uL=int
ud=bytearray
uP=min
uq=len
uI=list
uE=pow
ux=super
import logging
uw=logging.getLogger
import time
uz=time.time
uc=time.sleep
import ok
uH=ok.okTRegisterEntry
uS=ok.okTRegisterEntries
uB=ok.okTDeviceInfo
uC=ok.okCFrontPanel
uA=ok.FrontPanelManager
from threading import Lock
class ui(uA):
 def __init__(v):
  uA.__init__(v)
  v.__handler=uC()
  v.vendor_info=uB()
  v.info=i()
  v.lock=u()
  v.is_connected=uJ
  v.on_connection_change_callback=ub
  v.logger=uw(__name__)
  v.actions=a(v,v.logger)
 @uf
 def il(v):
  return v.__handler
 def __get_device_info(v)->uj:
  v.vendor_info=uB()
  if v.__handler is not ub:
   v.__get_lock__()
   U=v.__handler.GetDeviceInfo(v.vendor_info)
   v.__release_lock__()
   if v.__handler.NoError!=U:
    v.logger.info("Unable to retrieve device information.")
    return uJ
  v.info.set_values_from_OK(v.vendor_info)
  return uV
 def ik(v):
  v.StartMonitoring()
 def iN(v):
  v.StopMonitoring()
 def iO(v,bitstream:ug):
  v.ir(bitstream)
  v.im()
 def im(v):
  pass
 def __get_lock__(v):
  v.lock.acquire(timeout=5)
 def __release_lock__(v):
  v.lock.release()
 def ir(v,bit_stream_path:ug="")->uj:
  v.__get_lock__()
  v.__handler.LoadDefaultPLLConfiguration()
  U=v.__handler.ConfigureFPGA(bit_stream_path)
  v.__release_lock__()
  if v.__handler.NoError!=U:
   v.logger.error("FPGA configuration failed.")
   return uJ
  v.logger.info("Device %s configuration success.",v.vendor_info.productName)
  v.__get_lock__()
  X=v.__handler.IsFrontPanelEnabled()
  v.__release_lock__()
  if not X:
   v.logger.error("Front Panel isn't enabled.")
   return uJ
  uc(1.5)
  if not v.actions.check_calibration():
   v.logger.error("Device RAM isn't calibrated.")
   return uJ
  v.actions.reset_device()
  return uV
 def ip(v,l):
  v.on_connection_change_callback=l
 def iD(v):
  if v.on_connection_change_callback is not ub:
   v.on_connection_change_callback()
 def iK(v,serial:ug)->ub:
  v.logger.debug("On device %s connected.",serial)
  if v.is_connected:
   return
  v.__get_lock__()
  v.__handler=v.Open(serial)
  v.__release_lock__()
  if not v.__handler:
   v.logger.error("A device could not be opened.")
  else:
   k=v.__get_device_info()
   if k:
    v.logger.info("Device %s connected.",v.vendor_info.productName)
    v.is_connected=uV
    v.iD()
 def io(v,serial:ug)->ub:
  v.__get_lock__()
  N=v.__handler.IsOpen()
  v.__release_lock__()
  if not N:
   v.logger.debug("On device %s disconnected.",v.vendor_info.productName)
   del v.__handler
   v.__handler=ub
   v.is_connected=uJ
   v.logger.info("Device %s disconnected.",v.vendor_info.productName)
   v.iD()
  else:
   v.logger.debug("On device %s disconnected.",serial)
class i:
 def __init__(v)->ub:
  v.vendor=ug()
  v.product_name=ug()
  v.serial_number=ug()
  v.dev_version=ug()
 def iM(v,O:uB):
  v.vendor="Opal Kelly"
  v.product_name=ug(O.productName)
  v.serial_number=ug(O.serialNumber)
  v.dev_version=".".join([ug(O.deviceMajorVersion),ug(O.deviceMinorVersion)])
class a:
 m=0x01
 r=32 
 p=1024*1024
 def __init__(v,D:ui,logger=uw(__name__))->ub:
  v.device=D
  v.links=K()
  v.logger=o
 def iW(v,address,M):
  v.device.__get_lock__()
  v.device.interface.WriteRegister(address,M)
  v.device.__release_lock__()
 def iy(v,address):
  v.device.__get_lock__()
  M=v.device.interface.ReadRegister(address)
  v.device.__release_lock__()
  U=v.device.interface.NoError
  v.__check_err_code(U,f"Reading register address {address} -> value {value}")
  return M
 def iR(v,registers):
  W=uS()
  for y in registers.values():
   R=uH()
   R.address=y.address
   R.data=y.value
   W.append(R)
  v.device.__get_lock__()
  s=v.device.interface.WriteRegisters(W)
  v.device.__release_lock__()
  if v.device.interface.NoError==s:
   v.logger.info("Device register write success.")
  else:
   v.logger.error("Device register write failed with code %s.",s)
 def iw(v,registers)->un:
  W=uS()
  for y in registers.values():
   R=uH()
   R.address=y.address
   W.append(R)
  v.device.__get_lock__()
  s=v.device.interface.ReadRegisters(W)
  v.device.__release_lock__()
  if v.device.interface.NoError==s:
   v.logger.info("Device register read success.")
   w={}
   for R in W:
    w[R.address]=R.data
   return w
  else:
   v.logger.error("Device register read failed with code %s.",s)
   return{}
 def ic(v,address,channel,M):
  v.__set_wire__(v.links.win_dac,address,ur.DAC_SEL)
  v.__set_wire__(v.links.win_dac,v.DAC_WRITE_MODE,ur.DAC_MODE)
  v.__set_wire__(v.links.win_dac,channel,ur.DAC_CHANNEL)
  v.__set_wire__(v.links.win_dac,M,ur.DAC_VALUE)
  v.__update_wires__()
  v.__set_trigger__(v.links.trig_in,uR.TRIG_DAC)
 def iz(v,dacs):
  for c in dacs.values():
   v.ic(c.address,c.channel,c.value)
 def iA(v,address,channel)->uL:
  v.__set_wire__(v.links.win_adc,address,um.ADC_ID)
  v.__set_wire__(v.links.win_adc,channel,um.ADC_CHANNEL)
  v.__update_wires__()
  v.__set_trigger__(v.links.trig_in,uR.TRIG_ADC)
  z=v.__wait_until(v.iC,1)
  if z:
   A=v.__read_wire__(v.links.wout_adc,uK.ADC_DATA)
  else:
   A=0
  return A
 def iC(v)->uj:
  C=v.__read_trigger__(v.links.trig_out,us.ADC_DATA_VALID)
  return C
 def iB(v):
  v.ig()
  v.iL()
  v.__set_wire__(v.links.win0,1,uk.WRITE_EN_RAM)
  v.__update_wires__()
  v.__set_trigger__(v.links.trig_in,uR.START)
 def iS(v):
  v.__set_trigger__(v.links.trig_in,uR.STOP)
 def iH(v)->uj:
  C=v.__read_trigger__(v.links.trig_out,us.VIDEO_DONE)
  return C
 def iJ(v)->uj:
  C=v.__read_trigger__(v.links.trig_out,us.EVENTS_DONE)
  return C
 def ib(v):
  v.__set_wire_as_trigger__(v.links.win0,uk.RESET_CHIP)
  v.__update_wires__()
 def ij(v):
  v.__set_wire_as_trigger__(v.links.win0,uk.RESET_PERIPH)
  v.__update_wires__()
 def iV(v):
  v.__set_wire_as_trigger__(v.links.win0,uk.RESET)
  v.__update_wires__()
 def ig(v):
  v.__set_wire__(v.links.win0,0,uk.READ_EN_RAM)
  v.__set_wire__(v.links.win0,0,uk.WRITE_EN_RAM)
  v.__set_wire_as_trigger__(v.links.win0,uk.RESET_FIFO)
  v.__update_wires__()
 def iL(v):
  v.__set_wire_as_trigger__(v.links.win0,uk.RESET_RAM)
  v.__update_wires__()
 def iP(v):
  M=v.__read_wire__(v.links.wout_calib,up.CALIB)
  if M==0:
   return uJ
  else:
   return uV
 def iq(v,is_enabled):
  if is_enabled:
   v.__set_wire__(v.links.win0,1,uk.CLK_20M_EN)
  else:
   v.__set_wire__(v.links.win0,0,uk.CLK_20M_EN)
  v.__update_wires__()
 def iI(v):
  B=v.__read_wire__(v.links.wout_xy,uy.X)
  S=v.__read_wire__(v.links.wout_xy,uy.Y)
  return B,S
 def iE(v,J):
  v.ig()
  v.iL()
  H=v.__read_ram_block(J)
  v.__set_wire__(v.links.win0,0,uk.READ_EN_RAM)
  v.__update_wires__()
  return H
 def ix(v,J):
  H=v.__read_ram_block(J)
  v.__set_trigger__(v.links.trig_in,uR.EVENTS_READ)
  return H
 def __read_ram_block(v,J):
  v.__set_wire__(v.links.win0,1,uk.READ_EN_RAM)
  v.__update_wires__()
  J=(J//16)*16
  b=0
  H=ud()
  while b<J:
   f=uP([v.RAM_READBUF_SIZE,J])
   j=v.__read_block_pipe_out__(v.links.pipe_out0,f)
   H.extend(j)
   b=b+f
  return H
 def iT(v):
  V=v.__read_wire__(v.links.wout_ram_read,uM.ADDR_RD)
  g=v.__read_wire__(v.links.wout_ram_write,uW.ADDR_WR)
  return V,g
 def iG(v,data_tx):
  v.__write_serial_fifo(data_tx)
 def iF(v):
  n=v.__read_serial_fifo()
  return n
 def ie(v,is_enabled):
  if is_enabled:
   v.__set_wire__(v.links.win0,1,uk.TEST_TFS_EN)
   v.__set_wire__(v.links.win0,1,uk.CLK_TFS_EN)
   v.__update_wires__()
  else:
   v.__set_wire__(v.links.win0,0,uk.TEST_TFS_EN)
   v.__set_wire__(v.links.win0,0,uk.CLK_TFS_EN)
   v.__update_wires__()
 def ih(v,mode):
  v.__set_wire__(v.links.win0,mode,uk.MODES)
  v.__update_wires__()
 def iY(v,signal,M):
  if signal==0:
   v.__set_wire__(v.links.win0,M,uk.AUX0)
  elif signal==1:
   v.__set_wire__(v.links.win0,M,uk.AUX1)
  elif signal==2:
   v.__set_wire__(v.links.win0,M,uk.AUX2)
  elif signal==3:
   v.__set_wire__(v.links.win0,M,uk.AUX3)
  elif signal==4:
   v.__set_wire__(v.links.win0,M,uk.AUX4)
  elif signal==5:
   v.__set_wire__(v.links.win0,M,uk.AUX5)
  v.__update_wires__()
 def iQ(v,switch_bit,M):
  if switch_bit==0:
   v.__set_wire__(v.links.win_pcb,M,uN.BIT0)
  elif switch_bit==1:
   v.__set_wire__(v.links.win_pcb,M,uN.BIT1)
  elif switch_bit==2:
   v.__set_wire__(v.links.win_pcb,M,uN.BIT2)
  elif switch_bit==3:
   v.__set_wire__(v.links.win_pcb,M,uN.BIT3)
  elif switch_bit==4:
   v.__set_wire__(v.links.win_pcb,M,uN.BIT4)
  elif switch_bit==5:
   v.__set_wire__(v.links.win0,M,uN.BIT5)
  v.__update_wires__()
 def uv(v)->uL:
  L=v.__read_wire__(v.links.wout_evt_count,uo.EVT_COUNT)
  return L
 def __write_serial_fifo(v,H):
  if H is not ub:
   d=uq(H) 
   H.reverse()
   v.__set_register__(v.links.reg_spi,d)
   v.__set_trigger__(v.links.trig_in,uR.SERIAL_RX_RST_FIFO)
   while d>0:
    P=v.__read_wire__(v.links.wout0,uD.SERIAL_TX_FULL)
    while P:
     P=v.__read_wire__(v.links.wout0,uD.SERIAL_TX_FULL)
     uc(0.01)
    if d>0:
     v.__set_wire__(v.links.win_spi,H[d-1],uO.BYTE3)
    if d>1:
     v.__set_wire__(v.links.win_spi,H[d-2],uO.BYTE2)
    if d>2:
     v.__set_wire__(v.links.win_spi,H[d-3],uO.BYTE1)
    if d>3:
     v.__set_wire__(v.links.win_spi,H[d-4],uO.BYTE0)
    v.__update_wires__()
    v.__set_trigger__(v.links.trig_in,uR.SERIAL_TX_WEN)
    d=d-4
   v.logger.debug(f"{len(data)} bytes sent to the serial driver.")
   uc(0.0005) 
  else:
   v.logger.error("Serial TX data is None.")
 def __read_serial_fifo(v):
  q=uI()
  I=v.__read_wire__(v.links.wout0,uD.SERIAL_RX_EMPTY)
  if I:
   v.logger.error("No RX data found in serial fifo. Make sure the device is answering or delay is long enough.")
   return ub
  else:
   while not I:
    v.__set_trigger__(v.links.trig_in,uR.SERIAL_RX_REN)
    E=v.__read_wire__(v.links.wout0,uD.SERIAL_RX_BYTE)
    q.append(E)
    I=v.__read_wire__(v.links.wout0,uD.SERIAL_RX_EMPTY)
   v.logger.debug(f"{len(data_read)} bytes read from the serial driver.")
   return q
 def __set_trigger__(v,address,trigger):
  v.device.__get_lock__()
  U=v.device.interface.ActivateTriggerIn(address,trigger.offset)
  v.device.__release_lock__()
  v.__check_err_code(U,f"Activate trigger address {address} bit {trigger.offset}")
 def __read_trigger__(v,address,trigger):
  v.device.__get_lock__()
  U=v.device.interface.UpdateTriggerOuts()
  v.__check_err_code(U,"Update trigger out")
  C=v.device.interface.IsTriggered(address,trigger.mask)
  v.device.__release_lock__()
  return C
 def __set_wire_as_trigger__(v,address,wire):
  v.__set_wire__(address,1,wire)
  v.__update_wires__()
  v.__set_wire__(address,0,wire)
  v.__update_wires__()
 def __read_wire__(v,address,wire):
  v.device.__get_lock__()
  U=v.device.interface.UpdateWireOuts()
  v.__check_err_code(U,f"Read wire out {address}")
  x=v.device.interface.GetWireOutValue(address)
  v.device.__release_lock__()
  return(x&wire.mask)>>wire.offset
 def __set_wire__(v,address,M,wire):
  v.device.__get_lock__()
  T=M<<wire.offset
  U=v.device.interface.SetWireInValue(address,T,wire.mask)
  v.device.__release_lock__()
  v.__check_err_code(U,f"Set wire -> bits {format(to_write_value, '#032b')} -> mask {format(wire.mask,'#032b')} in address {address}",)
 def __update_wires__(v):
  v.device.__get_lock__()
  U=v.device.interface.UpdateWireIns()
  v.device.__release_lock__()
  v.__check_err_code(U,"Update wire in")
 def __read_block_pipe_out__(v,address,length):
  G=ud(length)
  v.device.__get_lock__()
  U=v.device.interface.ReadFromBlockPipeOut(address,v.RAM_BLOCK_SIZE,G)
  v.device.__release_lock__()
  if U<0:
   v.__check_err_code(U,f"Read pipe block with address {address}")
  else:
   v.logger.debug(f"Query {length} bytes \t Read {err_code} bytes")
  return G
 def __set_register__(v,address,M):
  v.device.__get_lock__()
  U=v.device.interface.WriteRegister(address,M)
  v.device.__release_lock__()
  v.__check_err_code(U,f"Writing register address {address} value {value}")
 def __check_err_code(v,U,msg=""):
  if U!=v.device.interface.NoError:
   v.logger.error(msg+f" failed with code({err_code}).")
   v.logger.error(f"Opal kelly error message: {self.device.interface.GetLastErrorMessage()}")
  else:
   v.logger.debug(msg+" OK.")
 def __wait_until(v,somepredicate,t,period=0.01,*args,**kwargs):
  F=uz()+t
  while uz()<F:
   if somepredicate(*args,**kwargs):
    return uV
   uc(period)
  return uJ
class K:
 def __init__(v)->ub:
  v.win0=0x00
  v.win_spi=0x01
  v.win_adc=0x02
  v.win_pcb=0x03
  v.win_dac=0x04
  v.reg_spi=0x08
  v.wout_calib=0x20
  v.wout0=0x21
  v.wout_xy=0x22
  v.wout_adc=0x23
  v.wout_evt_count=0x27
  v.wout_ram_read=0x28
  v.wout_ram_write=0x29
  v.trig_in=0x41
  v.trig_out=0x60
  v.pipe_out0=0xA0
class uX:
 def __init__(v,h,end=0)->ub:
  if e!=0:
   v.size=e-h+1
  else:
   v.size=1
  v.offset=h
  v.mask=(uE(2,v.size)-1)<<h
class ul(uX):
 def __init__(v,h)->ub:
  ux().__init__(h)
class uk:
 Y=uX(0)
 Q=uX(1)
 vi=uX(2)
 vu=uX(3)
 va=uX(4)
 vU=uX(5)
 vt=uX(7)
 vX=uX(8)
 vl=uX(9)
 vk=uX(10)
 vN=uX(20)
 vO=uX(21)
 vm=uX(22)
 vr=uX(23)
 vp=uX(24)
 vD=uX(25)
 vK=uX(26)
 vo=uX(27)
 vM=uX(29,31)
class uN:
 vW=uX(0)
 vy=uX(1)
 vR=uX(2)
 vs=uX(3)
 vw=uX(4)
 vc=uX(5)
 vz=uX(6)
class uO:
 vA=uX(0,7)
 vC=uX(8,15)
 vB=uX(16,23)
 vS=uX(24,31)
 vH=uX(0,31)
class um:
 vJ=uX(0,1)
 vb=uX(2,3)
class ur:
 vf=uX(0,11)
 vj=uX(12,13)
 vV=uX(14,15)
 vg=uX(16,17)
class up:
 vn=uX(0)
class uD:
 vL=uX(0,7)
 vd=uX(8)
 vP=uX(10)
 vq=uX(9)
class uK:
 vI=uX(0,11)
class uo:
 vE=uX(0,31)
class uM:
 vx=uX(0,31)
class uW:
 vT=uX(0,31)
class uy:
 X=uX(0,15)
 Y=uX(16,31)
class uR:
 vG=ul(0)
 vF=ul(1)
 ve=ul(2)
 vh=ul(3)
 vY=ul(4)
 vQ=ul(5)
 iv=ul(6)
 iu=ul(7)
class us:
 ia=ul(0)
 iU=ul(1)
 it=ul(2)
 iX=ul(3)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
