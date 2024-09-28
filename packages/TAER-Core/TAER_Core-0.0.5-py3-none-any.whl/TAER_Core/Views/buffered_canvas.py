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
t=None
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
Y=wx.Bitmap
l=wx.BufferedPaintDC
e=wx.MemoryDC
C=wx.EVT_ERASE_BACKGROUND
D=wx.EVT_SIZE
O=wx.EVT_PAINT
A=wx.NO_FULL_REPAINT_ON_RESIZE
s=wx.DefaultSize
L=wx.DefaultPosition
m=wx.Panel
class F(m):
 buffer=t
 z=t
 def __init__(i,parent,ID=-1,pos=L,size=s,style=A,):
  m.__init__(i,parent,ID,pos,size,style)
  i.Bind(O,i.d)
  i.Bind(D,i.g)
  def h(*pargs,**kwargs):
   pass 
  i.Bind(C,h)
  i.g(t)
 def R(i,dc):
  pass
 def P(i):
  i.buffer,i.backbuffer=i.backbuffer,i.buffer
  i.Refresh()
 def r(i):
  dc=e()
  dc.SelectObject(i.backbuffer)
  i.R(dc)
  i.P()
 def d(i,event):
  dc=l(i,i.buffer)
  del dc
 def g(i,event):
  G,j=i.GetClientSize()
  if G==0:
   G=1
  if j==0:
   j=1
  i.buffer=Y(G,j)
  i.backbuffer=Y(G,j)
  i.r()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
