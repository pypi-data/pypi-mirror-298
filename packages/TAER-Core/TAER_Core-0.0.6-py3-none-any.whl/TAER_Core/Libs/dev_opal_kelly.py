""" Opal Kelly device class """
DT=False
DY=None
Di=property
DO=bool
Dp=True
DA=str
Dd=dict
DC=int
DQ=bytearray
DK=min
DE=len
Dh=list
DM=pow
DP=super
import logging
Dc=logging.getLogger
import time
Df=time.time
Dv=time.sleep
import ok
Dy=ok.okTRegisterEntry
Dw=ok.okTRegisterEntries
Db=ok.okTDeviceInfo
DR=ok.okCFrontPanel
Du=ok.FrontPanelManager
from threading import Lock
class qs(Du):
 def __init__(I):
  Du.__init__(I)
  I.__handler=DR()
  I.vendor_info=Db()
  I.info=q()
  I.lock=D()
  I.is_connected=DT
  I.on_connection_change_callback=DY
  I.logger=Dc(__name__)
  I.actions=n(I,I.logger)
 @Di
 def qa(I):
  return I.__handler
 def __get_device_info(I)->DO:
  I.vendor_info=Db()
  if I.__handler is not DY:
   I.__get_lock__()
   k=I.__handler.GetDeviceInfo(I.vendor_info)
   I.__release_lock__()
   if I.__handler.NoError!=k:
    I.logger.info("Unable to retrieve device information.")
    return DT
  I.info.set_values_from_OK(I.vendor_info)
  return Dp
 def qF(I):
  I.StartMonitoring()
 def qX(I):
  I.StopMonitoring()
 def qV(I,bitstream:DA):
  I.qW(bitstream)
  I.qB()
 def qB(I):
  pass
 def __get_lock__(I):
  I.lock.acquire(timeout=5)
 def __release_lock__(I):
  I.lock.release()
 def qW(I,bit_stream_path:DA="")->DO:
  I.__get_lock__()
  I.__handler.LoadDefaultPLLConfiguration()
  k=I.__handler.ConfigureFPGA(bit_stream_path)
  I.__release_lock__()
  if I.__handler.NoError!=k:
   I.logger.error("FPGA configuration failed.")
   return DT
  I.logger.info("Device %s configuration success.",I.vendor_info.productName)
  I.__get_lock__()
  G=I.__handler.IsFrontPanelEnabled()
  I.__release_lock__()
  if not G:
   I.logger.error("Front Panel isn't enabled.")
   return DT
  Dv(1.5)
  if not I.actions.check_calibration():
   I.logger.error("Device RAM isn't calibrated.")
   return DT
  I.actions.reset_device()
  return Dp
 def qU(I,a):
  I.on_connection_change_callback=a
 def qH(I):
  if I.on_connection_change_callback is not DY:
   I.on_connection_change_callback()
 def qL(I,serial:DA)->DY:
  I.logger.debug("On device %s connected.",serial)
  if I.is_connected:
   return
  I.__get_lock__()
  I.__handler=I.Open(serial)
  I.__release_lock__()
  if not I.__handler:
   I.logger.error("A device could not be opened.")
  else:
   F=I.__get_device_info()
   if F:
    I.logger.info("Device %s connected.",I.vendor_info.productName)
    I.is_connected=Dp
    I.qH()
 def qt(I,serial:DA)->DY:
  I.__get_lock__()
  X=I.__handler.IsOpen()
  I.__release_lock__()
  if not X:
   I.logger.debug("On device %s disconnected.",I.vendor_info.productName)
   del I.__handler
   I.__handler=DY
   I.is_connected=DT
   I.logger.info("Device %s disconnected.",I.vendor_info.productName)
   I.qH()
  else:
   I.logger.debug("On device %s disconnected.",serial)
class q:
 def __init__(I)->DY:
  I.vendor=DA()
  I.product_name=DA()
  I.serial_number=DA()
  I.dev_version=DA()
 def qg(I,V:Db):
  I.vendor="Opal Kelly"
  I.product_name=DA(V.productName)
  I.serial_number=DA(V.serialNumber)
  I.dev_version=".".join([DA(V.deviceMajorVersion),DA(V.deviceMinorVersion)])
