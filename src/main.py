import pygame
from pygame.locals import *
import random
import time
import sys
import math
from words import words
from path import get_root_path
from settings import Settings

print("starting")
pygame.init()
print("continuing")
pygame.display.init()
pygame.mixer.init()

root_path = get_root_path()

win_audios = [pygame.mixer.Sound(root_path + "/audio/kids_cheering.mp3"), pygame.mixer.Sound(root_path + "/audio/bell.wav"), pygame.mixer.Sound(root_path + "/audio/tada.mp3"), pygame.mixer.Sound(root_path + "/audio/banana.mp3"), pygame.mixer.Sound(root_path + "/audio/fart.mp3")]
loss_audio = pygame.mixer.Sound(root_path + "/audio/buzzer.mp3")

TEXT_FONT = 144
FONT_SIZE_PIXELS = int(TEXT_FONT * (4/3))

settings = Settings()

# word_count = 0

def main():
    print("main function")
    play(random.choice(words).lower())
    
def play(word):
    print(word)
    
    display = pygame.display.set_mode(size=(1000,800))
    curr_surface = pygame.display.get_surface()
    surface_height = pygame.Surface.get_height(curr_surface)
    surface_width = pygame.Surface.get_width(curr_surface)
    
    letterbox_height = surface_height//2
    letterbox_y = surface_height//2
    letterbox_top = letterbox_y - (letterbox_height//2)

    letterbox_width = surface_width//8
    letterbox_x = [surface_width//5, (2*surface_width)//5, (3*surface_width)//5, (4*surface_width)//5]
    letterbox_left = [letterbox_x[i] - (letterbox_width//2) for i in range(len(letterbox_x))]

    font = pygame.font.SysFont('chalkduster.ttf', TEXT_FONT)

    containers = [pygame.Rect(letterbox_left[i], letterbox_top, letterbox_width, letterbox_height) for i in range(len(letterbox_left))]
    letters = [font.render(char.upper(), True, (0,0,0)) for char in word]
    letter_rects = [letter.get_rect(center=(letterbox_x[i], letterbox_y)) for i, letter in enumerate(letters)]
    
    for i in range(len(word)):
        pygame.draw.rect(curr_surface, (194, 197, 204), containers[i])
        curr_surface.blit(letters[i], letter_rects[i])

    settings_img = pygame.image.load(root_path + "/images/gear.png")
    settings_img = pygame.transform.scale(settings_img, (settings_img.get_width()//2, settings_img.get_height()//2))
    curr_surface.blit(settings_img, settings_img.get_rect(bottomright=(surface_width-10, surface_height-10)))
    
    pygame.display.update()
    
    for i, char in enumerate(word):
        event = pygame.event.wait()
        while event.type not in [QUIT, KEYDOWN]:
            print(event)
            event = pygame.event.wait()
        if event.type == QUIT:
            print("quitting")
            return exitg()
        elif event.type == KEYDOWN:
            if event.key == ord(char):
                print("character correct!")
                pygame.draw.rect(curr_surface, (144, 238, 144), containers[i])
                curr_surface.blit(letters[i], letter_rects[i])
                pygame.display.update()
            else:
                print("character wrong")
                pygame.draw.rect(curr_surface, (238, 144, 144), containers[i])
                curr_surface.blit(letters[i], letter_rects[i])
                pygame.display.update()
                miss()
                return play(word)
    return win()

def win():
    print("playing win sound")
    audio = random.choices(win_audios, weights=[0.15, 0.1, 0.35, 0.35, 0.05])[0]
    audio.set_volume(settings.volume_pct)
    pygame.mixer.Sound.play(audio)
    reset()

# def launch_fireworks(max_width, max_height):
#     explode_fireworks(0, [(random.randint(width), random.randint(height)) for i in range(3)], [random.choice(COLORS) for i in range(3)], [random.randint(4, 6) for i in range(3)])

# def explode_fireworks(cycle, positions, colors, cycles):
#     if cycle == 6:
#         return
#     for i in range(min(cycle+1, 3)):
#         if cycles[i] >= cycle:
#             deploy_cycle(positions[i], colors[i])
#     time.sleep(1)
#     explode_fireworks(cycle+1, colors, positions)

# def deploy_cycle(cycle, position, color):
#     pass

def miss():
    print("playing loss sound")
    if settings.wrong_sound:
        pygame.mixer.Sound.play(loss_audio)

def reset():
    print("resetting game")
    pygame.display.get_surface().fill((0,0,0))
    pygame.display.update()
    main() # restart for next word
    pass

def exitg():
    print("exiting game")
    pygame.display.quit()
    sys.exit()

if __name__ == "__main__":
    main()