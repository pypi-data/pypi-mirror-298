import wx
ށ=super
𐲓=wx.LEFT
ﱲ=wx.ALIGN_RIGHT
ݮ=wx.ALIGN_CENTER_VERTICAL
泱=wx.TOP
𐒳=wx.ALIGN_CENTER
ﴝ=wx.GridSizer
𐩦=wx.ID_ANY
𰺳=wx.Button
𨣒=wx.TE_READONLY
𐿠=wx.TE_CENTER
ݝ=wx.TextCtrl
𥋳=wx.CENTER
𐴗=wx.StaticText
ﰄ=wx.Panel
𩕫=wx.EXPAND
ڊ=wx.ALL
ﱽ=wx.HORIZONTAL
𑱵=wx.VERTICAL
ﳟ=wx.BoxSizer
𘄙=wx.NullColour
ﻶ=wx.Size
𠿜=wx.MAXIMIZE_BOX
诐=wx.RESIZE_BORDER
𠫳=wx.DEFAULT_FRAME_STYLE
from TAER_Core.Views.auxiliar_view_base import AuxViewBase
class 𞸇(AuxViewBase):
 def __init__(𞠒,ߥ):
  ށ().__init__(parent=ߥ,title="SERIAL debugger",style=𠫳^诐^𠿜,)
  𞠒.SetMinSize(ﻶ(0,0))
  𞠒.__create_layout()
 def __create_layout(𞠒):
  𞠒.SetBackgroundColour(𘄙)
  𞠒.vsizer=ﳟ(𑱵)
  𞠒.hsizer=ﳟ(ﱽ)
  𞠒.vsizer.Add(𞠒.hsizer,0,ڊ,5)
  𞠒.panel_serial_control=ﴡ(𞠒)
  𞠒.hsizer.Add(𞠒.panel_serial_control,0,𩕫)
  𞠒.SetSizerAndFit(𞠒.vsizer)
  𞠒.Layout()
class ﴡ(ﰄ):
 def __init__(𞠒,ߥ):
  ﰄ.__init__(𞠒,ߥ)
  𞠒.__create_layout()
 def __create_layout(𞠒):
  뗣=𐴗(𞠒,label="SERIAL TX data",style=𥋳)
  𞠒.serial_tx_box=ݝ(𞠒,value="",style=𐿠)
  𞸈=𐴗(𞠒,label="SERIAL RX data",style=𥋳)
  𞠒.serial_rx_box=ݝ(𞠒,value="",style=𐿠|𨣒)
  𞠒.btn_write=𰺳(𞠒,𐩦,"Write SERIAL")
  𞠒.vsizer=ﳟ(𑱵)
  𞠒.main_grid=ﴝ(2,0,0)
  𞠒.main_grid.Add(뗣,0,𐒳|泱,5)
  𞠒.main_grid.Add(𞠒.serial_tx_box,0,ݮ|ﱲ|𐲓|泱,5,)
  𞠒.main_grid.Add(𞸈,0,𐒳|泱,5)
  𞠒.main_grid.Add(𞠒.serial_rx_box,0,ݮ|ﱲ|𐲓|泱,5,)
  𞠒.vsizer.Add(𞠒.main_grid,0,ڊ,1)
  𞠒.vsizer.Add(𞠒.btn_write,0,ﱲ|ڊ,5)
  𞠒.SetSizer(𞠒.vsizer)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
