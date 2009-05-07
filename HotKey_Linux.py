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
import gobject
import sys
import os
import time
from threading import Thread

class KeyHook(Thread):
    '''Key hook for global hotkey.
    
    '''
    def __init__(self, function, hotkey=()):
        Thread.__init__(self)
        self.function = function
        self.hotkey = hotkey        
        self.exit= False
        
    def run(self):
        while not self.exit:
            if os.path.exists("/tmp/plaunch_lock"):
#                print "hotkey get"
                self.function()
                os.remove("/tmp/plaunch_lock")
            else:
                time.sleep(0.1)  
    def stop(self):
        self.exit = True
    
if __name__ == '__main__':
    gobject.threads_init()
    test = KeyHook(lambda: sys.stdout.write('hotkey\n'))
    try:
        test.start()
    except KeyboardInterrupt:
        print 'Test over'
    test.exit = True
