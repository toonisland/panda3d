#!/bin/bash
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Installing Panda3D
echo = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
echo Mounting DMG...
"/usr/bin/hdiutil" attach Panda3D-1.11.0-py3.10.dmg
echo Running Installer...
sudo installer -pkg "/Volumes/Panda3D SDK 1.11.0/Panda3D.mpkg" -verboseR -target "/Library/Developer/"
echo Detaching...
"/usr/bin/hdiutil" detach "/Volumes/Panda3D SDK 1.11.0" -force
echo Installed
