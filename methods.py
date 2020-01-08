#!/usr/bin/env
# -*- coding: utf-8 -*-
import re

class Calcul:

	def __init__(self, result):
		self.result = result
	def __repr__(self):
		return f"{self.result}"

class ParseInfo:
	"""docstring forParseInfo."""

	def __init__(self, entry):
		self.firstPart, self.secondPart = self.splitEntry(entry)
		self.firstType = self.parseFirst()
		self.secondType = self.parseSecond()
		self.parse = True

	def splitEntry(self, entry):
		firstPart = None
		secondPart = None
		splitingEqual = entry.split('=')
		if len(splitingEqual) == 2:
			firstPart = splitingEqual[0].strip() if splitingEqual[0].strip() != '' else None
			secondPart = splitingEqual[1].strip() if splitingEqual[0].strip() != '' else None

		return firstPart, secondPart

	def parseFirst(self):

		if self.firstPart is None:
			return

		if self.checkVar(self.firstPart):
			return 'variable'
		elif self.checkFunc(self.firstPart):
			return 'function'
		elif self.checkOp(self.firstPart):
			return 'operation'
		else:
			self.parse = False
		return None

	def parseSecond(self):

		if self.secondPart is None:
			return

	def checkVar(self, part):
		if not part.isalpha() or part != 'i':
			return False
		return True

	def checkFunc(self, part):
		x = re.findall('(?<=\d)\s(?=\d)', part)
		nameFunc = re.findall('[a-zA-Z]+(?=\([a-zA-Z]+\))', part)
		if len(x) != 1 or len(nameFunc) != 1:
			return False
		if not nameFunc[0].isalpha() or not x[0].isalpha():
			return False
		rightParenthese = re.findall('(?<=\(x[0]\)).')
		if len(rightParenthese) > 0:
			return False
		return True

	def checkOp(self, part):

		infos = re.split(r'([\+\-\/\*])', part)
		for info in infos:
			if info.strip() != '':
				if self.checkVar(info) or self.checkFunc(info) or info.isnumeric():
					continue
			else:
				return False

		return True

	def inParenthesis(self, group):
		



	def __repr__(self):
		return f"{self.firstPart}, {self.secondPart}, {self.firstType}"
