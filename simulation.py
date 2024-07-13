import pygame
import pymunk
import pymunk.pygame_util
from Ragdoll import *

pygame.init()

width = 800
height = 800
screen_size = (width, height)
clock = pygame.time.Clock()
Fps = 120

display = pygame.display.set_mode((width, height))
space = pymunk.Space()
space.gravity = 0, 800


#Parameters regarding the dimentions of the body
Position = (500,400)
Size = (50, 100)
Limb_radius = 10
Limb_size = 80
Head_size = 30


floor = Floor(space)

runner = RagDoll(Position, Size, 10, 80, 30, space)

draw_options = pymunk.pygame_util.DrawOptions(display)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        display.fill((255, 255, 255))

        space.debug_draw(draw_options)

        
        pygame.display.update() 
        clock.tick(Fps)
        space.step(1/Fps)


            
        
main()
pygame.quit()
