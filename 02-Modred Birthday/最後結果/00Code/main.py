import pygame, sys
from settings import * # 導入遊戲設定
from level import Level
from debug import debug

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 控制熒幕大小
        pygame.display.set_caption('Modred Birthday') # 標題
        self.clock = pygame.time.Clock() # 控制FPS

        self.level = Level() # 建立關卡

        # sound
        main_sound = pygame.mixer.Sound('./03graphics/Overwatch Medley.wav')
        main_sound.play(loops = -1)
 
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # 當遊戲關閉時
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')   # 填充黑色
            self.level.run() # 更新關卡
            pygame.display.update() # 刷新
            self.clock.tick(FPS)    # 控制FPS

if __name__ == '__main__':
    game = Game()
    game.run()

