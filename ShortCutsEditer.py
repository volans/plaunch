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

(COLUMN_SHORTCUT, COLUMN_DISCRIPTION, COLUMN_COMMAND, COLUMN_EDITABLE) = range(4)
TITLE = [u'Shortcut', u'Discription', u'Command']

GLADE = sys.path[0] + '/data/PLaunch.glade'
SHORTCUTS_CONF = sys.path[0] + '/data/ShortCutList.txt'

class ShortCutsEditer:
    '''UI interface for user to modify shortcuts list.
    With this window, user do not need to modify ShortCutsList.txt.
    '''

    def __init__(self):
        xml = self.xml = glade.XML(GLADE)
        self.win = self.xml.get_widget('ShotcutsConf')
        self.win.connect('delete_event', lambda _,__: self.win.destroy())
        self.xml.signal_autoconnect(self)
        self.shortcut_pool = file(SHORTCUTS_CONF).readlines()[1:]
        self.list = self.__create_list() 
        self.tv = self.__create_treeview()
        self.tv.set_model(self.list)

        selection = self.tv.get_selection()
        selection.select_path(0)

        self.win.show_all()
    
    def __create_list(self):
        list = gtk.ListStore(gobject.TYPE_STRING,
                             gobject.TYPE_STRING,
                             gobject.TYPE_STRING,
                             gobject.TYPE_BOOLEAN,
                             )

        for item in self.shortcut_pool:
            item = item.replace('\n','').split(',')
            list.set(list.append(),
                     COLUMN_SHORTCUT, item[0],
                     COLUMN_DISCRIPTION, item[1],
                     COLUMN_COMMAND, item[2],
                     COLUMN_EDITABLE, True
                     )
        return list

    def __create_treeview(self):
        tv = self.xml.get_widget('ShortCutsPool')
        selection = tv.get_selection()
        selection.set_mode(gtk.SELECTION_BROWSE)

        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_edited, tv)
        col = gtk.TreeViewColumn(TITLE[0], 
                renderer, 
                text=COLUMN_SHORTCUT, 
                editable=COLUMN_EDITABLE)
        tv.append_column(col)

        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_edited, tv)
        col = gtk.TreeViewColumn(TITLE[1],
                renderer,
                text=COLUMN_DISCRIPTION,
                editable=COLUMN_EDITABLE)
        tv.append_column(col)

        renderer = gtk.CellRendererText()
        renderer.connect("edited", self.on_edited, tv)
        col = gtk.TreeViewColumn(TITLE[2],
                renderer,
                text=COLUMN_COMMAND,
                editable=COLUMN_EDITABLE)
        tv.append_column(col)

        return tv

    def on_new_clicked(self, widget):
        self.list.set(self.list.append(),
                 COLUMN_SHORTCUT, "shortcut",
                 COLUMN_DISCRIPTION, "discription",
                 COLUMN_COMMAND, "command",
                 COLUMN_EDITABLE, True
                 )
        self.tv.set_model(self.list)

    def on_delete_clicked(self, widget):
        list, iter = self.tv.get_selection().get_selected()
        list.remove(iter)
        #self.tv.get_selection().select_path(0)

    def on_close_clicked(self, widget):
        tmp_shortcuts_txt='Shortcut,Discription,Command\n'
        
        iter = self.list.get_iter_first()
        sct = self.list.get_value(iter, COLUMN_SHORTCUT)
        dis = self.list.get_value(iter, COLUMN_DISCRIPTION)
        cmd = self.list.get_value(iter, COLUMN_COMMAND)

        tmp_shortcuts_txt += '%s,%s,%s\n' % \
                (sct.encode('utf-8'), dis.encode('utf-8'), cmd.encode('utf-8'))
        while True:
            try:
                iter = self.list.iter_next(iter)
                sct = self.list.get_value(iter, COLUMN_SHORTCUT)
                dis = self.list.get_value(iter, COLUMN_DISCRIPTION)
                cmd = self.list.get_value(iter, COLUMN_COMMAND)
                tmp_shortcuts_txt += '%s,%s,%s\n' % \
                   (sct.encode('utf-8'), dis.encode('utf-8'), cmd.encode('utf-8'))
            except:
                break
        
        # save and cover old file
        fhandle = open(SHORTCUTS_CONF, 'w')
        fhandle.write(tmp_shortcuts_txt)
        fhandle.close()

        self.on_cancel_clicked(None)

    def on_cancel_clicked(self, widget):
        self.win.destroy()
        del self.win

    def on_edited(self, cellrenderer, row, new_text, tv): #5
        title = tv.get_cursor()[1].get_title()
        title = title.encode('utf-8')
        iter = tv.get_model().get_iter_from_string(row)
        self.list.set_value(iter, TITLE.index(title), new_text)

if __name__ == '__main__':
    test = ShortCutsEditer()
    test.win.connect('destroy', lambda _: gtk.main_quit())
    gtk.main()

