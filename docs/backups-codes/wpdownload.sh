#!/bin/bash

#cd datafpn
dirs=`ls datafpn/`

dtime=`date -d -I +%d_%m_%y`
echo "Download page.. tom $dtime"

mkdir -v datafpn/bbc/$dtime
curl 'https://www.bbc.com/portuguese' -o datafpn/bbc/$dtime/bbc.html

mkdir -v datafpn/band/$dtime
curl 'https://www.band.uol.com.br/' -o datafpn/band/$dtime/band.html

mkdir -v datafpn/cnn/$dtime
curl 'https://www.cnnbrasil.com.br/' -o datafpn/cnn/$dtime/cnn.html


mkdir -v datafpn/g1/$dtime
curl 'https://g1.globo.com/' -o datafpn/g1/$dtime/g1.html
