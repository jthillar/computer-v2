#!/usr/bin/env
# -*- coding: utf-8 -*-
import re

class Calcul:

	def __init__(self, result):
		self.result = result
	def __repr__(self):
		return str(self.result)

class ParseInfo:

	def __init__(self, entry):
		self.firstPart, self.secondPart = self.splitEntry(entry)
		self.first = self.parseFirst(self.firstPart)
		self.secondType = self.parseSecond()
		self.parse = True

	def checkConstruction(self, part):

		badConstruction = re.findall('\w\s+\w|\w\s+\(|\)\s+\w|\)\(|\)\s+\(|\(\)|^[\%\/\*]|[\+\-\%\/\*]$', part)
		if len(badConstruction) > 0:
			return
		part = part.replace(' ', '')
		doubleSign = re.findall('[\+\-\*\%\/][\+\-\*\%\/]', part)
		if len(doubleSign) > 0:
			return

		return part

	def splitEntry(self, entry):
		firstPart = None
		secondPart = None

		splitingEqual = entry.split('=')
		if len(splitingEqual) == 2:
			firstPart = splitingEqual[0].strip() if splitingEqual[0].strip() != '' else None
			firstPart = self.checkConstruction(firstPart)
			secondPart = splitingEqual[1].strip() if splitingEqual[0].strip() != '' else None
			secondPart = self.checkConstruction(secondPart)
		return firstPart, secondPart

	def parseFirst(self, part):

		if part is None:
			self.parse = False
			return

		number = self.checkNumber(part)
		if number is not None:return number

		var = self.checkVar(part)
		if var is not None: return var

		func = self.checkFunc(part)
		if func is not None: return func

		op = self.checkOp(part)
		if op is not None: return op

		self.parse = False
		return None

	def parseSecond(self):

		if self.secondPart is None:
			return

	def checkNumber(self, part):
		try:
			result = eval(part)
			return {'number': result}
		except NameError as n:
			return None

	def checkVar(self, part):
		"""Verification si la partie est une variable"""
		if not part.isalpha() or part == 'i':
			return None
		return {'variable': part}

	def checkFunc(self, part):
		"""Verification si la partie est suelement un nom de fonction"""
		func = re.findall('^[a-zA-Z]+\([a-zA-Z]+\)$', part)
		if len(func) != 1:
			return None
		return {'function': part}

	def checkMultiFunc(self, part):
		""" On regarde si un element ressemble à la syntaxe d'un nom de function
		et on remplace la parti par un code de remplacement"""

		funcVec = re.findall('[a-zA-Z]+\([a-zA-Z]+\)', part)
		functionDict = dict()
		if len(funcVec) > 0:
			for id, func in enumerate(funcVec):
				part = part.replace(func, '\"f' + str(id) + '\"')
				functionDict['\"f' + str(id) + '\"'] = func
		return part, functionDict

	def checkOp(self, part):

		operation = list()
		# On récupère les position par couple de parentheses
		if len(part) > 0 and part[0] != '-':
			part = '+' + part

		part, functionDict = self.checkMultiFunc(part)

		part, parenthesisDict = self.checkParenthesis(part, operation)
		if part is None: return None

		infos = re.split(r'([\+\-\/\*\%])', part)
		if len(infos) > 0 and infos[0] == '':
			del infos[0]
		if len(infos) % 2 != 0:
			return None
		signs = [x for i, x in enumerate(infos) if i % 2 == 0]
		values = [x for i, x in enumerate(infos) if i % 2 == 1]
		for sign, value in zip(signs, values):
			subElement = dict(sign=sign)
			if len(re.findall('^\"p\d+\"', value)) > 0:
				subElement['parenthesis'] = parenthesisDict[value]
			elif len(re.findall('^\"f\d+\"', value)) > 0:
				subElement['function'] = functionDict[value]
			elif self.checkVar(value) is not None:
				subElement.update(self.checkVar(value))
			elif self.checkNumber(value):
				subElement.update(self.checkNumber(value))
			else:
				return None
			operation.append(subElement)

		return {'operation': operation}

	def positionParentheses(self, part):

		opening = [i for i, c in enumerate(part) if c == '(']
		closing = [i for i, c in enumerate(part) if c == ')']
		if len(opening) != len(closing):
			return None
		result = list()
		for posClosing in closing:
			for i, posOpening in enumerate(opening):
				index = i
				if posOpening > posClosing:
					index = i - 1
					result.append([opening[index], posClosing])
					opening.pop(index)
					break
				if i == len(opening) - 1:
					result.append([opening[index], posClosing])
					opening.pop(index)

		for couple in result:
			if couple[0] > couple[1]:
				return None

		return result

	def sortParentheses(self, coupleVec):
		"""Get Largest or single penrathese"""

		coupleToDrop = list()
		for i, couple in enumerate(coupleVec):
			for couple2 in coupleVec:
				if couple[0] > couple2[0] and couple[1] < couple2[1]:
					coupleToDrop.append(i)
		for i in coupleToDrop:
			del coupleVec[i]

		return coupleVec

	def checkParenthesis(self, part, operation):
		coupleVec = self.positionParentheses(part)
		if coupleVec is None:
			return None, None

		if len(coupleVec) > 0:
			coupleVec = self.sortParentheses(coupleVec)
			parenthesisDict = dict()
			partToDropVec = list()
			for id, couple in enumerate(coupleVec):
				resultCouple = self.parseFirst(part[couple[0] + 1:couple[1]])
				if resultCouple is None:
					return None, None
				if 'operation' in resultCouple:
					parenthesisDict['\"p' + str(id) + '\"'] = resultCouple['operation']
					partToDropVec.append(['operation', part[couple[0]:couple[1] + 1]])
				else:
					partToDropVec.append(['notOperation', part[couple[0]:couple[1] + 1]])

			for id, partToDrop in enumerate(partToDropVec):
				if partToDrop[0] == 'operation':
					part = part.replace(partToDrop[1], '\"p' + str(id) + '\"')
				else:
					part = part.replace(partToDrop[1], partToDrop[1][1:-1])

			return part, parenthesisDict


		return part, None

	def __repr__(self):
		return str(self.firstPart) + str(self.secondPart)
