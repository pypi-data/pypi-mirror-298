"""
BufferedCanvas -- Double-buffered, flicker-free canvas widget
Copyright (C) 2005, 2006 Daniel Keep
To use this widget, just override or replace the draw method.
This will be called whenever the widget size changes, or when
the update method is explicitly called.
Please submit any improvements/bugfixes/ideas to the following
url:
  http://wiki.wxpython.org/index.cgi/BufferedCanvas
2006-04-29: Added bugfix for a crash on Mac provided by Marc Jans.
"""
ﶒ=None
__author__="Daniel Keep <daniel.keep.sp4msux0rz@gmail.com>"
__license__="""
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 2.1 of the
License, or (at your option) any later version.
As a special exception, the copyright holders of this library
hereby recind Section 3 of the GNU Lesser General Public License. This
means that you MAY NOT apply the terms of the ordinary GNU General
Public License instead of this License to any given copy of the
Library. This has been done to prevent users of the Library from being
denied access or the ability to use future improvements.
This library is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
"""
__all__=["BufferedCanvas"]
import wx
𧻘=wx.Bitmap
𬢵=wx.BufferedPaintDC
ﭻ=wx.MemoryDC
𐢑=wx.EVT_ERASE_BACKGROUND
𞤚=wx.EVT_SIZE
ޟ=wx.EVT_PAINT
ﮘ=wx.NO_FULL_REPAINT_ON_RESIZE
ﶗ=wx.DefaultSize
𱁳=wx.DefaultPosition
ﲽ=wx.Panel
class 𞤊(ﲽ):
 buffer=ﶒ
 𖢋=ﶒ
 def __init__(𐬛,parent,ID=-1,pos=𱁳,size=ﶗ,style=ﮘ,):
  ﲽ.__init__(𐬛,parent,ID,pos,size,style)
  𐬛.Bind(ޟ,𐬛.𪬶)
  𐬛.Bind(𞤚,𐬛.𡨱)
  def ቂ(*pargs,**kwargs):
   pass 
  𐬛.Bind(𐢑,ቂ)
  𐬛.𡨱(ﶒ)
 def ﻩ(𐬛,ﮡ):
  pass
 def 𞤥(𐬛):
  𐬛.buffer,𐬛.backbuffer=𐬛.backbuffer,𐬛.buffer
  𐬛.Refresh()
 def 傸(𐬛):
  ﮡ=ﭻ()
  ﮡ.SelectObject(𐬛.backbuffer)
  𐬛.ﻩ(ﮡ)
  𐬛.𞤥()
 def 𪬶(𐬛,event):
  ﮡ=𬢵(𐬛,𐬛.buffer)
  del ﮡ
 def 𡨱(𐬛,event):
  ݵ,𫘘=𐬛.GetClientSize()
  if ݵ==0:
   ݵ=1
  if 𫘘==0:
   𫘘=1
  𐬛.buffer=𧻘(ݵ,𫘘)
  𐬛.backbuffer=𧻘(ݵ,𫘘)
  𐬛.傸()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
