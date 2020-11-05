import pygame as pg
import os

SOUNDS = {}

def play_sound(key):
    SOUNDS[key].play()

def load_sound(key, sound):
    global SOUNDS
    SOUNDS[key] = sound

def load_dir(dirpath):
    global SOUNDS

    for fname in os.listdir(dirpath):
        if fname.endswith(".wav"):
            load_sound(fname[:fname.index(".wav")], pg.mixer.Sound(os.path.join(dirpath, fname)))
