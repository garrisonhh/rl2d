=== RL2D by garrisonhh ===
made for my own fast prototyping with pretty tileset graphics :)

=== potential ideas to implement ===
- easy connected tiles
- movement routines/queues for elements

=== documentation ===
--- tileset ---
get_tile(key)
    DESC
        accesses the tileset dictionary.

    PARAMS
        key

    RETURNS pygame Surface

load_tile(sheet, key, rect = 0, palette = 0, fg = None, bg = None, rotate = 0, fv = 0, fh = 0)
    PARAMS
        sheet - pg.Surface
        key
        rect - if passed, tileset will assign a subsurface of rect to key instead of whole surface.
        palette - if passed, fg and bg will replace non-black and black
        fg - foreground color from palette
        bg - background color from palette. if not passed, image will be transparent
        rotate - number of times to rotate 90 degrees
        fv - boolean; flip tile horizontally
        fh - boolean; flip tile vertically

    RETURNS void

load_tileset(tilesize, tilesheet, definitions, palette = 0)
    DESC
        loads a tilesheet using a definitions file.

    PARAMS
        tilesize - tuple(int width, int height)
        tilesheet - path to image
        definitions - path to tile definitions text file
        palette - pg.Surface

    RETURNS void

    NOTES
        defs look like this:
        ; this is a comment
        key x y ; no palette
        key x y fg ; yes palette, white -> fg, black -> transparent
        key x y fg bg ; yes palette, white -> fg, black -> bg
        key x y -fv ; no palette, flip vertically and horizontally
        key x y fg bg -r2 ; no palette, rotate 90 degrees twice

load_font(charsize, tilesheet, encoding = 'ascii', palette = 0, fg = None, bg = None)
    DESC
        loads all possible printable characters for the tilesheet in specified encoding
        assumes horizontal format

    PARAMS
        encoding - the string encoding format that tilesheet uses.

        other parameters same as load_tileset.

    RETURNS void

--- soundset ---
play_sound(key):
    DESC
        plays a sound.

    PARAMS
        key - self-explanatory

    RETURNS void

load_sound(key, sound):
    DESC
        adds a sound to sound dict.

    PARAMS
        key
        sound

    RETURNS void

load_dir(dirpath):
    DESC
        loads all .wav files from a directory, and loads them with the file name as key.

    PARAMS:
        dirpath - path to directory

    RETURNS void

--- elements ---
Sprite(self, constructor, interval, variance, group = 0):
