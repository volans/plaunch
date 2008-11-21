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
import gobject
import sys
import subprocess

from ShortCutsLoader import ShortCutsLoader

GLADE = sys.path[0] + '/data/PLaunch.glade'
SHORTCUTS_CONF = sys.path[0] + '/data/ShortCutList.txt'
(COLUMN_NUM, COLUMN_SHORTCUT, COLUMN_DISCRIPTION) = range(3)

class MainDialog:
    '''MainDialog for user input, show shortcuts...

    '''
    def __init__(self):
        self.xml = glade.XML(GLADE)
        self.win = self.xml.get_widget('PLaunch')
        self.xml.signal_autoconnect(self)

        self.win.connect("delete_event", self.on_close_main)
        self.win.set_keep_above(True)

        self.scm = ShortCutsLoader(file(SHORTCUTS_CONF).readlines()[1:])
        self.list = self.__create_list() 
        self.tv = self.__create_treeview()
        self.__update_tree()

        #self.win.show_all()
        #self.win.present()

    def __create_list(self):
        list = gtk.ListStore(gobject.TYPE_UINT,
                             gobject.TYPE_STRING,
                             gobject.TYPE_STRING,
                             )

        return list

    def __create_treeview(self):
        tv = self.xml.get_widget('shortcutTree')
        selection = tv.get_selection()
        selection.set_mode(gtk.SELECTION_BROWSE)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn(u'Number',
                renderer,
                text=COLUMN_NUM)
        tv.append_column(col)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn(u'Shortcuts',
                renderer,
                text=COLUMN_SHORTCUT)
        tv.append_column(col)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn(u'Discription',
                renderer,
                text=COLUMN_DISCRIPTION)
        tv.append_column(col)

        return tv

    def __update_tree(self):
        '''Updated tree view of shortcuts after user input modification.
        ''' 
        self.list.clear()
        for key, cmd in self.scm.shortcutmatch.items():
            self.list.set(self.list.append(),
                            0, key,
                            1, cmd,
                            2, self.scm.shortcutspool[cmd][1]
                         )
        self.tv.set_model(self.list)

        selection = self.tv.get_selection()
        selection.select_path(0)

    def on_select_shortcut(self, tv, column_number, column):
        '''Get command from command pool.
        Create a new process to run this command.
        '''
        command = self.scm.shortcutspool[self.scm.shortcutmatch[column_number[0]]][0]
        subprocess.Popen(command, shell=True)

        # clear input
        entryinput = self.xml.get_widget('userInput')
        entryinput.set_text('')
        self.on_close_main(None)
        return True

    def on_userInput_key_press_event(self, widget, key):
        '''Catch the Enter key
        '''
        if key.keyval == 65293: # Enter
            self.on_select_shortcut(None, (0,), None)
        elif key.keyval == 65307: # Esc
            entryinput = self.xml.get_widget('userInput')
            entryinput.set_text('')
            self.on_close_main(None)

    def on_userInput_changed(self, widget, data=None):
        input = widget.get_text()
        self.scm.flush_input(input)
        self.__update_tree()

    def on_close_main(self, widget, data=None):
        self.win.hide_all()
        return True

    def open_main(self):
        self.win.show_all()
        self.win.present()
        #return True

if __name__ == '__main__':
    class Test(MainDialog):
        def on_close_main(self, widget, data=None):
            gtk.main_quit()
    test = Test()
    test.win.show_all()
    test.win.present()
    gtk.main()
