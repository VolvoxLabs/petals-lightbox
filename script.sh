#!/bin/bash
python process-video.py frame.txt bouncingBall1.mov &
python process-video.py frame2.txt bouncingBall2.mov &
python process-video.py frame3.txt bouncingBall3.mov 

sudo PYTHONPATH=".:build/lib.linux-mv7l-2.7" python led-playback.py
