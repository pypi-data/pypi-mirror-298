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
w=None
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
class u(wx.Panel):
 buffer=w
 f=w
 def __init__(V,parent,ID=-1,pos=wx.DefaultPosition,size=wx.DefaultSize,style=wx.NO_FULL_REPAINT_ON_RESIZE,):
  wx.Panel.__init__(V,parent,ID,pos,size,style)
  V.Bind(wx.EVT_PAINT,V.onPaint)
  V.Bind(wx.EVT_SIZE,V.onSize)
  def d(*pargs,**kwargs):
   pass 
  V.Bind(wx.EVT_ERASE_BACKGROUND,d)
  V.onSize(w)
 def y(V,dc):
  pass
 def n(V):
  V.buffer,V.backbuffer=V.backbuffer,V.buffer
  V.Refresh()
 def g(V):
  dc=wx.MemoryDC()
  dc.SelectObject(V.backbuffer)
  V.draw(dc)
  V.flip()
 def l(V,event):
  dc=wx.BufferedPaintDC(V,V.buffer)
  del dc
 def i(V,event):
  t,k=V.GetClientSize()
  if t==0:
   t=1
  if k==0:
   k=1
  V.buffer=wx.Bitmap(t,k)
  V.backbuffer=wx.Bitmap(t,k)
  V.update()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
