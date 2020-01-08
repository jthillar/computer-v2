#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys
from methods import ParseInfo, Calcul

result = dict()

def getData(entry):

	info = ParseInfo(entry)
	if not info.parse:
		return

	result[info.firstPart] = info.secondPart

	ok = Calcul(result)
	print(ok)


if __name__ == '__main__':

	if len(sys.argv) > 1:
		exit('You shouln\'t set an entry')


	while True:
		inp = str(input("> "))
		if inp == 'quit()':
			exit(0)
		else:
			getData(inp)
