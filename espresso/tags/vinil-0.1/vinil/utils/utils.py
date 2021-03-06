#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def parseFile(filename):
    e = []
    x = []
    y = []
    z = []
    f = open(filename,  "r")
    line = f.readline() # Skip the first line with header
    line = f.readline()
    while line:
        list = line.split()

        #Convert strings to float and append to the list
        e.append(float(list[0]))
        x.append(float(list[1]))
        y.append(float(list[2]))
        z.append(float(list[3]))
        line = f.readline()
    f.close()
    return (e,  x,  y,  z)

def parsePHFile(filename):
    e = []
    x = []
    f = open(filename,  "r")
    line = f.readline()
    while line:
        list = line.split()
        #print list
        e.append(float(list[0]))
        x.append(float(list[1]))
        line = f.readline()
    f.close()
    return (e,  x)

def test():
    print "Testing utils.utils.test()"

__date__ = "$Jul 30, 2009 12:08:31 PM$"


