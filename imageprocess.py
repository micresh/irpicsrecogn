# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 22:30:32 2016

@author: micresh
"""

from tifffile import *
import numpy as np
import csv


def objslicefromtiff(filenum, objectnum, xcen, ycen, n=150):
    xstart = xcen-n/2
    xfin = xcen+n/2-1
    ystart = ycen - n/2
    yfin = ycen + n/2-1
    if xcen <= n:
        xstart = 1
        xfin = n
    if ycen <= n:
        ystart = 1
        yfin = n
    if xcen >= 16000-n/2:
        xstart = 16000-n
        xfin = 16000
    if ycen >= 576-n/2:
        ystart = 576-n
        yfin = 576
    filenamecurr = filenum + '.tif'
    tif1 = imread(filenamecurr)
    objimage = np.zeros((n+1, n+1), dtype=np.uint16)
    yy = 0
    for y in range(ystart, yfin):
        xx = 0
        for x in range(xstart, xfin):
            objimage[yy][xx] = tif1[y][x]
            xx += 1
        yy += 1
    filenameresult = filenum + '-' + objectnum + '.tif'
    # print tif1.dtype, objimage.dtype
    with TiffWriter(filenameresult) as tif:
        tif.save(objimage, photometric='minisblack')
    return


def objlinintiff(filenum, xcen, ycen, n=100):
    xstart = xcen-n/2
    xfin = xcen+n/2-1
    ystart = ycen - n/2
    yfin = ycen + n/2-1
    if xcen <= n:
        xstart = 1
        xfin = n
    if ycen <= n:
        ystart = 1
        yfin = n
    if xcen >= 16000-n/2:
        xstart = 16000-n
        xfin = 15999
    if ycen >= 576-n/2:
        ystart = 576-n
        yfin = 575
    filenamecurr = filenum + '.tif'
    tif1 = imread(filenamecurr)
    for z in range(1, n-1):
        tif1[ystart][xstart+z] = 0
        tif1[yfin][xstart+z] = 0
        tif1[ystart+z][xstart] = 0
        tif1[ystart+z][xfin] = 0
    with TiffWriter(filenamecurr) as tif:
        tif.save(tif1, photometric='minisblack')
        tif.close()
    return


# objslicefromtiff('2-test','0',103,30)
pics = 0
previm = ''
currim = '1'
with open('objects.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    i = 0
    for row in reader:
        print "current object num = ", i
        objlinintiff(str(row[0]), int(row[1]), int(row[2]))
        i += 1
#        previm = currim
#        currim = row[0]
#        if previm == currim:
#            pics += 1
#        else:
#            pics = 0
#        objslicefromtiff(str(row[0]), str(pics), int(row[1]), int(row[2]))
