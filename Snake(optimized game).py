import multiprocessing

import pygame
import time
import random
import cv2

from fingers import HandDetector
from multiprocessing import Pipe
pygame.init()

camera = cv2.VideoCapture(0)
detector = HandDetector()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Pythonist')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 120

font_style = pygame.font.SysFont("bahnschrift", 25)
font_style_target = pygame.font.SysFont("comicsansms", 18)
score_font = pygame.font.SysFont("comicsansms", 35)
lock = multiprocessing.Lock()


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def mes_target(msg, color):
    mesg = font_style_target.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6 + 120, dis_height / 3 + 60])

def last_mes1(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6 + 65, dis_height / 3 - 15])

def last_mes2(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6 + 35, dis_height / 3 + 23])

def score(msg, color):
    mesg = score_font.render(msg, True, color)
    dis.blit(mesg, [10, 10])

def camera_work(input_c, l):
    while camera.isOpened():
        #l.acquire()
        suc, img = camera.read()
        if not suc:
            break
        cv2.imshow("IMG", img)
        finger_move = [0, 0]
        img, finger_move = detector.findHands(img, raised_rightukaz=[finger_move[0], finger_move[1]])
        if cv2.waitKey(1) == 27:
            break
            # camera_work = 0
        if l.acquire(False):
            l.release()
            input_c.send(finger_move)
        #l.release()


def gameLoop(output_c, l):
    #global s
    game_over = False
    game_close = False
    game_win = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0


    #camera_work = 1

    while not game_over:
        finger_move = output_c.recv()
        '''if camera_work < 1:
            camera_work += 1
        else:'''
        while game_close == True:

            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            mes_target("Get 15 points to win", green)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        #l.release()
                        gameLoop(output_c=output_c, l=lock)

        if finger_move[0] == -1:
            x1_change = -snake_block
            y1_change = 0
        elif finger_move[0] == 1:
            x1_change = snake_block
            y1_change = 0
        elif finger_move[1] == -1:
            y1_change = -snake_block
            x1_change = 0
        elif finger_move[1] == 1:
            y1_change = snake_block
            x1_change = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        score(f'Your score: {Length_of_snake - 1}', red)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]


        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True


        our_snake(snake_block, snake_List)

        pygame.display.update()
        if x1 == foodx and y1 == foody:

            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        if Length_of_snake == 16:
            game_win = True
        while game_win == True:
            dis.fill(blue)
            last_mes1("You Win! Congratulations!", yellow)
            last_mes2("Do you want to quit or try again?", green)
            mes_target("C - restart. Q - quit.", green)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_win = False
                    if event.key == pygame.K_c:
                        # l.release()
                        gameLoop(output_c=output_c, l=lock)
        clock.tick(snake_speed)
        #l.release()

    pygame.quit()
    quit()
if __name__ == "__main__":
    input_c, output_c = Pipe()
    p1 = multiprocessing.Process(target=camera_work, args=(input_c, lock)).start()
    p2 = multiprocessing.Process(target=gameLoop, args=(output_c, lock)).start()


'''Игра, развивающая мышцы пальцев.

О проблемах:
На начале игра была с фризами, скорость не соответствовала, оказалась проблема в нагрузке.
Пришлось подключать библиотеку multiprocessing для распределения операций на ядра процессора.
Добаляя библиотеку, следующим шагом стала передача данных между процессами, т.к. они должны ссылаться на одну переменную,
которая с учётом положения руки изменяется одним процессом и считывается вторым.
В этом помогло изучение функции Pipe. Неожиданной проблемой стала большая задержка между командой
жеста и воспроизведением вызываемой функции в игре.
Пришлось исключать функцию clock, которая отвечала за ограниченность скорости передвижения змейки.
При её отсутствии змейка либо приобретает чрезвычайно большую скорость, либо остаётся неподвижной.
Найдя нужную скорость 120, змейка приобрела приемлимую скорость, при этом передача команды не имела задержки.

Проблемы, которые остаются нерешёнными:
1. После функции Restart файл может запомнить движения,
которые были выполнены пальцем вне игры на камеру и воспроизвести их в ускоренном виде при перезапуске.
2. Программу не удаётся преобразовать в exe файл.

Целевая: люди, нуждающиеся в развитии моторики рук, маленькие дети'''