class n:
 B=0x01
 W=32 
 U=1024*1024
 def __init__(I,H:qs,logger=Dc(__name__))->DY:
  I.device=H
  I.links=L()
  I.logger=t
 def qc(I,address,g):
  I.device.__get_lock__()
  I.device.interface.WriteRegister(address,g)
  I.device.__release_lock__()
 def qv(I,address):
  I.device.__get_lock__()
  g=I.device.interface.ReadRegister(address)
  I.device.__release_lock__()
  k=I.device.interface.NoError
  I.__check_err_code(k,f"Reading register address {address} -> value {value}")
  return g
 def qf(I,registers):
  c=Dw()
  for v in registers.values():
   f=Dy()
   f.address=v.address
   f.data=v.value
   c.append(f)
  I.device.__get_lock__()
  u=I.device.interface.WriteRegisters(c)
  I.device.__release_lock__()
  if I.device.interface.NoError==u:
   I.logger.info("Device register write success.")
  else:
   I.logger.error("Device register write failed with code %s.",u)
 def qu(I,registers)->Dd:
  c=Dw()
  for v in registers.values():
   f=Dy()
   f.address=v.address
   c.append(f)
  I.device.__get_lock__()
  u=I.device.interface.ReadRegisters(c)
  I.device.__release_lock__()
  if I.device.interface.NoError==u:
   I.logger.info("Device register read success.")
   R={}
   for f in c:
    R[f.address]=f.data
   return R
  else:
   I.logger.error("Device register read failed with code %s.",u)
   return{}
 def qR(I,address,channel,g):
  I.__set_wire__(I.links.win_dac,address,DF.DAC_SEL)
  I.__set_wire__(I.links.win_dac,I.DAC_WRITE_MODE,DF.DAC_MODE)
  I.__set_wire__(I.links.win_dac,channel,DF.DAC_CHANNEL)
  I.__set_wire__(I.links.win_dac,g,DF.DAC_VALUE)
  I.__update_wires__()
  I.__set_trigger__(I.links.trig_in,Dt.TRIG_DAC)
 def qb(I,dacs):
  for b in dacs.values():
   I.qR(b.address,b.channel,b.value)
 def qw(I,address,channel)->DC:
  I.__set_wire__(I.links.win_adc,address,Da.ADC_ID)
  I.__set_wire__(I.links.win_adc,channel,Da.ADC_CHANNEL)
  I.__update_wires__()
  I.__set_trigger__(I.links.trig_in,Dt.TRIG_ADC)
  w=I.__wait_until(I.qy,1)
  if w:
   y=I.__read_wire__(I.links.wout_adc,DB.ADC_DATA)
  else:
   y=0
  return y
 def qy(I)->DO:
  T=I.__read_trigger__(I.links.trig_out,Dg.ADC_DATA_VALID)
  return T
 def qT(I):
  I.qC()
  I.qQ()
  I.__set_wire__(I.links.win0,1,Dk.WRITE_EN_RAM)
  I.__update_wires__()
  I.__set_trigger__(I.links.trig_in,Dt.START)
 def qY(I):
  I.__set_trigger__(I.links.trig_in,Dt.STOP)
 def qi(I)->DO:
  T=I.__read_trigger__(I.links.trig_out,Dg.VIDEO_DONE)
  return T
 def qO(I)->DO:
  T=I.__read_trigger__(I.links.trig_out,Dg.EVENTS_DONE)
  return T
 def qp(I):
  I.__set_wire_as_trigger__(I.links.win0,Dk.RESET_CHIP)
  I.__update_wires__()
 def qA(I):
  I.__set_wire_as_trigger__(I.links.win0,Dk.RESET_PERIPH)
  I.__update_wires__()
 def qd(I):
  I.__set_wire_as_trigger__(I.links.win0,Dk.RESET)
  I.__update_wires__()
 def qC(I):
  I.__set_wire__(I.links.win0,0,Dk.READ_EN_RAM)
  I.__set_wire__(I.links.win0,0,Dk.WRITE_EN_RAM)
  I.__set_wire_as_trigger__(I.links.win0,Dk.RESET_FIFO)
  I.__update_wires__()
 def qQ(I):
  I.__set_wire_as_trigger__(I.links.win0,Dk.RESET_RAM)
  I.__update_wires__()
 def qK(I):
  g=I.__read_wire__(I.links.wout_calib,DX.CALIB)
  if g==0:
   return DT
  else:
   return Dp
 def qE(I,is_enabled):
  if is_enabled:
   I.__set_wire__(I.links.win0,1,Dk.CLK_20M_EN)
  else:
   I.__set_wire__(I.links.win0,0,Dk.CLK_20M_EN)
  I.__update_wires__()
 def qh(I):
  Y=I.__read_wire__(I.links.wout_xy,DL.X)
  i=I.__read_wire__(I.links.wout_xy,DL.Y)
  return Y,i
 def qM(I,p):
  I.qC()
  I.qQ()
  O=I.__read_ram_block(p)
  I.__set_wire__(I.links.win0,0,Dk.READ_EN_RAM)
  I.__update_wires__()
  return O
 def qP(I,p):
  O=I.__read_ram_block(p)
  I.__set_trigger__(I.links.trig_in,Dt.EVENTS_READ)
  return O
 def __read_ram_block(I,p):
  I.__set_wire__(I.links.win0,1,Dk.READ_EN_RAM)
  I.__update_wires__()
  p=(p//16)*16
  A=0
  O=DQ()
  while A<p:
   d=DK([I.RAM_READBUF_SIZE,p])
   C=I.__read_block_pipe_out__(I.links.pipe_out0,d)
   O.extend(C)
   A=A+d
  return O
 def qr(I):
  Q=I.__read_wire__(I.links.wout_ram_read,DU.ADDR_RD)
  K=I.__read_wire__(I.links.wout_ram_write,DH.ADDR_WR)
  return Q,K
 def qz(I,data_tx):
  I.__write_serial_fifo(data_tx)
 def ql(I):
  E=I.__read_serial_fifo()
  return E
 def qm(I,is_enabled):
  if is_enabled:
   I.__set_wire__(I.links.win0,1,Dk.TEST_TFS_EN)
   I.__set_wire__(I.links.win0,1,Dk.CLK_TFS_EN)
   I.__update_wires__()
  else:
   I.__set_wire__(I.links.win0,0,Dk.TEST_TFS_EN)
   I.__set_wire__(I.links.win0,0,Dk.CLK_TFS_EN)
   I.__update_wires__()
 def qN(I,mode):
  I.__set_wire__(I.links.win0,mode,Dk.MODES)
  I.__update_wires__()
 def qJ(I,signal,g):
  if signal==0:
   I.__set_wire__(I.links.win0,g,Dk.AUX0)
  elif signal==1:
   I.__set_wire__(I.links.win0,g,Dk.AUX1)
  elif signal==2:
   I.__set_wire__(I.links.win0,g,Dk.AUX2)
  elif signal==3:
   I.__set_wire__(I.links.win0,g,Dk.AUX3)
  elif signal==4:
   I.__set_wire__(I.links.win0,g,Dk.AUX4)
  elif signal==5:
   I.__set_wire__(I.links.win0,g,Dk.AUX5)
  I.__update_wires__()
 def qx(I,switch_bit,g):
  if switch_bit==0:
   I.__set_wire__(I.links.win_pcb,g,De.BIT0)
  elif switch_bit==1:
   I.__set_wire__(I.links.win_pcb,g,De.BIT1)
  elif switch_bit==2:
   I.__set_wire__(I.links.win_pcb,g,De.BIT2)
  elif switch_bit==3:
   I.__set_wire__(I.links.win_pcb,g,De.BIT3)
  elif switch_bit==4:
   I.__set_wire__(I.links.win_pcb,g,De.BIT4)
  elif switch_bit==5:
   I.__set_wire__(I.links.win0,g,De.BIT5)
  I.__update_wires__()
 def qj(I)->DC:
  h=I.__read_wire__(I.links.wout_evt_count,DW.EVT_COUNT)
  return h
 def __write_serial_fifo(I,O):
  if O is not DY:
   M=DE(O) 
   O.reverse()
   I.__set_register__(I.links.reg_spi,M)
   I.__set_trigger__(I.links.trig_in,Dt.SERIAL_RX_RST_FIFO)
   while M>0:
    P=I.__read_wire__(I.links.wout0,DV.SERIAL_TX_FULL)
    while P:
     P=I.__read_wire__(I.links.wout0,DV.SERIAL_TX_FULL)
     Dv(0.01)
    if M>0:
     I.__set_wire__(I.links.win_spi,O[M-1],DG.BYTE3)
    if M>1:
     I.__set_wire__(I.links.win_spi,O[M-2],DG.BYTE2)
    if M>2:
     I.__set_wire__(I.links.win_spi,O[M-3],DG.BYTE1)
    if M>3:
     I.__set_wire__(I.links.win_spi,O[M-4],DG.BYTE0)
    I.__update_wires__()
    I.__set_trigger__(I.links.trig_in,Dt.SERIAL_TX_WEN)
    M=M-4
   I.logger.debug(f"{len(data)} bytes sent to the serial driver.")
   Dv(0.0005) 
  else:
   I.logger.error("Serial TX data is None.")
 def __read_serial_fifo(I):
  r=Dh()
  z=I.__read_wire__(I.links.wout0,DV.SERIAL_RX_EMPTY)
  if z:
   I.logger.error("No RX data found in serial fifo. Make sure the device is answering or delay is long enough.")
   return DY
  else:
   while not z:
    I.__set_trigger__(I.links.trig_in,Dt.SERIAL_RX_REN)
    l=I.__read_wire__(I.links.wout0,DV.SERIAL_RX_BYTE)
    r.append(l)
    z=I.__read_wire__(I.links.wout0,DV.SERIAL_RX_EMPTY)
   I.logger.debug(f"{len(data_read)} bytes read from the serial driver.")
   return r
 def __set_trigger__(I,address,trigger):
  I.device.__get_lock__()
  k=I.device.interface.ActivateTriggerIn(address,trigger.offset)
  I.device.__release_lock__()
  I.__check_err_code(k,f"Activate trigger address {address} bit {trigger.offset}")
 def __read_trigger__(I,address,trigger):
  I.device.__get_lock__()
  k=I.device.interface.UpdateTriggerOuts()
  I.__check_err_code(k,"Update trigger out")
  T=I.device.interface.IsTriggered(address,trigger.mask)
  I.device.__release_lock__()
  return T
 def __set_wire_as_trigger__(I,address,wire):
  I.__set_wire__(address,1,wire)
  I.__update_wires__()
  I.__set_wire__(address,0,wire)
  I.__update_wires__()
 def __read_wire__(I,address,wire):
  I.device.__get_lock__()
  k=I.device.interface.UpdateWireOuts()
  I.__check_err_code(k,f"Read wire out {address}")
  m=I.device.interface.GetWireOutValue(address)
  I.device.__release_lock__()
  return(m&wire.mask)>>wire.offset
 def __set_wire__(I,address,g,wire):
  I.device.__get_lock__()
  N=g<<wire.offset
  k=I.device.interface.SetWireInValue(address,N,wire.mask)
  I.device.__release_lock__()
  I.__check_err_code(k,f"Set wire -> bits {format(to_write_value, '#032b')} -> mask {format(wire.mask,'#032b')} in address {address}",)
 def __update_wires__(I):
  I.device.__get_lock__()
  k=I.device.interface.UpdateWireIns()
  I.device.__release_lock__()
  I.__check_err_code(k,"Update wire in")
 def __read_block_pipe_out__(I,address,length):
  J=DQ(length)
  I.device.__get_lock__()
  k=I.device.interface.ReadFromBlockPipeOut(address,I.RAM_BLOCK_SIZE,J)
  I.device.__release_lock__()
  if k<0:
   I.__check_err_code(k,f"Read pipe block with address {address}")
  else:
   I.logger.debug(f"Query {length} bytes \t Read {err_code} bytes")
  return J
 def __set_register__(I,address,g):
  I.device.__get_lock__()
  k=I.device.interface.WriteRegister(address,g)
  I.device.__release_lock__()
  I.__check_err_code(k,f"Writing register address {address} value {value}")
 def __check_err_code(I,k,msg=""):
  if k!=I.device.interface.NoError:
   I.logger.error(msg+f" failed with code({err_code}).")
   I.logger.error(f"Opal kelly error message: {self.device.interface.GetLastErrorMessage()}")
  else:
   I.logger.debug(msg+" OK.")
 def __wait_until(I,somepredicate,e,period=0.01,*args,**kwargs):
  x=Df()+e
  while Df()<x:
   if somepredicate(*args,**kwargs):
    return Dp
   Dv(period)
  return DT
class L:
 def __init__(I)->DY:
  I.win0=0x00
  I.win_spi=0x01
  I.win_adc=0x02
  I.win_pcb=0x03
  I.win_dac=0x04
  I.reg_spi=0x08
  I.wout_calib=0x20
  I.wout0=0x21
  I.wout_xy=0x22
  I.wout_adc=0x23
  I.wout_evt_count=0x27
  I.wout_ram_read=0x28
  I.wout_ram_write=0x29
  I.trig_in=0x41
  I.trig_out=0x60
  I.pipe_out0=0xA0
class Dq:
 def __init__(I,s,end=0)->DY:
  if j!=0:
   I.size=j-s+1
  else:
   I.size=1
  I.offset=s
  I.mask=(DM(2,I.size)-1)<<s
class Dn(Dq):
 def __init__(I,s)->DY:
  DP().__init__(s)
class Dk:
 S=Dq(0)
 o=Dq(1)
 Iq=Dq(2)
 ID=Dq(3)
 In=Dq(4)
 Ik=Dq(5)
 Ie=Dq(7)
 IG=Dq(8)
 Ia=Dq(9)
 IF=Dq(10)
 IX=Dq(20)
 IV=Dq(21)
 IB=Dq(22)
 IW=Dq(23)
 IU=Dq(24)
 IH=Dq(25)
 IL=Dq(26)
 It=Dq(27)
 Ig=Dq(29,31)
class De:
 Ic=Dq(0)
 Iv=Dq(1)
 If=Dq(2)
 Iu=Dq(3)
 IR=Dq(4)
 Ib=Dq(5)
 Iw=Dq(6)
class DG:
 Iy=Dq(0,7)
 IT=Dq(8,15)
 IY=Dq(16,23)
 Ii=Dq(24,31)
 IO=Dq(0,31)
class Da:
 Ip=Dq(0,1)
 IA=Dq(2,3)
class DF:
 Id=Dq(0,11)
 IC=Dq(12,13)
 IQ=Dq(14,15)
 IK=Dq(16,17)
class DX:
 IE=Dq(0)
class DV:
 Ih=Dq(0,7)
 IM=Dq(8)
 IP=Dq(10)
 Ir=Dq(9)
class DB:
 Iz=Dq(0,11)
class DW:
 Il=Dq(0,31)
class DU:
 Im=Dq(0,31)
class DH:
 IN=Dq(0,31)
class DL:
 X=Dq(0,15)
 Y=Dq(16,31)
class Dt:
 IJ=Dn(0)
 Ix=Dn(1)
 Ij=Dn(2)
 Is=Dn(3)
 IS=Dn(4)
 Io=Dn(5)
 qI=Dn(6)
 qD=Dn(7)
class Dg:
 qn=Dn(0)
 qk=Dn(1)
 qe=Dn(2)
 qG=Dn(3)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
