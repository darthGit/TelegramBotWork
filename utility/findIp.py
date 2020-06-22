#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import sys


def find_shop(shop_name):
    word = shop_name.lower()
    result = []
    with io.open('/home/darthgit/lkh-it-adm-05/iplist', encoding='utf-8') as file:
        for line in file:
            linelow = line.lower()
            if word in linelow:
                splitedStr = line.split()
                result.append([splitedStr[0], " ".join(splitedStr[1:len(splitedStr)])])
        return result
