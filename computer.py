#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys
from Parsing import ParseInfo

result = dict()


def getData(entry):
    info = ParseInfo(entry)
    if not info.parse:
        return

    return info


if __name__ == '__main__':
    if len(sys.argv) > 1:
        exit('You shouln\'t set an entry')

    while True:
        inp = str(input("> "))
        if inp == 'quit()':
            exit(0)
        else:
            getData(inp)
