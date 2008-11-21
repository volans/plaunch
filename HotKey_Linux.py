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
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq


class KeyHook:
    '''Key hook to catch global Hotkey.

    '''
    def __init__(self, function, hotkey=(XK.XK_Alt_L, XK.XK_r)):
        self.function = function
        self.hotkey = hotkey
        self.keystatus = {1:0,2:0}
        self.record_dpy = display.Display()
        self.exit= False
        self.ctx = self.record_dpy.record_create_context(
            0,
            [record.AllClients],
            [{
                    'core_requests': (0, 0),
                    'core_replies': (0, 0),
                    'ext_requests': (0, 0, 0, 0),
                    'ext_replies': (0, 0, 0, 0),
                    'delivered_events': (0, 0),
                    'device_events': (X.KeyPress, X.MotionNotify),
                    'errors': (0, 0),
                    'client_started': False,
                    'client_died': False,
            }])

    def __callback(self, reply):
        gtk.gdk.threads_enter()
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            #print "* received swapped protocol data, cowardly ignored"
            return
        if not len(reply.data) or ord(reply.data[0]) < 2:
            # not an event
            return

        data = reply.data
        event, data = rq.EventField(None).parse_binary_value(
                data, 
                self.record_dpy.display, 
                None, 
                None)
    
        if event.type in [X.KeyPress, X.KeyRelease]:
            keysym = self.record_dpy.keycode_to_keysym(event.detail, 0)
            if event.type == X.KeyPress:
                if keysym == self.hotkey[0]: #XK.XK_Alt_L:
                    self.keystatus[1] = 1
                elif keysym == self.hotkey[1]: # XK.XK_r:
                    self.keystatus[2] = 1
            else:
                if keysym == self.hotkey[0]: #XK.XK_Alt_L:
                    self.keystatus[1] = 0
                elif keysym == self.hotkey[1]: #XK.XK_r:
                    self.keystatus[2] = 0
            #print   self.keystatus 
            if self.keystatus[1] == self.keystatus[2] == 1:
                self.function()
        gtk.gdk.threads_leave()

    def check_hotkey(self, flag):
        if flag == True:
            self.function()

    def stop(self):
        self.record_dpy.record_disable_context(self.ctx)
        self.record_dpy.flush()
        self.record_dpy.record_free_context(self.ctx)

    def start(self):
        self.record_dpy.record_enable_context(self.ctx, self.__callback)



if __name__ == '__main__':
    gobject.threads_init()
    import sys
    test = KeyHook(lambda: sys.stdout.write('hotkey\n'))
    try:
        test.start()
    except KeyboardInterrupt:
        print 'Test over'
    test.exit = True
    test.stop()
