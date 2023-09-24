@echo off
title Toon Island Aftermath Panda3D Builder
if not exist thirdparty/win-nsis (
    echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    echo Fetching ThirdParty Dependencies
    echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
    if not exist panda3d-1.10.9-tools-win64.zip ( 
        "thirdparty\win-wget\wget" https://www.panda3d.org/download/panda3d-1.10.9/panda3d-1.10.9-tools-win64.zip
    )
    if not exist panda3d-1.10.9 ( 
        "thirdparty\win-7zip\7z" x panda3d-1.10.9-tools-win64.zip
    )
    robocopy "panda3d-1.10.9\thirdparty" "thirdparty" /E /NFL /MOVE
    rmdir /q panda3d-1.10.9
)

echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Building Panda3D
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
set /P THREADS="Thread Count: "
"thirdparty\win-python3.9-x64\python" makepanda/makepanda.py --everything --installer --msvc-version=14.2 --windows-sdk=10 --no-eigen --threads=%THREADS%
PAUSE