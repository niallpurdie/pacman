import os, sys, time, pygame, numpy
from pygame import *
from numpy import *
pygame.init()
size = width, height = 224, 288
screen = pygame.display.set_mode(size)
FPS=20
fpsClock=pygame.time.Clock()
pygame.key.set_repeat(1,1)
pygame.display.set_caption('Pac-Man')
debugMaze = True
dirLeft = 1    #0001
dirRight = 2   #0010
dirUp = 4      #0100
dirDown = 8    #1000 

if debugMaze:
    os.remove("debug.txt")
    file = open("debug.txt", "a")
    file.write("Dir \t Coords \t Current Pos \t Next Pos \t Validity \n")
    file.write("=== \t ====== \t =========== \t ======== \t ======== \n")
    file.close()

# draw maze, define valid moves, pellets
mazesprite = array([( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0),
                    ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0),
                    ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0),
                    ( 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 2, 2, 2, 2,
                      2, 2, 2, 2, 2, 2, 2, 2, 5), 
                    ( 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 9), 
                    ( 6, 0, 10, 11, 11, 12, 0, 10, 11, 11, 11, 12, 0, 7, 8, 0, 
                      10, 11, 11, 11, 12, 0, 10, 11, 11, 12, 0, 9), 
                    ( 6, 0, 7, 0, 0, 8, 0, 7, 0, 0, 0, 8, 0, 7, 8, 0, 7, 0, 0, 
                      0, 8, 0, 7, 0, 0, 8, 0, 9), 
                    ( 6, 0, 13, 14, 14, 15, 0, 13, 14, 14, 14, 15, 0, 13, 15, 0, 
                      13, 14, 14, 14, 15, 0, 13, 14, 14, 15, 0, 9), 
                    ( 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0, 9), 
                    ( 6, 0, 10, 11, 11, 12, 0, 10, 12, 0, 10, 11, 11, 11, 11, 
                      11, 11, 12, 0, 10, 12, 0, 10, 11, 11, 12, 0, 9), 
                    ( 6, 0, 13, 14, 14, 15, 0, 7, 8, 0, 13, 14, 14, 12, 16, 14,
                      14, 15, 0, 7, 8, 0, 13, 14, 14, 15, 0, 9), 
                    ( 6, 0, 0, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0, 
                      7, 8, 0, 0, 0, 0, 0, 0, 9), 
                    ( 17, 18, 18, 18, 18, 12, 0, 7, 13, 11, 11, 12, 0, 7, 8, 0, 
                      10, 11, 11, 15, 8, 0, 10, 18, 18, 18, 18, 20), 
                    ( 0, 0, 0, 0, 0, 6, 0, 7, 16, 14, 14, 15, 0, 13, 15, 0, 13,
                      14, 14, 12, 8, 0, 9, 0, 0, 0, 0, 0), 
                    ( 0, 0, 0, 0, 0, 6, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      7, 8, 0, 9, 0, 0, 0, 0, 0), 
                    ( 0, 0, 0, 0, 0, 6, 0, 7, 8, 0, 25, 18, 18, 29, 29, 18, 18, 
                      26, 0, 7, 8, 0, 9, 0, 0, 0, 0, 0), 
                    ( 2, 2, 2, 2, 2, 15, 0, 13, 15, 0, 9, 0, 0, 0, 0, 0, 0, 6, 
                      0, 13, 15, 0, 13, 2, 2, 2, 2, 2), 
                    ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 6, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0, 0), 
                    ( 18, 18, 18, 18, 18, 12, 0, 10, 12, 0, 9, 0, 0, 0, 0, 0, 0,
                      6, 0, 10, 12, 0, 10, 18, 18, 18, 18, 18), 
                    ( 0, 0, 0, 0, 0, 6, 0, 7, 8, 0, 27, 2, 2, 2, 2, 2, 2, 28, 0,
                      7, 8, 0, 9, 0, 0, 0, 0, 0), 
                    ( 0, 0, 0, 0, 0, 6, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      7, 8, 0, 9, 0, 0, 0, 0, 0), 
                    ( 0, 0, 0, 0, 0, 6, 0, 7, 8, 0, 10, 11, 11, 11, 11, 11, 11, 
                      12, 0, 7, 8, 0, 9, 0, 0, 0, 0, 0), 
                    ( 1, 2, 2, 2, 2, 15, 0, 13, 15, 0, 13, 14, 14, 12, 16, 14, 
                      14, 15, 0, 13, 15, 0, 13, 2, 2, 2, 2, 5), 
                    ( 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0, 9), 
                    ( 6, 0, 10, 11, 11, 12, 0, 10, 11, 11, 11, 12, 0, 7, 8, 0, 
                      10, 11, 11, 11, 12, 0, 10, 11, 11, 12, 0, 9), 
                    ( 6, 0, 13, 14, 12, 8, 0, 13, 14, 14, 14, 15, 0, 13, 15, 0, 
                      13, 14, 14, 14, 15, 0, 7, 16, 14, 15, 0, 9), 
                    ( 6, 0, 0, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 7, 8, 0, 0, 0, 9), 
                    ( 22, 11, 12, 0, 7, 8, 0, 10, 12, 0, 10, 11, 11, 11, 11, 11,
                      11, 12, 0, 10, 12, 0, 7, 8, 0, 0, 11, 24), 
                    ( 21, 14, 15, 0, 13, 15, 0, 7, 8, 0, 13, 14, 14, 12, 16, 14,
                      14, 15, 0, 7, 8, 0, 13, 15, 0, 13, 14, 23), 
                    ( 6, 0, 0, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0, 
                      7, 8, 0, 0, 0, 0, 0, 0, 9), 
                    ( 6, 0, 10, 11, 11, 11, 11, 15, 13, 11, 11, 12, 0, 7, 8, 0,
                      10, 11, 11, 15, 13, 11, 11, 11, 11, 12, 0, 9), 
                    ( 6, 0, 13, 14, 14, 14, 14, 14, 14, 14, 14, 15, 0, 13, 15, 
                      0, 13, 14, 14, 14, 14, 14, 14, 14, 14, 15, 0, 9), 
                    ( 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0, 9), 
                    ( 17, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 
                      18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 20), 
                    ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0, 0), 
                    ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0, 0)])
