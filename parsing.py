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
		self.second = self.parseSecond(self.secondPart)
		self.parse = True

	def checkConstruction(self, part):

		badConstruction = re.findall('\w\s+\w|\w\s+\(|\)\s+\w|\)\(|\)\s+\(|\(\)|^[\%\/\*]|[\+\-\%\/\*]$', part)
		if len(badConstruction) > 0:
			return
		part = part.replace(' ', '')
		part = re.sub(r'([a-z])(\d+)', r'\1*\2', part)
		part = re.sub(r'(\d+)([a-z])', r'\1*\2', part)
		doubleSign = re.findall('[\+\-\*\%\/][\+\-\*\%\/]', part)
		for	ds in doubleSign:
			if ds != '**':
				return
		if '***' in part:
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

		if part is None or part == '':
			self.parse = False
			return

		number = self.checkNumber(part)
		if number is not None:return number

		var = self.checkVar(part)
		if var is not None: return var

		func = self.checkFunc(part)
		if func is not None: return func

		mat = self.checkMatrice(part)
		if mat is not None: return mat

		op = self.checkOp(part)
		if op is not None: return op

		self.parse = False
		return None

	def parseSecond(self, part):

		if part is None or part == '':
			self.parse=False
			return

		result = {'resolution': True}
		if part == '?':
			return result

		if part[-1] == '?':
			part = part[:-1]
		else:
			result['resolution'] = False
		parsePart = self.parseFirst(part)
		if parsePart is None:
			self.parse = False
			return

		result.update(parsePart)
		return result

	def checkCoef(self, part):
		coef = re.findall('\^\w+$', part)
		if len(coef) > 0:
			part = part.replace(coef[0], '')
			coef = coef[0][1:]
		else:
			coef = '1'
		return part, coef

	def checkNumber(self, part):
		"""Verification si la partie est un nombre"""
		try:
			part, coef = self.checkCoef(part)
			part = eval(part)
			if isinstance(part, list):
				raise NameError
			sign = '+' if part >= 0 else '-'
			return {'number': abs(part), 'sign': sign, 'coefficient': coef}

		except (NameError, SyntaxError) as e:
			return None

	def checkImaginaire(self, part):
		"""Verification si la partie est i"""
		if part == 'i':
			return {'imaginaire': 'i', 'sign': '+', 'coefficient': '1'}

	def checkVar(self, part):
		"""Verification si la partie est une variable"""

		if not part.isalpha() or part == 'i':
			return None
		return {'variable': part, 'sign': '+', 'coefficient': '1'}

	def checkFunc(self, part):
		"""Verification si la partie est suelement un nom de fonction"""
		func = re.findall('^[a-zA-Z]+\([a-zA-Z]+\)$', part)
		if len(func) != 1:
			return None

		result = {'function':
					{'name': re.findall('^[a-zA-Z]+(?=\()', part)[0],
					'variable': re.findall('(?<=\()[a-zA-Z](?=\))', part)[0],
					'coefficient': '1',
					'sign': '+'},
				'sign': '+',
				'coefficient': '1'}

		return result

	def checkMultiFunc(self, part):
		""" On regarde si un element ressemble à la syntaxe d'un nom de function
		et on remplace la parti par un code de remplacement"""

		funcVec = re.findall('[a-zA-Z]+\([a-zA-Z]+\)', part)
		functionDict = dict()
		if len(funcVec) > 0:
			for id, func in enumerate(funcVec):
				part = part.replace(func, '\"f' + str(id) + '\"')
				functionDict['\"f' + str(id) + '\"'] = self.checkFunc(func)
		return part, functionDict

	def checkMatrice(self, part):

		if part[0:2] == '[[' and part[-2:] == ']]':
			matriceSplit = part[2:-2].split('];[')
			for element in matriceSplit:
				if len(re.findall('^.+\,.+$', element)) > 0:
					continue
				return None

			matrice = list()
			for element in matriceSplit:
				parsedElement1 = self.parseFirst(element.split(',')[0])
				parsedElement2 = self.parseFirst(element.split(',')[1])
				if parsedElement1 is not None and parsedElement2 is not None:
					matrice.append([parsedElement1, parsedElement2])
				else:
					return None

			return {'matrice': matrice, 'sign': '+', 'coefficient': '1'}

	def checkOp(self, part, recursion=0):

		operation = list()
		# On récupère les position par couple de parentheses
		if len(part) > 0 and part[0] not in ['+', '-'] :
			part = '+' + part

		part, functionDict = self.checkMultiFunc(part)

		part, parenthesisDict = self.checkParenthesisAndFunction(part, operation)
		if part is None: return None

		infos = re.split(r'([\+\-\/\%]|[\*]+)', part)
		if len(infos) > 0 and infos[0] == '':
			del infos[0]
		if len(infos) % 2 != 0:
			return None
		signs = [x for i, x in enumerate(infos) if i % 2 == 0]
		values = [x for i, x in enumerate(infos) if i % 2 == 1]
		for sign, value in zip(signs, values):
			value, coef = self.checkCoef(value)
			subElement = dict(sign=sign)
			if len(re.findall('^\"p\d+\"', value)) > 0:
				subElement['parenthesis'] = parenthesisDict[value]
			elif len(re.findall('^\"fp\d+\"', value)) > 0:
				subElement['function'] = parenthesisDict[value]
			elif len(re.findall('^\"f\d+\"', value)) > 0:
				subElement['function'] = functionDict[value]['function']
			elif self.checkVar(value) is not None:
				subElement['variable'] = self.checkVar(value)['variable']
			elif self.checkNumber(value) is not None:
				subElement['number'] = self.checkNumber(value)['number']
			elif self.checkMatrice(value) is not None:
				subElement['matrice'] = self.checkMatrice(value)['matrice']
			elif self.checkImaginaire(value) is not None:
				subElement['imaginaire'] = self.checkImaginaire(value)['imaginaire']
			else:
				return

			subElement['coefficient'] = coef
			operation.append(subElement)

		return {'operation': operation, 'coefficient': '1', 'sign': '+'}

	def positionParentheses(self, part):

		opening = [(x.start(), x.end()-1) for x in re.finditer('[a-zA-Z]+\(|(?<=[\+\-\*\%\/])\(', part)]
		closing = [i for i, c in enumerate(part) if c == ')']
		if len(opening) != len(closing):
			return None
		result = list()
		for posClosing in closing:
			for i, posOpening in enumerate(opening):
				index = i
				if posOpening[0] > posClosing:
					index = i - 1
					result.append([opening[index], posClosing])
					opening.pop(index)
					break
				if i == len(opening) - 1:
					result.append([opening[index], posClosing])
					opening.pop(index)

		for couple in result:
			if couple[0][1] > couple[1]:
				return None

		return result

	def sortParentheses(self, coupleVec):
		"""Get Largest or single penrathese"""

		coupleToDrop = list()
		for i, couple in enumerate(coupleVec):
			for couple2 in coupleVec:
				if couple[0][0] > couple2[0][0] and couple[1] < couple2[1]:
					coupleToDrop.append(i)
		for i in coupleToDrop:
			del coupleVec[i]

		return coupleVec

	def checkParenthesisAndFunction(self, part, operation):
		coupleVec = self.positionParentheses(part)
		if coupleVec is None:
			return None, None

		if len(coupleVec) > 0:
			coupleVec = self.sortParentheses(coupleVec)
			parenthesisDict = dict()
			partToDropVec = list()
			for id, couple in enumerate(coupleVec):
				resultCouple = self.parseFirst(part[couple[0][1] + 1:couple[1]])
				if resultCouple is None:
					return None, None
				type = 'parenthesis' if couple[0][1] - couple[0][0] == 0 else 'function'
				if type == 'parenthesis':
					if 'operation' in resultCouple:
						parenthesisDict['\"p' + str(id) + '\"'] = resultCouple['operation']
						partToDropVec.append([type, 'operation', part[couple[0][0]:couple[1] + 1]])
					else:
						partToDropVec.append([type, 'notOperation', part[couple[0][0]:couple[1] + 1]])
				else:
					resultCouple['name'] = part[couple[0][0]:couple[0][1]]
					parenthesisDict['\"fp' + str(id) + '\"'] = resultCouple
					partToDropVec.append([type, 'operation', part[couple[0][0]:couple[1] + 1]])

			for id, partToDrop in enumerate(partToDropVec):
				if partToDrop[1] == 'operation' and partToDrop[0] == 'parenthesis':
					part = part.replace(partToDrop[2], '\"p' + str(id) + '\"')
				elif partToDrop[0] == 'function':
					part = part.replace(partToDrop[2], '\"fp' + str(id) + '\"')
				else:
					part = part.replace(partToDrop[2], partToDrop[2][1:-1])

			return part, parenthesisDict


		return part, None

	def __repr__(self):
		return str(self.firstPart) + str(self.secondPart)
