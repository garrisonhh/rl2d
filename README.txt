===RL2D by garrisonhh===

---tile definition files---
by using load_sheet, tiles in an rl2d Scene are defined with "name x y", where x
and y refer to locations in a tilesheet:

> tree    10  5

if you submit a palette filepath, rl2d will also load a palette and replace white
with the foreground color and (optionally) black with a background color. if no
background color is submitted, the background will be transparent.

> tree    10  5   4
> tree    10  5   4   2

you can also write comments if u want:

> ; this is a comment
> tree  10  5   ; also a comment

---misc---
some great fonts to use with
https://www.gridsagegames.com/rexpaint/resources.html#Fonts
