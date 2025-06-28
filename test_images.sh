#/bin/bash
# using ImageMagick version 7 to create some test images
magick -size 400x400 radial-gradient:red-yellow    -gravity center -fill white -pointsize 72 -annotate 0 "1" img/number_1.png
magick -size 640x480 radial-gradient:blue-green    -gravity center -fill white -pointsize 72 -annotate 0 "2" img/number_2.png
magick -size 200x800 radial-gradient:purple-orange -gravity center -fill white -pointsize 72 -annotate 0 "3" img/number_3.png
magick -size 800x200 radial-gradient:cyan-magenta  -gravity center -fill white -pointsize 72 -annotate 0 "4" img/number_4.png
magick -size 600x100 radial-gradient:lime-pink     -gravity center -fill white -pointsize 72 -annotate 0 "5" img/number_5.png
