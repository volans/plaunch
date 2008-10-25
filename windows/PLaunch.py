#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
#   Copyright (c) 2008, Volans Wang <volansw@gmail.com> All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above copyright
#         notice, this list of conditions and the following disclaimer in the
#         documentation and/or other materials provided with the distribution.
#       * Neither the name of the <organization> nor the
#         names of its contributors may be used to endorse or promote products
#         derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#   FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#   COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#   (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#   HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#   STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#   OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade as glade
import gobject
import os
import subprocess
import thread
import win32con
import ctypes
from ctypes import wintypes
import pyHook

class ShortcutsManagement:
    '''Manage all short cuts,

    including Keys/discription/command and input matching

    Construction:
        conf: short config file

    Data structure:
        self.shortcutspool data structrue: {shortcut: [ command, discription]}
            {'command': ['cmd', 'Terminal']}

        self.shortcutmatch data structure: {number: shortcut}
            {0: 'cmmand'; 1: 'mycomputer'}
    '''
    def __init__(self, conf):
        self.input = ''
        self.shortcutspool = {}
        self.shortcutmatch = {}
        self.shortcuttop10 = {}

        for line in conf:
            line = line.split(',')
            self.shortcutspool[line[0]] = [line[2].replace('\n',''), line[1]]

        i = 0
        for line in conf:
            line = line.split(',')
            self.shortcutmatch[i] = line[0]
            i += 1
            if i > 9:
                break
        self.shortcuttop10 = self.shortcutmatch

    def flush_input(self, input):
        '''Flush self.shortcutmatch base on input.
        If more than 10 matched items, only got the first 10 items.
        '''

        if not input:
            self.shortcutmatch = self.shortcuttop10
            return

        if input in ['0','1','2','3','4','5','6','7','8','9']:
            tmp = self.shortcutmatch[int(input)]
            self.shortcutmatch = {}
            self.shortcutmatch[0] = tmp
            return

        tmp = {0:[]}
        for item in self.shortcutspool.keys():
            try:
                index=item.index(input)
            except ValueError:
                continue

            if tmp.has_key(index):
                tmp[index].append(item)
            else:
                tmp[index] = [item]

        self.shortcutmatch = {}
        j = 0 # match number
        for i in range(10):
            if not tmp.has_key(i):
                continue

            for item in tmp[i]:
                self.shortcutmatch[j] = item
                j += 1


class MainDialog:
    '''MainDialog for user input, show shortcuts...

    '''
    def __init__(self):
        xml = self.xml = glade.XML('PLaunch.glade')
        win = self.win = xml.get_widget('PLaunch')
        xml.signal_autoconnect(self) # it is very important

        if win:
            win.connect("delete_event", self.on_close_main)
            win.set_size_request( 400, 300 )

        list = self.list = gtk.ListStore(gobject.TYPE_UINT,
                                        gobject.TYPE_STRING,
                                        gobject.TYPE_STRING)
        self.scm = ShortcutsManagement(file('ShortCutList.txt').readlines()[1:])
        self.list = gtk.ListStore( gobject.TYPE_UINT,
                                    gobject.TYPE_STRING,
                                    gobject.TYPE_STRING )
        self.tv = xml.get_widget('shortcutTree')


        selection = self.tv.get_selection()
        selection.set_mode(gtk.SELECTION_BROWSE)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Number', renderer, text=0)
        col.set_sort_column_id(0)
        col.set_clickable(False)
        self.tv.append_column(col)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Shortcuts', renderer, text=1)
        col.set_sort_column_id(1)
        col.set_clickable(False)
        self.tv.append_column(col)

        renderer = gtk.CellRendererText()
        col = gtk.TreeViewColumn('Name', renderer, text=2)
        col.set_sort_column_id(2)
        col.set_clickable(False)
        self.tv.append_column(col)

        self.update_tree()


    def update_tree(self):

        self.list.clear()
        for key, cmd in self.scm.shortcutmatch.items():
            self.list.set(self.list.append(),
                            0, key,
                            1, cmd,
                            2, self.scm.shortcutspool[cmd][1]
                         )

        self.tv.__init__(self.list)

        selection = self.tv.get_selection()
        selection.select_path(0)

    def on_select_shortcut(self, tv, column_number, column):
        '''Get command from command pool.
        Create a new process to run this command.
        '''
        command = self.scm.shortcutspool[self.scm.shortcutmatch[column_number[0]]][0]
        subprocess.Popen(command)

        #clear input
        entryinput = self.xml.get_widget('userInput')
        entryinput.set_text('')
        self.win.hide_all()
        return True

    def on_userInput_key_press_event(self, widget, key):
        '''Catch the Enter key
        '''
        if key.keyval == 65307: # Esc
            entryinput = self.xml.get_widget('userInput')
            entryinput.set_text('')
            self.win.hide_all()
            return True
        if key.keyval == 65293: # Enter
            self.on_select_shortcut(None, (0,), None)

    def on_userInput_changed(self, widget, data=None):

        input = widget.get_text()
        self.scm.flush_input(input)
        self.update_tree()

    def on_close_main(self, widget, data=None):
        self.win.hide_all()
        return True

    def open_main(self):
        self.win.show_all()
        return True


