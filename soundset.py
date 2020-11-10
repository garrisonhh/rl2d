import pygame as pg
import os

SOUNDS = {}

"""
plays sound
"""
def play_sound(key):
    SOUNDS[key].play()

"""
loads a directory of [name].wav files with the file name as key
"""
def load_dir(dirpath):
    global SOUNDS

    for fname in os.listdir(dirpath):
        if fname.endswith(".wav"):
            SOUNDS[fname[:fname.index(".wav")]] = pg.mixer.Sound(os.path.join(dirpath, fname))
