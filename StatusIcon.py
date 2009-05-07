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
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade as glade
import sys

from MainDialog import MainDialog
from ShortCutsEditer import ShortCutsEditer


GLADE = sys.path[0] + '/data/PLaunch.glade'
ICON = sys.path[0] + '/data/PLaunch.ico'

class PLaunchStatusIcon(gtk.StatusIcon):
    '''Plaunch statusIcon, It show always in system tray.

    '''
    def __init__(self):
        gtk.StatusIcon.__init__(self)
        menu = '''
            <ui>
             <menubar name="PLaunch">
              <menu action="Menu">
               <menuitem action="Show"/>
               <menuitem action="Config"/>
               <menuitem action="About"/>
               <menuitem action="Exit"/>
              </menu>
             </menubar>
            </ui>
        '''

        actions = [
            ('Menu',  None, 'Menu'),
            ('Show', gtk.STOCK_EXECUTE, '_Show...', None, None, self.on_activate),
            ('Config', gtk.STOCK_EDIT, '_Shortcuts...', None, None, self.on_edit_shortcut),
            ('About', gtk.STOCK_ABOUT, '_About...', None, None, self.on_about),
            ('Exit', gtk.STOCK_CLOSE, '_Exit...', None, None, self.on_exit_event)]


        ag = gtk.ActionGroup('Actions')
        ag.add_actions(actions)
        self.manager = gtk.UIManager()
        self.manager.insert_action_group(ag, 0)
        self.manager.add_ui_from_string(menu)
        self.menu = self.manager.get_widget('/PLaunch/Menu/About').props.parent
        self.set_from_file(ICON)
        self.set_tooltip('PLaunch is running here')
        self.set_visible(True)
        self.connect('activate', self.on_activate)
        self.connect('popup-menu', self.on_popup_menu)
        self.maindialog = MainDialog()


    def on_popup_menu(self, status, button, time):
        self.menu.popup(None, None, None, button, time)
    
    def on_activate(self, data):
        self.maindialog.open_main()

    def on_edit_shortcut(self, widget):
        ShortCutsEditer() 

    def on_about(self, widget):
        xml = glade.XML(GLADE)
        about = xml.get_widget('aboutplaunch')
        about.run()
        about.destroy()

    def on_exit_event(self, widget, data=None):
        gtk.main_quit()
        return False

if __name__ == '__main__':
    test = PLaunchStatusIcon()
    gtk.main()

    
