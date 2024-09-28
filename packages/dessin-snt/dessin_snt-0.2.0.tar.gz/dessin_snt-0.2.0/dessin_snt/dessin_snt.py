#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Christophe Viroulaud
@Time:   Lundi 20 Septembre 2021 22:21
"""

from PIL import Image
import os
from random import randint

LONGUEUR, LARGEUR = 800, 600


def creer_image_vide(r: int, v: int, b: int):
    if r < 0 or r > 255:
        r = 255
    if v < 0 or v > 255:
        v = 255
    if b < 0 or b > 255:
        b = 255
    return Image.new("RGB", (LONGUEUR, LARGEUR), (r, v, b))


def afficher(image):
    image.show()


def sauvegarder(image, nom):
    # nom_fichier = os.path.basename(__file__)
    rep = os.path.dirname(os.path.abspath(__file__))
    image.save(rep + "/" + nom + ".png")


def placer_pixel(image, x, y):
    assert x >= 0 or x < LONGUEUR, "valeur hors limite"
    assert y >= 0 or y < LARGEUR, "valeur hors limite"
    image.putpixel((x, y), (0, 0, 0))


def trait_vertical(image, x, debut=0, fin=599, couleur=(0, 0, 0)):
    assert x >= 0 or x < LONGUEUR, "valeur hors limite"
    assert debut >= 0, "valeur hors limite"
    assert fin < LARGEUR, "valeur hors limite"
    for y in range(debut, fin + 1):
        image.putpixel((x, y), couleur)


def trait_horizontal(image, y, debut=0, fin=799, couleur=(0, 0, 0)):
    assert y >= 0 or y < LARGEUR, "valeur hors limite"
    assert debut >= 0, "valeur hors limite"
    assert fin < LONGUEUR, "valeur hors limite"
    for x in range(debut, fin + 1):
        image.putpixel((x, y), couleur)


def carre(
    image,
    o_x=LONGUEUR // 2 - LONGUEUR // 20,
    o_y=LARGEUR // 2 - LONGUEUR // 20,
    longueur=LONGUEUR // 10,
    couleur=(0, 0, 0),
):
    for x in range(o_x, o_x + longueur):
        for y in range(o_y, o_y + longueur):
            image.putpixel((x, y), couleur)


def disque(
    image, o_x=LONGUEUR // 2, o_y=LARGEUR // 2, rayon=LONGUEUR // 10, couleur=(0, 0, 0)
):
    for x in range(-rayon, rayon):
        for y in range(-rayon, rayon):
            if x**2 + y**2 <= rayon**2:
                image.putpixel((o_x + x, o_y + y), couleur)


def donner_couleur():
    return randint(0, 255), randint(0, 255), randint(0, 255)

