# PROJECT UNDER DEVELOPMENT 

# OpenCalculator

## Description
OpenCalculator is an open source calculator and plotter, created by me using Python and Pygame, re and math libraries.

## Installation
1. Download the whole "images" folder and "help.txt" and place it in a directory.
2. Download calculator.py and place it in the same directory and just run it, if you're using windows os, an executable version is avaiable. 
**Keep in mind the library dependencies**
If you go with calculator.py option, pygame and re have to be installed to your computer. Both of them are cross-platform. 


Furtheremore, before reading the source code I defintely suggest checking out the wiki's "GUI Explaination" page right [here.](https://github.com/KonstantinosPetrakis/OpenCalculator/wiki/GUI-explanation)

## Usage
OpenCalculator is small project which allows you to do mathematical calculations and plot a function in the x-y plane. 
<br> <br>
**Screenshots**
<br>
![Screenshot1](/wiki_files/screenshot1.jpg)
<br>
![Screenshot2](/wiki_files/screenshot2.jpg)

## Known bugs

Graph of f = 0, causes an error.

Graph of tanx, or any polynomial function has nothing to do with the regular graphs of other computer programs, because this program condiders
the boundaries of the the y axis the [-max |f|, max |f|] as  x belongs to [-12 * zoom, 12 * zoom].
So, any difference in small values is not shown in the GUI presentation, for example the graph of any polynomial will be almost equal to
the graph of its biggest term, so plot(x^3+x^2+1) ≈ plot(x^3).

I am currentlly working on a fix for this, that means I have to change the whole xy-axis values and zoom function dramatically. 
