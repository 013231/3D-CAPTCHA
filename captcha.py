#!/usr/bin/env python 
# encoding=utf-8

from random import uniform, shuffle
from cStringIO import StringIO
from PIL import ImageFont, Image, ImageDraw
import numpy, pylab
from mpl_toolkits.mplot3d import Axes3D

fontPath = '/Library/Fonts/Arial.ttf'

def makeImage(text, width=400, height=200, angle=None):
    '''Generate a 3d CAPTCHA image.
    Args:
        text: Text in the image.
        width: Image width in pixel.
        height: Image height in pixel.
        angle: The angle between text and X axis.
    Returns:
        Binary data of CAPTCHA image in PNG format.
    '''
    angle = angle if angle != None else uniform(-20, 20)
    try:
        font = ImageFont.truetype(fontPath, 24)
    except IOError:
        raise IOError(
            'Font file doesn\'t exist. Please set `fontPath` correctly.')
    txtW, txtH = font.getsize(text)
    img = Image.new('L', (txtW * 3, txtH * 3), 255)
    drw = ImageDraw.Draw(img)
    drw.text((txtW, txtH), text, font=font)

    fig = pylab.figure(figsize=(width/100.0, height/100.0))
    ax = Axes3D(fig)
    X, Y = numpy.meshgrid(range(img.size[0]), range(img.size[1]))
    Z = 1 - numpy.asarray(img) / 255
    ax.plot_wireframe(X, -Y, Z, rstride=1, cstride=1)
    ax.set_zlim((-3, 3))
    ax.set_xlim((txtW * 1.1, txtW * 1.9))
    ax.set_ylim((-txtH * 1.9, -txtH * 1.1))
    ax.set_axis_off()
    ax.view_init(elev=60, azim=-90 + angle)

    fim = StringIO()
    fig.savefig(fim, format='png')
    binData = fim.getvalue()
    fim.close()
    return binData

def randStr(length=7):
    '''Generate a random string composed of lowercase and digital.
    Indistinguishable characters have been removed.
    '''
    characters = list('bcdghijkmnpqrtuvwxyz23456789')
    shuffle(characters)
    return ''.join(characters[:length])


if __name__ == '__main__':
    for i in range(20):
        img = makeImage(randStr(), width=512)
        with open('%d.png' % i, 'wb') as f:
            f.write(img)
        print i
