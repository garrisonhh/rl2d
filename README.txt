=== RL2D by garrisonhh ===
made for my own fast prototyping with pretty tileset graphics :)

=== documentation ===
--- rl2d.tileset ---
get_tile(key)
    key - key for tileset

    returns pg.Surface.

load_tile(sheet, key, rect = 0, palette = 0, fg = None, bg = None)
    sheet - pg.Surface
    key - key for tileset
    rect - if passed, tileset will assign a subsurface of rect to key instead of whole surface.
    palette - if passed, fg and bg will replace non-black and black
    fg - foreground color from palette
    bg - background color from palette. if not passed, image will be transparent

    void.

load_tileset(tilesize, tilesheet, definitions, palette = 0)
    tilesize - tuple(int width, int height)
    tilesheet - path to image
    definitions* - path to tile definitions text file
    palette - self-explanatory

    void.

    *definitions look like this:
    ; this is a comment
    key x y ; no palette
    key x y fg ; yes palette, white -> fg, black -> transparent
    key x y fg bg ; yes palette, white -> fg, black -> bg

    one load_sheet() call, one tilesize. u can load multiple sized images
    using multiple load_sheet() or load_tile() calls

load_font(charsize, tilesheet, encoding = 'ascii', palette = 0, fg = None, bg = None)
    encoding - the string encoding format that tilesheet uses.
    other parameters same as load_tileset.

    void.
