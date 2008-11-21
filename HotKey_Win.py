#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#    PLaunch - Shortcuts management tool, base on pyton/pygtk/pyxlib
#
#    Copyright (C) 2008 Volans  <volansw@gmail.com>
#
#    PLaunch is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 2 of the License, or (at your 
# option) any later version.  
#
#    PLaunch is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License 
# for more details.  
#
#    You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.   
#-------------------------------------------------------------------------------
import gtk
import gobject
import sys
import win32con
import pyHook 
import ctypes

class KeyHook:
    '''Key hook to catch global Hotkey.

    '''
    def __init__(self, function, 
            hotkey={'hotkey' : win32con.MOD_ALT, 'modifiers': ord('R')}):
        self.function = function
        self.register_hotkey(1, hotkey)

        # start key Hook
        hm = pyHook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent
        hm.HookKeyboard()

    def OnKeyboardEvent(self, event):
        if event.Alt and event.Key == 'R':
            self.function()

        # return True to pass the event to other handlers
        # return False to stop the event from propagating
        return True

    def register_hotkey(self, id, hotkey):
        byref = ctypes.byref
        user32 = ctypes.windll.user32

        if not user32.RegisterHotKey(None,
                                    id,
                                    hotkey['hotkey'],
                                    hotkey['modifiers']):
            print"Unable to register hotkey"
