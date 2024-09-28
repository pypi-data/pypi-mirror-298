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
H=None
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
q=wx.Bitmap
h=wx.BufferedPaintDC
S=wx.MemoryDC
E=wx.EVT_ERASE_BACKGROUND
l=wx.EVT_SIZE
X=wx.EVT_PAINT
M=wx.NO_FULL_REPAINT_ON_RESIZE
K=wx.DefaultSize
J=wx.DefaultPosition
y=wx.Panel
class o(y):
 buffer=H
 s=H
 def __init__(w,parent,ID=-1,pos=J,size=K,style=M,):
  y.__init__(w,parent,ID,pos,size,style)
  w.Bind(X,w.W)
  w.Bind(l,w.U)
  def r(*pargs,**kwargs):
   pass 
  w.Bind(E,r)
  w.U(H)
 def t(w,dc):
  pass
 def N(w):
  w.buffer,w.backbuffer=w.backbuffer,w.buffer
  w.Refresh()
 def V(w):
  dc=S()
  dc.SelectObject(w.backbuffer)
  w.t(dc)
  w.N()
 def W(w,event):
  dc=h(w,w.buffer)
  del dc
 def U(w,event):
  R,v=w.GetClientSize()
  if R==0:
   R=1
  if v==0:
   v=1
  w.buffer=q(R,v)
  w.backbuffer=q(R,v)
  w.V()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
