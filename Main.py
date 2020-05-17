import pygame
import time
from threading import Thread
from GameSettings import *
import Objects
import ScreenEngine as SE
import Logic
import Service
from Speech2Text import Speecher
from argparse import ArgumentParser


class MyHeroFactory(Objects.AbstractHeroFactory):
    def create(self):
        sprite = Service.ObjectsLib.textures['hero']['sprite']
        return Objects.Hero(BASE_STATS, sprite)


def repaint(game_display, pygame_obj, drawer_obj):
    # Обновляем изображение на экране
    game_display.blit(drawer_obj, (0, 0))
    drawer_obj.draw(gameDisplay)
    pygame_obj.display.update()


def quit_game(pygame_obj):
    # Выходим из игры
    pygame_obj.display.quit()
    pygame_obj.quit()
    exit(0)


def create_game(sprite_size, pygame_obj):
    dict_dirs = {
        'objects': OBJECT_TEXTURE,
        'ally': ALLY_TEXTURE,
        'enemies': ENEMY_TEXTURE,
        'textures': OTHER_TEXTURE
    }

    Service.ObjectsLib.set_generators(
        # Указываем, кто будет отвественный за текстуры
        Service.GraphicalLib(
            pygame_obj,
            sprite_size,
            dict_dirs
        ),
        # А тут, за эффекты
        Service.ActionLib()
    )

    Service.ObjectsLib.load(MAP_TEXTURES)
    with open('objects.yml', 'r') as file:
        Service.ObjectsLib.append(file.read())

    Service.LevelGenerator.set_libs(Service.ObjectsLib)
    Service.LevelGenerator.load('levels.yml')
    Service.LevelGenerator.levels.append(
        {'map': Service.MC.EndMapSurface('EndMap'),
         'obj': Service.MC.EmptyMapSpawn('EndMap')})

    engine_obj = Logic.GameEngine()
    engine_obj.sprite_size = sprite_size

    engine_obj.hero_generator = MyHeroFactory()
    engine_obj.level_generator = Service.LevelGenerator
    engine_obj.subscribe(Service.ObjectsLib)
    engine_obj.start()

    return engine_obj


def get_voice_command() -> int:
    speecher = Speecher()
    command = speecher.listen_to()
    print("command: " + command)
    if command not in VOICE_TO_KEY:
        return -1
    return VOICE_TO_KEY[command]



def key_decider(event_key):
    global engine
    if event_key == pygame.K_h:
        # Справка
        engine.show_help = not engine.show_help
        repaint(gameDisplay, pygame, drawer)
    if event_key == pygame.K_m:
        # Показать миникарту
        engine.show_minimap = not engine.show_minimap
        repaint(gameDisplay, pygame, drawer)
    if event_key == pygame.K_F12:
        # Маленький "не документированный" чит
        engine.level_next()
    if event_key == pygame.K_KP_PLUS or \
        event_key == pygame.K_PLUS or \
        event_key == pygame.K_EQUALS:
        # Приближаем карту
        engine.zoom_in()
    if event_key == pygame.K_KP_MINUS or event_key == pygame.K_MINUS:
        # Отдаляем карту
        engine.zoom_out()
    if event_key == pygame.K_r:
        # Рестарт
        engine.sprite_size = BASE_SPRITE_SIZE
        engine.start()
    if event_key == pygame.K_RETURN or event_key == pygame.K_KP_ENTER:
        # Сброс уровня
        engine.level_reset()
    if event_key == pygame.K_ESCAPE:
        engine.working = False
    if engine.game_process:
        if event_key == pygame.K_UP:
            engine.move_up()
        elif event_key == pygame.K_DOWN:
            engine.move_down()
        elif event_key == pygame.K_LEFT:
            engine.move_left()
        elif event_key == pygame.K_RIGHT:
            engine.move_right()
        elif event_key == pygame.K_w:
            engine.run_up()
        elif event_key == pygame.K_s:
            engine.run_down()
        elif event_key == pygame.K_a:
            engine.run_left()
        elif event_key == pygame.K_d:
            engine.run_right()

parser = ArgumentParser()
parser.add_argument('--use-micro', type=bool)
args = parser.parse_args()
use_micro = args.use_micro

pygame.init()
gameDisplay = pygame.display.set_mode(SCREEN_DIM)
pygame.display.set_caption("MyRPG")
# Добавляем возможность обрабатывать длительные нажатия клавиши
pygame.key.set_repeat(15, 200)

engine = create_game(BASE_SPRITE_SIZE, pygame)

drawer = SE.ScreenHandle((0, 0))
drawer = SE.HelpWindow((700, 500), pygame.SRCALPHA, (0, 0), drawer)
drawer = SE.MiniMap((164, 164), pygame.SRCALPHA, (50, 50), drawer)
drawer = SE.InfoWindow((160, 600), (490, 14), drawer)
drawer = SE.ProgressBar((640, 120), (640, 0), drawer)
drawer = SE.GameSurface((640, 480), pygame.SRCALPHA, (0, 480), drawer)

drawer.connect_engine(engine)

VOICE_TO_KEY = {
    'help': pygame.K_h,
    'map': pygame.K_m,
    'next level': pygame.K_F12,
    'zoom in': pygame.K_KP_PLUS,
    'zoom out': pygame.K_KP_MINUS,
    'new game': pygame.K_r,
    'restart': pygame.K_RETURN,
    'escape': pygame.K_ESCAPE,
    'Escape': pygame.K_ESCAPE,
    'move up': pygame.K_UP,
    'up': pygame.K_UP,
    'move down': pygame.K_DOWN,
    'down': pygame.K_DOWN,
    'move left': pygame.K_LEFT,
    'left': pygame.K_LEFT,
    'move right': pygame.K_RIGHT,
    'right': pygame.K_RIGHT,
    'run up': pygame.K_w,
    'run left': pygame.K_a,
    'run down': pygame.K_s,
    'run right': pygame.K_d,
}

a = lambda x: [repaint(gameDisplay, pygame, drawer) for _ in range(x)]
if use_micro:
    speecher = Speecher()
    dict = {"command": ""}
    a(2)  # :D
    dict["command"] = speecher.listen_to()
    while engine.working:
        repaint(gameDisplay, pygame, drawer)
        if dict["command"] != "":
            if dict["command"] not in VOICE_TO_KEY:
                print("not in VOICE_TO_KEY")
                dict["command"] = ""
                continue
            key = VOICE_TO_KEY[dict["command"]]
            key_decider(key)
            dict["command"] = ""
            a(3)
        pygame.event.get()
        speecher.listen(dict)
else:
    while engine.working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.working = False
            if event.type == pygame.KEYDOWN:
                key_decider(event.key)

        repaint(gameDisplay, pygame, drawer)

quit_game(pygame)
