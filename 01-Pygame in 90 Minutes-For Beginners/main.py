import pygame
import os # windows系統上下級文件夾操作
pygame.font.init() # 載入Pygame font library
pygame.mixer.init() #倒入音樂

WIDTH, HEIGHT = 800, 500 
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # 設定寬度和高度
pygame.display.set_caption("First Game") # 設定遊戲（窗口）標題

WHITE = (255, 255, 255) # 白色
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# BULLET_HIT_SOUND = pygame.mixer.music.load('Grenade+1.wav')
# BULLET_FIRE_SOUND = pygame.mixer.music.load('Gun+Silencer.wav')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40) #設定字型和大小
WINNER_FONT = pygame.font.SysFont('comicsans', 100) # 勝利字體

# 如果不設定幀率上線的話，就會變成無限制
FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3 # 熒幕中最多出現3顆子彈
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (40, 40)

YELLOW_HIT = pygame.USEREVENT + 1 # unique ID
RED_HIT = pygame.USEREVENT + 2 # unique ID

# 找到黃色飛機
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('01-Pygame in 90 Minutes-For Beginners\Assets','spaceship_yellow.png'))
# 再旋轉素材
# 設定飛機的大小
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90) 

# 找到紅色飛機
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('01-Pygame in 90 Minutes-For Beginners\Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) 

# 加載背景
SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('01-Pygame in 90 Minutes-For Beginners\Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    # WIN.fill(WHITE) # 因為pygame不會移除上一幀的畫面，如果不添加白色的遮擋，每一幀的軌道就都會保留下來
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f'Red Health: {red_health}', True, RED)
    yellow_health_text = HEALTH_FONT.render(f'Yellow Health: {yellow_health}', True, YELLOW)
    WIN.blit(red_health_text, (WIDTH//2 - red_health_text.get_width()-110,0))
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width()-20, 0))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # 透過blit這個函數，將img放到畫面中
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update() # Pygame需要不斷的刷新頁面，才能夠得到你的設置


# 按壓後，更改red的坐標
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: # 按a鍵，像左移動(同時設定移動邊距)
        red.x -= VEL
    elif keys_pressed[pygame.K_d] and red.x + VEL < WIDTH//2 - SPACESHIP_WIDTH: # 按d鍵，像右移動
        red.x += VEL
    elif keys_pressed[pygame.K_w] and red.y - VEL >0: # 按w鍵，像上移動
        red.y -= VEL
    elif keys_pressed[pygame.K_s] and red.y + VEL < HEIGHT - SPACESHIP_HEIGHT: # 按s鍵，像下移動
        red.y += VEL

# 按壓後，更改yellow的坐標
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > WIDTH//2:
        yellow.x -= VEL
    elif keys_pressed[pygame.K_RIGHT] and yellow.x + VEL < WIDTH- SPACESHIP_WIDTH:
        yellow.x += VEL
    elif keys_pressed[pygame.K_UP] and yellow.y - VEL >0:
        yellow.y -= VEL
    elif keys_pressed[pygame.K_DOWN] and yellow.y + VEL < HEIGHT - SPACESHIP_HEIGHT:
        yellow.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet): # colliderect 對撞
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH: # 碰到邊界的時候，消除子彈
            red_bullets.remove(bullet)
    
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

# 勝利界面
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000) # 當延時等待5秒後，再重新開始

def main():
    # 紅飛機和黃飛機的初始位置
    red = pygame.Rect(WIDTH//2//2-10, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(WIDTH//4*3-10, HEIGHT//2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # 設定FPS為60幀每秒

        # 如果在遊戲的過程中點擊了退出，則退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() # 當點了退出，則關閉Pygame

            # yellow.x += 1
            # red.x += 1

            # 設置左右ctrl
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS: # 熒幕中最多出現3顆子彈
                    # （添加子彈（置中），寬度10，高度5）
                    bullet = pygame.Rect(
                        red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()
                elif event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            # 如果誰被擊中後，扣血
            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()
            elif event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()

        winner_text = ""
        # 當誰的血小於0時，結束遊戲
        if red_health <= 0:
            winner_text = 'Yellow Wins! '
        
        if yellow_health <= 0:
            winner_text = 'Red Wins! '
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        # print(red_bullets, yellow_bullets)
        # 移動飛機
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) # 呼叫背景白色函數

    # pygame.quit() # 如果設定勝利完退出遊戲則寫這行
    # 如果勝利後想要繼續遊戲，則寫↓
    main()

if __name__ == '__main__':
    main()