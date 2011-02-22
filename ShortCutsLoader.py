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

class ShortCutsLoader:
    '''Load Shortcuts, filter Shortcuts,

    including Keys/discription/command and input matching

    Construction:
        conffile: short config file

    Data structure:
        self.shortcutspool data structrue: {shortcut: [ command, discription]}
            {'command': ['cmd', 'Terminal']}

        self.shortcutmatch data structure: {number: shortcut}
            {0: 'cmmand'; 1: 'mycomputer'}
    '''
    def __init__(self, conffile):
        self.input = ''
        self.conffile = conffile
        self.shortcutspool = {}
        self.shortcutmatch = {}
        self.shortcuttop10 = {}

        for line in conffile:
            line = line.split(',')
            self.shortcutspool[line[0]] = [line[2].replace('\n',''), line[1]]

        i = 0
        for line in conffile:
            line = line.split(',')
            self.shortcutmatch[i] = line[0]
            i += 1
            #if i > 9:
            #    break
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


