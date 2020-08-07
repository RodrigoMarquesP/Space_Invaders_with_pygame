# Space Invaders with pygame
A complete project of a space invaders game developed in python with pygame

This project was focused in develop a high indented code of a full game in python using pygame.
It's made in a structural shape instead of object oriented - which are maybe the more recomended.
The sounds, musics, icons and the font are included for those who wanna test the code.

A executable can be generated from this file, following the steps:

1 - Install pyInstaller module
2 - run  ``pyInstaller -F -c --hidden-import="pkg_resources.py2_warn" --onefile -i"the_icon.ico" the_file.py``
Details:
=> 'the_ico' must be replaced by the name of the .ico file and 'the_file' must be the name of the python file, which will be the .exe name too.
=> the hidden import of pkg_resources.py2_warn was due to an error that i found creating the executable, but may be already fixed when you're running yourself.
