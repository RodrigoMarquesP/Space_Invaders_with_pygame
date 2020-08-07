# Space Invaders with pygame
A complete project of a space invaders game developed in python with pygame

This project was focused in develop a high indented code of a full game in python using pygame.
It's made in a structural shape instead of object oriented - which are maybe the more recomended.  
The sounds, musics, icons and the font are included for those who wanna test the code.

**The game is composed by:**  
* Color pulsing background
* Four pixel stars running down at the backgroud
* Four spinning meteors that instantly cause game over
* A sorted color battleship
* Bullets from the battleship
* Three maximum lifes of the battleship (shields)
* A heat marker for the shooting mechanism, that limits the fire rate
* Spawning enemies at the top of the screen those give 10 points when destroied
* Enemies blast shoots
* Four randomly generated power-ups (Bomb, Shield, Points, Speed)
* The **Bomb** power-up explodes all actual enemys at the screen
* The **Shield** power-up add a shield if there are less than three
* The **Points** power-up give 100 points
* The **Speed** power-up accelerate everything in the game, making it harder, but much funnier

A executable can be generated for the game, following the steps:

1. Install pyInstaller module  
2. run  ``pyInstaller -F -c --hidden-import="pkg_resources.py2_warn" --onefile -i"the_icon.ico" the_file.py``  

**Details:**  
* 'the_ico' must be replaced by the name of the .ico file and 'the_file' must be the name of the python file, which will be the .exe name too.  
* The hidden import of pkg_resources.py2_warn was due to an error that i found creating the executable, but may be already fixed when you're running yourself.  
* While developing your own applications, a good place to look for icons is <https://www.flaticon.com/>.  
* During execution in energy economy it can present performance drop, i'm sorry about that, but fell free to study pygame documentation to fix this problem.
