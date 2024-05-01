import os
import pygame
from math import cos, sin


white = (255, 255, 255)
black = (0, 0, 0)

os.environ['SDL_VIDEO_CENTERED'] =  '1'
RES = WIDTH, HEIGHT = 1000, 800
FPS = 60

pixel_width = 20
pixel_height = 20

x_pixel = 0
y_pixel = 0

screen_width = WIDTH // pixel_width
screen_height = HEIGHT // pixel_height
screen_size = screen_width * screen_height
#print(screen_width, screen_height, screen_size)

A, B = 0, 0

teta_spacing = 10
fi_spacing = 3
chars = ".,-~:;=!*#$@"

r1 = 10
r2 = 20
k2 = 200
k1 = screen_height * k2 * 3 / (8 * (r1 + r2))
#print(k1)

pygame.init()

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
pygame.display.set_caption('Donut')
font = pygame.font.SysFont('Arial', 20, bold=True)

def text_display(char, x, y):
    text = font.render(str(char), True, white)
    text_rect = text.get_rect(center=(x,y))
    screen.blit(text, text_rect)

paused = False
running = True

k = 0

while running:
    clock.tick(FPS)
    pygame.display.set_caption("FPS: {:.2f}".format(clock.get_fps()))
    screen.fill(black)

    #SPACE TO CODE
    #text_display("Donut", WIDTH/2, HEIGHT/2)
    output = [' '] * screen_size
    zbuffer = [0] * screen_size

    for teta in range(0, 628, teta_spacing):
        for fi in range(0, 628, fi_spacing):

            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            costeta = cos(teta)
            sinteta = sin(teta)
            cosfi = cos(fi)
            sinfi = sin(fi)

            circlex = r2 + r1 * costeta
            circley = r1 * sinteta

            #x = circlex * cosfi
            #y = circley
            #z = k2 + circlex * sinfi
            #ooz = 1 / z

            #x = circlex * sinfi
            #y = circlex * cosfi
            #z = k2 + circley
            #ooz = 1 / z

            x = circlex * (cosB * cosfi + sinA * sinB * sinfi) - circley * cosA * sinB
            y = circlex * (sinB * cosfi - sinA * cosB * sinfi) + circley * cosA * cosB
            z = k2 + cosA * circlex * sinfi + circley * sinA
            ooz = 1 / z

            xp = int(screen_width / 2 + k1 * ooz * x) 
            yp = int(screen_height / 2 - k1 * ooz * y)

            position = xp + screen_width * yp

            L = cosfi * costeta * sinB - cosA * costeta * sinfi - sinA * sinteta + cosB * (
                cosA * sinteta - costeta * sinA * sinfi)
            
            if ooz > zbuffer[position]:
                zbuffer[position] = ooz
                luminecence_index = int(L * 8)
                output[position] = chars[luminecence_index if luminecence_index > 0 else 0]

            #output[position] = '*'


    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display (output[k], x_pixel, y_pixel)
            k += 1
        x_pixel = 0
    y_pixel = 0
    k = 0

    A += 0.2
    B += 0.035

    if not paused:
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = not paused