class PLaunch(gtk.StatusIcon):
    '''AltRun statusIcon, It show always in system tray.

    '''
    def __init__(self):
        gtk.StatusIcon.__init__(self)
        menu = '''
            <ui>
             <menubar name="PLaunch">
              <menu action="Menu">
               <menuitem action="Show"/>
               <menuitem action="ShortCut"/>
               <menuitem action="Config"/>
               <menuitem action="About"/>
               <menuitem action="Exit"/>
              </menu>
             </menubar>
            </ui>
        '''

        actions = [
            ('Menu',  None, 'Menu'),
            ('Show', gtk.STOCK_EXECUTE, '_Show...', None, 'Open the PLaunch', self.on_activate),
            ('ShortCut', gtk.STOCK_PREFERENCES, '_ShortCut...', None, 'Modify shortcuts', self.on_edit_shortcut),
            ('Config', gtk.STOCK_EDIT, '_Config...', None, 'Config PLaunch', self.on_config),
            ('Exit', gtk.STOCK_CLOSE, '_Exit...', None, 'Exit and Close', self.on_exit_event),
            ('About', gtk.STOCK_ABOUT, '_About...', None, 'About PLaunch', self.on_about)]

        ag = gtk.ActionGroup('Actions')
        ag.add_actions(actions)
        self.manager = gtk.UIManager()
        self.manager.insert_action_group(ag, 0)
        self.manager.add_ui_from_string(menu)
        self.menu = self.manager.get_widget('/PLaunch/Menu/About').props.parent
        self.set_from_file('PLaunch.ico')
        self.set_tooltip('PLaunch is running here')
        self.set_visible(True)
        self.connect('activate', self.on_activate)
        self.connect('popup-menu', self.on_popup_menu)

        self.maindialog = MainDialog()

        # Register Hotkey to windows
        hotkey = {'hotkey' : win32con.MOD_ALT, 'modifiers': ord('R')}
        self.register_hotkey(1, hotkey)

        # start key Hook
        hm = pyHook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent
        hm.HookKeyboard()


    def OnKeyboardEvent(self, event):
        if event.Alt and event.Key == 'R':
            self.on_activate(None)

        # return True to pass the event to other handlers
        # return False to stop the event from propagating
        return True


    def register_hotkey(self, id, hotkey):
        byref = ctypes.byref
        user32 = ctypes.windll.user32


        user32 = ctypes.windll.user32
        if not user32.RegisterHotKey(None,
                                    id,
                                    hotkey['hotkey'],
                                    hotkey['modifiers']):
            print"Unable to register hotkey"


    def on_popup_menu(self, status, button, time):
        self.menu.popup(None, None, None, button, time)

    def on_activate(self, data):
        # self.window.show_all()
        self.maindialog.open_main()

    def on_edit_shortcut(self):
        pass

    def on_config(self):
        pass

    def on_about(self, widget):
        xml = glade.XML('PLaunch.glade')
        about = xml.get_widget('aboutplaunch')
        about.run()
        about.destroy()

    def on_exit_event(self, widget, data=None):
        gtk.main_quit()
        return False

if __name__ == '__main__':
	PLaunch()
	gtk.main()
