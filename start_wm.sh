#!/bin/bash

# Start WM from env specs

if [ "$XINITRC" != "" ] ; then
    export XINITRC=$XINITRC
else
    XINITRC=./xinitrc
fi
if [ "$WM" != "" ] ; then
    export WM=$WM
else
    export WM=./tinywm
fi

#echo Starting X with: $XINITRC $WM

XEPHYR=$(whereis -b Xephyr | cut -f2 -d' ')
xinit $XINITRC -- \
    "$XEPHYR" \
        :100 \
        -ac \
        -screen 800x600 \
        -host-cursor