# 1 Un-used Tile; 0 Straight; 5 Left Up; 9 Left Down; 6 Right Up; 10 Right Down;
# 7 Left Right Up; 11 Left Right Down; 13 Left Up Down; 14 Right Up Down; 
# 15 Left Right Up Down
maze = array([( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1),
              ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1),
              ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1), 
              ( 1, 10, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 9, 1, 1, 10, 0, 0, 0, 0, 
                0, 11, 0, 0, 0, 0, 9, 1), 
              ( 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                0, 1, 1, 1, 1, 0, 1), 
              ( 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                0, 1, 1, 1, 1, 0, 1),
              ( 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                0, 1, 1, 1, 1, 0, 1), 
              ( 1, 14, 0, 0, 0, 0, 15, 0, 0, 11, 0, 0, 7, 0, 0, 7, 0, 0, 11, 0, 
                0, 15, 0, 0, 0, 0, 13, 1), 
              ( 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 0, 1), 
              ( 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 0, 1),
              ( 1, 6, 0, 0, 0, 0, 13, 1, 1, 6, 0, 0, 9, 1, 1, 10, 0, 0, 5, 1, 1, 
                14, 0, 0, 0, 0, 5, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 10, 0, 0, 7, 0, 0, 7, 0, 0, 9, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 1, 1),
              ( 0, 0, 0, 0, 0, 0, 15, 0, 0, 13, 1, 1, 1, 1, 1, 1, 1, 1, 14, 0, 
                0, 15, 0, 0, 0, 0, 0, 0), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 14, 0, 0, 0, 0, 0, 0, 0, 0, 13, 1, 1, 
                0, 1, 1, 1, 1, 1, 1),
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 1, 1, 1, 1), 
              ( 1, 10, 0, 0, 0, 0, 15, 0, 0, 7, 0, 0, 9, 1, 1, 10, 0, 0, 7, 0, 
                0, 15, 0, 0, 0, 0, 9, 1), 
              ( 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                0, 1, 1, 1, 1, 0, 1), 
              ( 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                0, 1, 1, 1, 1, 0, 1), 
              ( 1, 6, 0, 9, 1, 1, 14, 0, 0, 11, 0, 0, 7, 0, 0, 7, 0, 0, 11, 0, 
                0, 13, 1, 1, 10, 0, 5, 1), 
              ( 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 0, 1, 1, 1), 
              ( 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 
                0, 1, 1, 0, 1, 1, 1), 
              ( 1, 10, 0, 7, 0, 0, 5, 1, 1, 6, 0, 0, 9, 1, 1, 10, 0, 0, 5, 1, 1,
                6, 0, 0, 7, 0, 9, 1), 
              ( 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 0, 1), 
              ( 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 0, 1), 
              ( 1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 5, 1), 
              ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1), 
              ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                1, 1, 1, 1, 1, 1, 1)])
