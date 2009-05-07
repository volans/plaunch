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
from StatusIcon import PLaunchStatusIcon
import gtk
import gobject
import thread
import sys

PROCESS = 'PLaunch'

def main_linux():
    try:
        import dl
        libc = dl.open('/lib/libc.so.6')
        libc.call('prctl', 15, PROCESS, 0, 0, 0)
    except:
        quit() 
    from HotKey_Linux import KeyHook
    gobject.threads_init()
    statusicon = PLaunchStatusIcon()
    hotkey = KeyHook(statusicon.maindialog.open_main)   
    thread.start_new_thread(hotkey.start, ())
    try:
        gtk.main()
    except KeyboardInterrupt:
        print 'User Cancled.'
    hotkey.stop()

def main_windows():
    from HotKey_Win import KeyHook
    statusicon = PLaunchStatusIcon()
    hotkey = KeyHook(statusicon.maindialog.open_main)
    gtk.main()


if __name__ == '__main__':
    if sys.platform == 'win32':
        main = main_windows
    else:
        main = main_linux
    main()
