First time using pygame for me, here is how I approached the creation of the game:

- First I coded along a freeCode Camp tutorial.
[Pygame Tutorial for Beginners - Python Game Development Course - YouTube.url](..%2F..%2F..%2F..%2FAppData%2FLocal%2FTemp%2F%2820%29%20Pygame%20Tutorial%20for%20Beginners%20-%20Python%20Game%20Development%20Course%20-%20YouTube.url)

- Secondly, modified the game to my pleasure creating classes and changing images and other features.

- Finally, I watched a short tutorial on how to create a menu in pygame and reorganized the whole code.
[HOW TO MAKE A MENU SCREEN IN PYGAME! - YouTube.url](..%2F..%2F..%2F..%2FAppData%2FLocal%2FTemp%2F%2820%29%20HOW%20TO%20MAKE%20A%20MENU%20SCREEN%20IN%20PYGAME%21%20-%20YouTube.url)

The game starts in a menu where the user can select to play in 3 different levels using the mouse. Once a level is
selected the user starts playing with the left and right arrows to move the spaceship and the space bar for shooting
bullets. In the gaming screen there are also 2 buttons which can be clicked: One for going back to the menu to select 
another level and another one for quiting the game.

During the game the score is shown in the top left corner and it increases every time a bullet hits an enemy. The user
is only allowed to shoot one bullet at a time and has to wait for it to hit an enemy or get to the top of the screen to
be able to shot again. If any enemies move from on side to another of the screen (starting randomly) and each time they
get to the side of the screen they bounce back but getting closer to the spaceship in the y-axis. If any enemy gets to
the y-axis position of the spaceship it's game over: All the enemies disappear and a "GAME OVER" text is shown in the
center of the screen.

LEVELS:

- Level 1 has 6 enemies.

- Level 2 has 8 enemies and the movement speed of enemies and spaceship are increased.

- Level 3 has 10 enemies speeds are increased for enemies, spaceship and bullets.
