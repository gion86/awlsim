# -*- coding: utf-8 -*-
#
# AWL simulator - Library entry selection
#
# Copyright 2014-2015 Michael Buesch <m@bues.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from __future__ import division, absolute_import, print_function, unicode_literals
from awlsim.common.compat import *

from awlsim.common.enumeration import *
from awlsim.common.wordpacker import *

import hashlib
import binascii


class AwlLibEntrySelection(object):
	"""AWL library entry selection."""

	IDENT_HASH	= "sha256"

	# Library entry type.
	# This enumeration is awlsim-coreserver API!
	EnumGen.start
	TYPE_UNKNOWN	= EnumGen.item
	TYPE_FC		= EnumGen.item
	TYPE_FB		= EnumGen.item
	EnumGen.end

	def __init__(self, libName="",
		     entryType=TYPE_UNKNOWN,
		     entryIndex=-1, effectiveEntryIndex=-1):
		self.__identHash = None
		self.setLibName(libName)
		self.setEntryType(entryType)
		self.setEntryIndex(entryIndex)
		self.setEffectiveEntryIndex(effectiveEntryIndex)

	def setLibName(self, libName):
		self.__libName = libName.strip()
		self.__identHash = None

	def getLibName(self):
		return self.__libName

	def setEntryType(self, entryType):
		if entryType not in (self.TYPE_UNKNOWN,
				     self.TYPE_FC,
				     self.TYPE_FB):
			raise AwlSimError("Library selection: "
				"Invalid entry type %d." %\
				entryType)
		self.__entryType = entryType
		self.__identHash = None

	def getEntryType(self):
		return self.__entryType

	def getEntryTypeStr(self):
		return {
			self.TYPE_UNKNOWN	: "UNKNOWN",
			self.TYPE_FC		: "FC",
			self.TYPE_FB		: "FB",
		}[self.getEntryType()]

	def setEntryIndex(self, entryIndex):
		if entryIndex < -1 or entryIndex > 0xFFFF:
			raise AwlSimError("Library selection: "
				"Invalid entry index %d." %\
				entryIndex)
		self.__entryIndex = entryIndex
		self.__identHash = None

	def getEntryIndex(self):
		return self.__entryIndex

	def setEffectiveEntryIndex(self, effectiveEntryIndex):
		if effectiveEntryIndex < -1 or effectiveEntryIndex > 0xFFFF:
			raise AwlSimError("Library selection: "
				"Invalid effective entry index %d." %\
				effectiveEntryIndex)
		self.__effectiveEntryIndex = effectiveEntryIndex
		self.__identHash = None

	def getEffectiveEntryIndex(self):
		return self.__effectiveEntryIndex

	def isValid(self):
		return self.__libName and\
		       self.__entryType in (self.TYPE_FC, self.TYPE_FB) and\
		       self.__entryIndex >= 0 and\
		       self.__entryIndex <= 0xFFFF and\
		       self.__effectiveEntryIndex >= 0 and\
		       self.__effectiveEntryIndex <= 0xFFFF

	def getIdentHash(self):
		"""Get the unique identification hash for this
		library selection descriptor.
		"""
		if not self.__identHash:
			# Calculate the ident hash
			h = hashlib.new(self.IDENT_HASH, b"AwlLibEntrySelection")
			h.update(self.__libName.encode("utf-8", "ignore"))
			h.update(WordPacker.toBytes(bytearray(4), 32, 0,
						    self.__entryIndex))
			h.update(WordPacker.toBytes(bytearray(4), 32, 0,
						    self.__effectiveEntryIndex))
			self.__identHash = h.digest()
		return self.__identHash

	def getIdentHashStr(self):
		return binascii.b2a_hex(self.getIdentHash()).decode("ascii")

	def __eq__(self, other):
		return self.getIdentHash() == other.getIdentHash()

	def __ne__(self, other):
		return not self.__eq__(other)

	def __repr__(self):
		asStr = ""
		if self.getEntryIndex() != self.getEffectiveEntryIndex():
			asStr = " (as %s %d)" % (self.getEntryTypeStr(),
						 self.getEffectiveEntryIndex())
		return "%s: %s %d%s" % (
			self.getLibName(),
			self.getEntryTypeStr(),
			self.getEntryIndex(),
			asStr,
		)
