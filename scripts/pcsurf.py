'''import pygame as pg

pgSurf = pg.surface.Surface

class PickleableSurface(pgSurf):
    def __init__(self, *arg,**kwarg):
        size = arg[0]

        # size given is not an iterable,  but the object of pgSurf itself
        if (isinstance(size, pgSurf)):
            pgSurf.__init__(self, size=size.get_size(), flags=size.get_flags())
            self.surface = self
            self.name='test'
            self.blit(size, (0, 0))

        else:
            pgSurf.__init__(self, *arg, **kwarg)
            self.surface = self
            self.name = 'test'

    def __getstate__(self):
        state = self.__dict__.copy()
        surface = state["surface"]

        _1 = pg.image.tostring(surface.copy(), "RGBA")
        _2 = surface.get_size()
        _3 = surface.get_flags()
        state["surface_string"] = (_1, _2, _3)
        return state

    def __setstate__(self, state):
        surface_string, size, flags = state["surface_string"]

        pgSurf.__init__(self, size=size, flags=flags)

        s=pg.image.fromstring(surface_string, size, "RGBA")
        state["surface"] =s;
        self.blit(s,(0,0));self.surface=self;
        self.__dict__.update(state)

pg.Surface = PickleableSurface
pg.surface.Surface = PickleableSurface

surf = pg.Surface((300, 400), pg.SRCALPHA|pg.HWSURFACE)
# Surface, color, start pos, end pos, width
pg.draw.line(surf, (0,0,0), (0,100), (200, 300), 2)

from pickle import loads, dumps

dump = dumps(surf)
loaded = loads(dump)
pg.init()
screen = pg.display.set_mode((300, 400))
screen.fill((255, 255, 255))
screen.blit(loaded, (0,0))
pg.display.update()'''

import base64
def serealizeimg(izobr):
    # Преобразование изображения в строку base64
    with open("image.jpeg", "rb") as image2string:
        # Чтение и кодирование изображения
        conv_str = base64.b64encode(image2string.read())
    print(conv_str)  # Вывод закодированной строки

    # Запись строки base64 в бинарный файл
    with open('img.bin', "wb") as file_bin:
        file_bin.write(conv_str)

    # Декодирование строки base64 обратно в изображение
    image_str = open('img.bin', 'rb')
    byte_file = image_str.read()
    image_str.close()

    decoded_img = open('decoded_image.jpeg', 'wb')
    decoded_img.write(base64.b64decode(byte_file))
    decoded_img.close()