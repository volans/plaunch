#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#	PLaunch - Shortcuts management tool, base on pyton/pygtk/pyxlib
#
#	Copyright (C) 2008 Volans  <volansw@gmail.com>
#
#	PLaunch is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 2 of the License, or (at your 
# option) any later version.  
#
#	PLaunch is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License 
# for more details.  
#
#	You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.   
#-------------------------------------------------------------------------------
import gtk
import gobject


KEYBINDING_DEFAULT = 1

_keybound_object = None
def GetKeyboundObject():
	"""Get the shared instance"""
	global _keybound_object
	if not _keybound_object:
		_keybound_object = KeyboundObject()
	return _keybound_object

class KeyboundObject (gobject.GObject):
	"""Keybinder object

	signals:
		keybinding (target, event_time)
		keybinding signal is triggered when the key bound
		for @target is triggered.
	"""
	__gtype_name__ = "KeyboundObject"
	def __init__(self):
		super(KeyboundObject, self).__init__()
	def _keybinding(self, target):
		import keybinder
		time = keybinder.get_current_event_time()
		self.emit("keybinding", target, time)

gobject.signal_new("keybinding", KeyboundObject, gobject.SIGNAL_RUN_LAST,
		gobject.TYPE_BOOLEAN, (gobject.TYPE_INT, gobject.TYPE_INT))

_currently_bound = {}

def _register_bound_key(keystr, target):
	_currently_bound[target] = keystr

def get_currently_bound_key(target=KEYBINDING_DEFAULT):
	return _currently_bound.get(target)

def bind_key(keystr, keybinding_target=KEYBINDING_DEFAULT):
	"""
	Bind @keystr, unbinding any previous key for @keybinding_target.
	If @keystr is a false value, any previous key will be unbound.
	"""
	try:
		import keybinder
	except ImportError:
		print(__name__, "Could not import keybinder, "
				"keybindings disabled!")
		return False

	keybinding_target = int(keybinding_target)
	callback = lambda : GetKeyboundObject()._keybinding(keybinding_target)
	if keystr and len(keystr) == 1:
		print(__name__, "Refusing to bind key", repr(keystr))
		return False

	succ = True
	if keystr:
		try:
			succ = keybinder.bind(keystr, callback)
			print(__name__, "binding", repr(keystr))
		except KeyError, exc:
			print(__name__, exc)
			succ = False
	if succ:
		old_keystr = get_currently_bound_key(keybinding_target)
		if old_keystr and old_keystr != keystr:
			keybinder.unbind(old_keystr)
			print(__name__, "unbinding", repr(old_keystr))
		_register_bound_key(keystr, keybinding_target)
	return succ

class KeyHook():
	'''Key hook for global hotkey.
	
	'''
	def __init__(self, function, hotkey="<Alt>R"):
		self.function = function
		self.hotkey = hotkey		

	def callback(self, keyobj, keybinding_number, event_time):
		self.function(time=event_time)
	
	def start(self):
		if self.hotkey:
			succ = bind_key(self.hotkey)
			print("Trying to register %s to spawn kupfer.. %s"
				% (self.hotkey, ["failed", "success"][int(succ)]))
		keyobj = GetKeyboundObject()
		keyobj.connect("keybinding", self.callback)

	def stop(self):
		bind_key(None)

	
if __name__ == '__main__':
	import gtk
	def func():
		print "got hot key!"
	test = KeyHook(func)	
	test.start()
	gtk.main()
	test.stop()

