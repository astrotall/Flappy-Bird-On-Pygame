import pygame
import random
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def collision(x1, y1, w1, h1, x2, y2, w2, h2):
    if x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2:
        return True


size = (480, 640)
window = pygame.display.set_mode(size)

pygame.font.init()
pygame.mixer.init()
font = pygame.font.SysFont(resource_path("Multiround Pro.otf"), 100)
font2 = pygame.font.SysFont(resource_path("Multiround Pro.otf"), 50)

bird1 = pygame.image.load(resource_path("1.png"))
bird2 = pygame.image.load(resource_path("2.png"))
bird3 = pygame.image.load(resource_path("3.png"))
bird_anim = [bird1, bird2, bird3, bird2]
bird_anim_ = []
bird_ind = 0
bird_anim_speed = 0.3
bird_x = 210 - 28
bird_y = 320 - 20
bird_w = 50  # 33
bird_h = 40  # 23
bird_angle = 14
bird_sound = pygame.mixer.Sound(resource_path("bird jump.mp3"))
for angle in range(30, -91, -7):
    images = []
    for img in bird_anim:
        new_img = pygame.transform.scale(img, [bird_w, bird_h])
        new_img = pygame.transform.rotate(new_img, angle)
        images.append(new_img)

    bird_anim_.append(images)
    if angle == 30:
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
        bird_anim_.append(images)
# print(bird_anim_)

bg = pygame.image.load(resource_path("4622710.png"))
bg = pygame.transform.scale(bg, size)
bg_x, bg_y = 0, 0
pygame.mixer.music.load(resource_path("music.mp3"))
pygame.mixer.music.play(-1)

road = pygame.image.load(resource_path("road.png"))
road_x, road_x2 = 0, 480
road_speed = 3

pipe_w, pipe_h = 80, 620
gap = 130
pipe_up = pygame.image.load(resource_path("up_pipe.png"))
pipe_down = pygame.image.load(resource_path("down_pipe.png"))
pipe_up, pipe_down = pygame.transform.scale(pipe_up, [pipe_w, pipe_h]), pygame.transform.scale(pipe_down,
                                                                                               [pipe_w, pipe_h])
min_pipe_y = -520
max_pipe_y = size[1] - 100 - gap - pipe_h
pipe_x, pipe_y = 801, random.randint(min_pipe_y, max_pipe_y)

pipe_w2, pipe_h2 = 80, 620
gap2 = 130
pipe_up2 = pygame.image.load(resource_path("up_pipe.png"))
pipe_down2 = pygame.image.load(resource_path("down_pipe.png"))
pipe_up2, pipe_down2 = pygame.transform.scale(pipe_up2, [pipe_w2, pipe_h2]), pygame.transform.scale(pipe_down2,
                                                                                                    [pipe_w2, pipe_h2])
min_pipe_y2 = -520
max_pipe_y2 = size[1] - 100 - gap2 - pipe_h2
pipe_x2, pipe_y2 = pipe_x + pipe_x // 2 - 1, random.randint(min_pipe_y2, max_pipe_y2)
pipe_dynamic = False

death_sound = pygame.mixer.Sound(resource_path("death_bird.mp3"))
death_sound_flag = False

restart_button = pygame.image.load(resource_path("restart.png"))
exit_button = pygame.image.load(resource_path("exit.png"))

gravity = 5
jump = False
jump_height_max = 14
jump_height = jump_height_max

score = 0
file = open(resource_path("record.txt"), "r")
best_score = int(file.read())
file.close()

state_game = True

ico = pygame.image.load(resource_path("2.ico"))
pygame.display.set_caption("Flappy bird")
pygame.display.set_icon(ico)