# 0 No Pellet; 1 Pellet; 2 Power Pellet
pellet = array([( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                ( 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 0),
                ( 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 1, 0),
                ( 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 2, 0),
                ( 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 1, 0),
                ( 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 0),
                ( 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                  1, 0, 0, 0, 0, 1, 0),
                ( 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                  1, 0, 0, 0, 0, 1, 0),
                ( 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0,
                  1, 1, 1, 1, 1, 1, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 0, 0),
                ( 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 0),
                ( 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 1, 0),
                ( 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                  1, 0, 0, 0, 0, 1, 0),
                ( 0, 2, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1,
                  1, 0, 0, 1, 1, 2, 0),
                ( 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                  1, 0, 0, 1, 0, 0, 0),
                ( 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                  1, 0, 0, 1, 0, 0, 0),
                ( 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0,
                  1, 1, 1, 1, 1, 1, 0),
                ( 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 0),
                ( 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 1, 0),
                ( 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1, 1, 0),
                ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0),
                ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0)])
# draw maze
rows = mazesprite.shape[0]
columns = mazesprite.shape[1]
x = y = 0
for element in mazesprite.flat:
    if element:
        sprite = "maze" + str(element) + ".png"
        gimp = pygame.image.load(sprite).convert()
        screen.blit(gimp, ((x*8),(y*8)))
    x += 1
    if x == columns:
        x = 0
        y += 1
pygame.display.flip()
up1Sprite = pygame.image.load('1up.png').convert()
screen.blit(up1Sprite, (24,0))
scoreSprite = pygame.image.load('0.png').convert()
screen.blit(scoreSprite, (36,8))
screen.blit(scoreSprite, (44,8))
#readySprite = pygame.image.load('ready.png').convert()
#screen.blit(readySprite, (88,156))
# pupulate pellets
x = y = 0
rows = pellet.shape[0]
columns = pellet.shape[1]
for element in pellet.flat:
    if element:
        if element == 2:
            gimp = pygame.image.load('powerPellet.png').convert()
            screen.blit(gimp, ((x*8),(y*8)))
        else:
            gimp = pygame.image.load('pellet.png').convert()
            screen.blit(gimp, ((x*8),(y*8)))       
    x += 1
    if x == columns:
        x = 0
        y += 1
pygame.display.flip()
sound = pygame.mixer.Sound('pacman_beginning.wav')
sound.play()

class pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        pygame.sprite.Sprite.__init__(self)
        self.bitmap = pygame.image.load("pacmanL1.png").convert_alpha()
        self.pacmanRect = self.bitmap.get_rect()
        self.pacmanRect.topleft = [104,204] # 14 X 8 - 8 26 X 8 - 8
        #self.pacmanRect.centre = [108,208]
    
    def move(self, x, y):
        self.pacmanRect.left += x
        self.pacmanRect.top += y
        
    def render(self, direction):
        if direction == dirLeft:
            self.bitmap = pygame.image.load("pacmanL1.png", transparent).convert_alpha()
        elif direction == dirRight:
            self.bitmap = pygame.image.load("pacmanR1.png", transarent).convert_alpha()
        elif direction == dirUp:
                self.bitmap = pygame.image.load("pacmanU1.png", transparent).convert_alpha() 
        else:
                self.bitmap = pygame.image.load("pacmanD1.png", transparent).convert_alpha()                 
        screen.blit(self.bitmap, (self.pacmanRect))
        pygame.display.update()
        pygame.display.flip()
        

     
    def legaldirection(self, direction):
        
        #0001 (Left) 	1
        #0010 (Right) 	2
        #0100 (Up) 	4
        #1000 (Down) 	8
        x = (self.pacmanRect.left + 16) / 8
        y = (self.pacmanRect.top + 16) / 8
        if direction == 1:
            x = (self.pacmanRect.left + 20) / 8
            y = (self.pacmanRect.top + 16) / 8        
        elif direction == 2:
            x = (self.pacmanRect.left + 12) / 8
            y = (self.pacmanRect.top + 16) / 8
        elif direction == 4:
            x = (self.pacmanRect.left + 16) / 8
            y = (self.pacmanRect.top + 19) / 8 
        elif direction == 8:
            x = (self.pacmanRect.left + 16) / 8
            y = (self.pacmanRect.top + 13) / 8          
            
        file = open("debug.txt", "a")
      
        #print "Binary of the direction is " + bin(direction)
        #print "Binary of the tile in the array is " + bin(maze[y-1,x-1])
        def writeMazeDetailsToFile(x,y):
            file.write("Left \t" + "(" + str(self.pacmanRect.left) + 
                                       ", " + str(self.pacmanRect.top) + 
                                       ") \t (" + str(x - 1) + ", " + 
                                       str(y - 1) + ")=" + str(maze[y-1,x-1]) + 
                                       "\t (" + str(x-2) + ", " + str(y-1) + 
                                       ")=" + str(maze[y-1,x-2]) + "\t")            
        if direction == 1:            
            if debugMaze:
                file.write("Left \t" + "(" + str(self.pacmanRect.left) + 
                           ", " + str(self.pacmanRect.top) + ") \t (" +
                           str(x - 1) + ", " + str(y - 1) + ")=" + 
                           str(maze[y-1,x-1]) + "\t (" + str(x-2) + ", " + 
                           str(y-1) + ")=" + str(maze[y-1,x-2]) + "\t")
            if maze[y-1,x-2] == 1:
                if debugMaze:
                    file.write("Next Tile invalid - attempt to go left denied\n")
                    file.close()
                return False   
        elif direction == 2:
            if debugMaze:
                file.write("Right \t" + "(" + str(self.pacmanRect.left) + ", " + 
                           str(self.pacmanRect.top) + ") \t (" + str(x - 1) + 
                           ", " + str(y - 1) + ")=" + str(maze[y-1,x]) 
                           + "\t (" + 
                           str(x) + ", " + str(y-1) + ")=" + str(maze[y-1,x]) 
                           + "\t")   
            if maze[y-1,x] == 1:
                if debugMaze:
                    file.write("Next Tile invalid - attempt to go right denied \n")
                    file.close()
                return False
        elif direction == 4:
            if debugMaze:
                file.write("Up \t" + "(" + str(self.pacmanRect.left) + ", " + 
                           str(self.pacmanRect.top) + ") \t (" + str(x - 1) + 
                           ", " + str(y - 1) + ")=" + str(maze[y-2,x-1]) + 
                           "\t (" + str(x-1) + ", " + str(y-2) + ")=" + 
                           str(maze[y-2,x-1]) + "\t")
            if maze[y-2,x-1] == 1:
                if debugMaze:
                    file.write("Next Tile invalid - attempt to go up denied \n")
                    file.close()
                return False
        elif direction == 8:
            if debugMaze:
                file.write("Down \t" + "(" + str(self.pacmanRect.left) + ", " + 
                           str(self.pacmanRect.top) + ") \t (" + str(x - 1) + 
                           ", " + str(y - 1) + ")=" + str(maze[y,x-1]) + 
                           "\t (" + str(x-1) + ", " + str(y) + ")=" + 
                           str(maze[y,x-1]) + "\t")            
            if maze[y,x-1] == 1:
                if debugMaze:
                    file.write("Next Tile invalid - attempt to go down denied \n")
                    file.close()
                return False       

        if maze[y-1,x-1] == 0:
            if debugMaze:
                file.write("Direction valid \n")
                file.close()
            return True
        elif bin(direction & maze[y-1,x-1]) <> 0:
            if debugMaze:
                file.write("Direction valid \n")
                file.close()            
            return True
        else:
            if debugMaze:
                file.write("Direction invalid \n")
                file.close() 
            return False
        
        #*******************************************8
        #NEED TO CHECK IF checking all JUNCTIONS above
        #NEED to write procedures to change sprite based on Direction and animation sequence
        #NEED TO check FPS is too fast so that all methods are being called.
        #NEED TO change dispay to Blit only the RECT rather than all display
        #      rewrote maze to 8x8 array need check
        #      still same problem
        # need rewrite keystroke continue direction until next key down or dead end
        
    

pac = pacman()
pac.render(dirLeft)


    
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                #0100 (Up) 	4
                if pac.legaldirection(4):
                    pac.move(0,-1)
                    pac.render(dirUp)
            elif event.key == pygame.K_DOWN:
                #1000 (Down) 	8
                if pac.legaldirection(8):
                    pac.move(0,1)
                    pac.render(dirDown)
            if event.key == pygame.K_RIGHT:
                #0010 (Right) 	2
                if pac.legaldirection(2):
                    pac.move(1,0)
                    pac.render(dirRight)
            if event.key == pygame.K_LEFT:
                #0001 (Left) 	1
                if pac.legaldirection(1):
                    pac.move(-1,0)
                    pac.render(dirLeft)

        pygame.display.update()
        fpsClock.tick(FPS)    