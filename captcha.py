#!/usr/bin/env python 
# encoding=utf-8

import random
import cStringIO
import ImageFont, Image, ImageDraw
import numpy, pylab
import mpl_toolkits.mplot3d

fontPath = '/Library/Fonts/Arial.ttf'

def makeImage(text, angle=random.randint(-20, 20)):
    '''Generate a 3d CAPTCHA image.
    Args:
        text: Text in the image.
        angle: The angle between text and X axis.
    Returns:
        Binary data of CAPTCHA image.
    '''
    #XXx
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
    ax = mpl_toolkits.mplot3d.Axes3D(fig)
    X, Y = numpy.meshgrid(range(img.size[0]), range(img.size[1]))
    Z = 1 - numpy.asarray(img) / 255
    ax.plot_wireframe(X, -Y, Z, rstride=1, cstride=1)
    ax.set_zlim((-3, 3))
    ax.set_xlim((txtW * 1.1, txtW * 1.9))
    ax.set_ylim((-txtH * 1.9, -txtH * 1.1))
    ax.set_axis_off()
    ax.view_init(elev=60, azim=-90 + angle)

    fim = cStringIO.StringIO()
    fig.savefig(fim, format='png')
    binData = fim.getvalue()
    fim.close()
    return binData

if __name__ == '__main__':
    #Hard to recognize characters have been removed from this list.
    characters = list('bcdghijkmnpqrtuvwxyz23456789')
    for i in range(-20, 21):
        random.shuffle(characters)
        word = ''.join(characters[:7])
        img = makeImage(word, angle=i)
        with open('%d.png' % (i + 20), 'wb') as outFile:
            outFile.write(img)
        print i
