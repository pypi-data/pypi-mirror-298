from .config import *

class DialogBox(pygame.sprite.DirtySprite):
    def __init__(self, parent,DialogBox_img,DialogBox_font):
        pygame.sprite.DirtySprite.__init__(self, global_var.ALL_SPRITES)

        self.dirty = 2
        self.orig_image = pygame.image.load(DialogBox_img)
        self.font = pygame.font.Font(DialogBox_font, 25)
        self._text = ''
        self._parent = parent
        self._textColor=(0,0,0)
        self.hide()

    def say(self, text = None,textColor=None):
        self._textColor=textColor
        if text:
            self._text = str(text)
        else:
            self.hide()

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False


    def update(self):
        self.image = self.orig_image.copy()
        sc = 0.3
        num = 10
        maxy=100
        if self._parent.pos[0] >= 0 and self._parent.pos[1] >= maxy:
            # 第一象限
            flipx = True  # 可以把图片左右翻转,False为正方向，向左
            flipy = True  # 可以把图片上下翻转,False为正方向，向上
            flipx_operation = -sc
            flipy_operation = sc
            flipx_x = -40
            flipy_y = 80
        elif self._parent.pos[0] < 0 and self._parent.pos[1] >= maxy:
            # 第二象限
            flipx = False
            flipy = True
            flipx_operation = sc
            flipy_operation = sc
            flipx_x = 40
            flipy_y = 80
        elif self._parent.pos[0] < 0 and self._parent.pos[1] < maxy:
            # 第三象限
            flipx = False
            flipy = False
            flipx_operation = sc
            flipy_operation = -sc
            flipx_x = 40
            flipy_y = -80
        elif self._parent.pos[0] >=0 and self._parent.pos[1] < maxy:
            # 第四象限
            flipx = True
            flipy = False
            flipx_operation = -sc
            flipy_operation = -sc
            flipx_x = -40
            flipy_y = -80
        else:
            flipx = True
            flipy = True
            flipx_operation = sc
            flipy_operation = sc
            flipx_x = 0
            flipy_y = 0
        self.image = pygame.transform.flip(self.image, flipx, flipy)
        lines = len(self._text)//num+1
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * lines / 14 + 50)))
        #1--------原始解决办法
        # for i in range(lines):
        #     text = self.font.render(f"{self._text[i*num:(i+1)*num]}", 1, self._textColor, (255, 255, 255))
        #     # self.image.blit(text, (int(10*lines/5)+18,int(20*lines/5)+10 + i * 30-(lines-1)*1.6+text_py*lines/5))
        #     self.image.blit(text, (int(10*lines/5)+17,int(20*lines/5)+10 + i * 30-(lines-1)*2+text_py*(lines-1)*0.5))
        #2-----------新解决办法
        for i in range(lines):
            text = self.font.render(f"{self._text[i*num:(i+1)*num]}", 1, self._textColor, (255, 255, 255))
            if flipy:
                self.image.blit(text, (int(10*lines/5)+18,self.image.get_height() * (1-240/524) - ((lines - 1) * 30 / 2) + (i * 30)))
            else:
                self.image.blit(text, (
                int(10 * lines / 5) + 18, self.image.get_height() * (200 / 524) - ((lines - 1) * 30 / 2) + (i * 30)))
        #3-------------新新解决办法
        # for i in range(lines):
        #     text = self.font.render(f"{self._text[i*num:(i+1)*num]}", 1, self._textColor, (255, 255, 255))
        #     if flipy:
        #         self.image.blit(text, (self.image.get_width()/20,self.image.get_height() * (1-206/524) - ((lines - 1) * 30 / 2) + (i * 30)))
        #     else:
        #         self.image.blit(text, (
        #         self.image.get_width()/20, self.image.get_height() * (206 / 524) - ((lines - 1) * 30 / 2) + (i * 30)))
        if not self._visible:
            self.image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)        
        self.rect = self.image.get_rect()
        camera_offset = vec(global_var.SCREEN.size) - vec(global_var.CAMERA.size)
        if self._parent._gameObject.sprite:
            self.rect.center = Cartesian2pygame(self._parent.pos) - camera_offset // 2 \
                               + vec(flipx_operation * self._parent._gameObject.sprite.width,
                                     flipy_operation * self._parent._gameObject.sprite.height) + vec(flipx_x, flipy_y)
            # print(flipx_operation, flipy_operation)
        else:
            self.rect.center = Cartesian2pygame(self._parent.pos) - camera_offset // 2 + vec(flipx_x, flipy_y)
        global_var.ALL_SPRITES.move_to_front(self)

class TextBox(pygame.sprite.DirtySprite):
    def __init__(self, size, font = cwd+'\static\simkai.ttf',bgfill=None,font_color=(0, 0, 0)):
        pygame.sprite.DirtySprite.__init__(self, global_var.ALL_SPRITES)
        self.font = pygame.font.Font(font, size)
        self._text = ''
        self._pos = vec(0, 0)
        self._color = font_color
        self.bgfill=bgfill

    def print(self, text = None):
        self._text = str(text)

    def goto(self, x, *y):
        if y:
            self.pos = (x, *y)
        else:
            self.pos = x
    @ property
    def pos(self):
        return self._pos

    @ pos.setter
    def pos(self, pos):
        self._pos = pos

    @ property
    def color(self):
        return self._color

    @ color.setter
    def color(self, color):
        self._color = color

    def update(self):
        lines = self._text.split('\n')
        rendered_lines = []
        for line in lines:
            rendered_lines.append(self.font.render(line, 2, self._color))
        # self.image = self.font.render(f"{self._text}", 2, self._color)
        max_width = max([line.get_width() for line in rendered_lines])
        total_height = sum([line.get_height() for line in rendered_lines])
        text_image = pygame.Surface((max_width, total_height),pygame.SRCALPHA)
        if self.bgfill!=None:
            text_image.fill(self.bgfill)
        y=0
        for line in rendered_lines:
            text_image.blit(line, (0, y))
            y += line.get_height()
        # print(self.image)
        self.image = text_image
        self.rect = self.image.get_rect()
        self.rect.center = Cartesian2pygame(self._pos)
        global_var.ALL_SPRITES.move_to_front(self)
