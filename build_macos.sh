#!/bin/bash
if [ ! -d "thirdparty/darwin-libs-a" ]; then
  echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
  echo Fetching ThirdParty Dependencies
  echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
  curl https://www.panda3d.org/download/panda3d-1.10.10/panda3d-1.10.10-tools-mac.tar.gz -O -J -L
  tar -xf "panda3d-1.10.10-tools-mac.tar.gz" "panda3d-1.10.10/thirdparty"
  rsync -a "panda3d-1.10.10/thirdparty/" "thirdparty/"
  rm -r panda3d-1.10.10*
fi

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Building Panda3D
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
read -p "Threads: " T
python3 makepanda/makepanda.py --everything --installer --no-fmod --threads=$T