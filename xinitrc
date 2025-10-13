# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# xinitrc file for testing our window manager.

# 1. Start some programs to play with.
xeyes -geometry +10+10 &
xclock -geometry 120x120+120+400 &
xterm -geometry 100x100+100+100 &
#sleep 1 && xterm -geometry +500+300 &
#sleep 1 && /usr/bin/mousepad &

# 2. Start our window manager.
#export GLOG_logtostderr=1
#sleep 1
./window.py -d :100

