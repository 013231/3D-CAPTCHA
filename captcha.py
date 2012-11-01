#!/usr/bin/env python 
# encoding=utf-8

from random import shuffle, randint
import numpy, pylab
from PIL import Image, ImageDraw, ImageFont
from mpl_toolkits.mplot3d import Axes3D

fontPath = '/Library/Fonts/Arial.ttf'

def makeImage(text, angle=randint(-20, 20)):
    try:
        font = ImageFont.truetype(fontPath, 24)
    except IOError:
        raise IOError(
            'Font file doesn\'t exist. Please set `fontPath` correctly.')
    txtW, txtH = font.getsize(text)
    img = Image.new('L', (txtW * 3, txtH * 3), 255)
    drw = ImageDraw.Draw(img)
    drw.text((txtW, txtH), text, font=font)

    fig = pylab.figure(figsize=(4, 2))
    ax = Axes3D(fig)
    X, Y = numpy.meshgrid(range(img.size[0]), range(img.size[1]))
    Z = 1 - numpy.asarray(img) / 255
    ax.plot_wireframe(X, -Y, Z, rstride=1, cstride=1)
    ax.set_zlim((-3, 3))
    ax.set_xlim((txtW * 1.1, txtW * 1.9))
    ax.set_ylim((-txtH * 1.9, -txtH * 1.1))
    ax.set_axis_off()
    ax.view_init(elev=60, azim=-90 + angle)
    return fig

if __name__ == '__main__':
    #Hard to recognize characters have been removed from this list.
    characters = list('bcdghijkmnpqrtuvwxyz23456789')
    for i in range(-20, 21):
        shuffle(characters)
        word = ''.join(characters[:7])
        fig = makeImage(word, angle=i)
        fig.savefig('%d.png' % (i + 20))
        print i