run = True
while run:
    score_text = font.render(str(score), True, [255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state_game:
                pipe_dynamic = True
                jump = True
                jump_height = jump_height_max
                bird_angle = 0
                bird_sound.play()
            if event.key == pygame.K_BACKSLASH:
                score += 1
        if event.type == pygame.MOUSEBUTTONDOWN and state_game:
            if event.button == 1:
                pipe_dynamic = True
                jump = True
                jump_height = jump_height_max
                bird_angle = 0
                bird_sound.play()
        if event.type == pygame.MOUSEBUTTONDOWN and not state_game:
            mouse_x, mouse_y = event.pos
            if 280 <= mouse_y <= 280 + 47:
                if 70 <= mouse_x <= 70 + 134:
                    bird_x = 210 - 28
                    bird_y = 320 - 20
                    pipe_x, pipe_y = 801, random.randint(min_pipe_y, max_pipe_y)
                    pipe_x2, pipe_y2 = pipe_x + pipe_x // 2 - 1, random.randint(min_pipe_y2, max_pipe_y2)
                    score = 0
                    pipe_dynamic = False
                    bird_angle = 14
                    pygame.mixer.music.play(-1)
                    death_sound_flag = False
                    state_game = True
                if 265 <= mouse_x <= 265 + 134:
                    run = False

    if pipe_dynamic and state_game:
        pipe_x -= 3
        pipe_x2 -= 3
        bird_y += gravity
        bird_angle += 0.5
    if bird_angle >= 27:
        bird_angle = 26

    if pipe_x < -81:
        pipe_x, pipe_y = 702, random.randint(min_pipe_y, max_pipe_y)

    if pipe_x2 < -81:
        pipe_x2, pipe_y2 = 702, random.randint(min_pipe_y2, max_pipe_y2)

    if collision(bird_x, bird_y, bird_w, bird_h, pipe_x, pipe_y, pipe_w, pipe_h):
        state_game = False

    if collision(bird_x, bird_y, bird_w, bird_h, pipe_x, pipe_y + pipe_h + gap, pipe_w, pipe_h):
        state_game = False

    if collision(bird_x, bird_y, bird_w, bird_h, pipe_x2, pipe_y2, pipe_w2, pipe_h2):
        state_game = False

    if collision(bird_x, bird_y, bird_w, bird_h, pipe_x2, pipe_y2 + pipe_h2 + gap2, pipe_w2, pipe_h2):
        state_game = False

    if bird_y < 0 and pipe_x <= bird_x <= pipe_x + pipe_w:
        state_game = False

    if bird_y < 0 and pipe_x2 <= bird_x <= pipe_x2 + pipe_w2:
        state_game = False

    if bird_y + bird_h >= 563:
        state_game = False

    if pipe_x == 150 or pipe_x2 == 150 and state_game:
        score += 1

    if jump:
        bird_y -= jump_height
        jump_height -= 1
        if jump_height < 0:
            jump = False
            jump_height = jump_height_max
    if state_game:
        bird_ind += bird_anim_speed
    if bird_ind >= 4:
        bird_ind = 0
    if state_game:
        road_x -= road_speed
        road_x2 -= road_speed
    if road_x <= -480:
        road_x = 480
    if road_x2 <= -480:
        road_x2 = 480

    #   print(pipe_x, pipe_x2)

    window.blit(bg, [bg_x, bg_y])
    window.blit(pipe_up, [pipe_x, pipe_y])
    window.blit(pipe_down, [pipe_x, pipe_y + pipe_h + gap])
    window.blit(pipe_up2, [pipe_x2, pipe_y2])
    window.blit(pipe_down2, [pipe_x2, pipe_y2 + pipe_h2 + gap2])
    window.blit(bird_anim_[int(bird_angle)][int(bird_ind)], [bird_x, bird_y])
    window.blit(road, [road_x, 563])
    window.blit(road, [road_x2, 563])
    if state_game:
        score_text_width = score_text.get_width()
        window.blit(score_text, [size[0] // 2 - score_text_width // 2, 60])
    else:
        if not death_sound_flag:
            death_sound_flag = True
            death_sound.play()
        pygame.mixer.music.stop()
        if score > best_score:
            best_score = score
            file = open(resource_path("record.txt"), "w")
            file.write(str(best_score))
            file.close()
        score_text = font2.render("score: " + str(score), True, [255, 255, 255])
        score_text2 = font2.render("best: " + str(best_score), True, [255, 255, 255])
        score_text_width = score_text.get_width()
        score_text_width2 = score_text2.get_width()
        window.blit(score_text, [size[0] // 2 - score_text_width // 2, 130])
        window.blit(score_text2, [size[0] // 2 - score_text_width2 // 2, 160])
        #        mouse_pos = pygame.mouse.get_pos()
        window.blit(restart_button, [70, 280])
        window.blit(exit_button, [265, 280])
    #        pygame.display.set_caption(str(mouse_pos))
    # window.blit(bird_anim_[0][0], [0, 0])
    pygame.display.update()
    pygame.time.delay(20)