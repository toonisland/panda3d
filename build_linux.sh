#!/bin/bash
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Building Panda3D
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
read -p "Threads: " T
python3 makepanda/makepanda.py --everything --installer --no-fmod --threads=$T
