# -*- coding: utf-8 -*-

#   Copyright (C) 2008-2016 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pychoacoustics

#    pychoacoustics is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pychoacoustics is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pychoacoustics.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import numpy


def get_list_indices(li, value):
    """ Get the indices of the elements of a list matching a certain value.
    The indices are returned as a list.
    
    Keyword ardguments:
    li -- a list
    value -- the value of the items you're searching for

    """
    idx = []
    for i in range(len(li)):
        if li[i] == value:
            idx.append(i)

    return idx

def checkEmailValid(address):
    emailValid = False
    if address.rfind('@') != -1 and len(address) > 2:
        if len(address.split('@')) == 2:
            loc = address.split('@')[0]
            dom = address.split('@')[1]
            if len(loc) > 0 and len(dom) > 0:
                emailValid = True
    return(emailValid)

def checkUsernameValid(username):
    usnValid = False
    if len(username) > 0:
        usnValid = True
    return(usnValid)
def checkServerValid(server):
    serverValid = False
    if len(server) > 0:
        serverValid = True
    return(serverValid)
def putDoubleQuotes(instr):
    instr = '"' + instr + '"'
    return instr
def strToBoolean(stringValue):
    if stringValue == "True":
        out = True
    elif stringValue == "False":
        out = False
    return out
    
    
def isEven(number):
    if number%2 == 0:
        out = True
    else:
        out = False

    return out

def stimSpacingGrid(lo, hi, step, scale='linear'):
    if scale == "linear":
        seq = numpy.arange(lo, hi+step, step)
    elif scale == "log":
        cnt = 0
        seq = numpy.array([lo])
        while seq[cnt] < hi:
            seq = numpy.concatenate((seq, [seq[cnt]*step]), 1)
            cnt = cnt+1
    return seq


