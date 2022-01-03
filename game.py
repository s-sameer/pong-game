import pygame, sys, random
from time import sleep

def ball_animation():
    global ball_speed_x, ball_speed_y,player_score,oppo_score,score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        player_score+=1
        score_time=pygame.time.get_ticks()
    if ball.right >= screen_width:
        oppo_score+=1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x>0:
        if abs(ball.right-player.left)<10:
            hit_s.play()
            ball_speed_x *= -1
        elif abs(ball.bottom-player.top)<10 and ball_speed_y>0:
            hit_s.play()
            ball_speed_y*=-1
        elif abs(ball.top-player.bottom)<10 and ball_speed_y<10:
            hit_s.play()
            ball_speed_y *= -1
    if ball.colliderect(opponent) and ball_speed_x<0:
        if abs(ball.left - opponent.right) < 10:
            hit_s.play()
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            hit_s.play()
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 10:
            hit_s.play()
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

#function to create the opponent/computer
def opponent_ai():
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.bottom > ball.y:
        opponent.y -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_start():
    global ball_speed_x, ball_speed_y,score_time
    currenttime=pygame.time.get_ticks()
    ball.center=(screen_width/2,screen_height/2-10)

    if currenttime-score_time<1000:
        ball_speed_y, ball_speed_x = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None

# General setup
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Colors
light_grey = (200,200,200)
bg_color = pygame.Color('grey12')

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10,120)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10,120)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7

#Text variables
player_score=0
oppo_score=0
font=pygame.font.SysFont('arial',25)

#Score timer
score_time=True

#Sound
hit_s=pygame.mixer.Sound('resources/hit.mp3')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed =-6
            if event.key == pygame.K_DOWN:
                player_speed =6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_speed =0


    #Game Logic
    player_animation()
    opponent_ai()
    ball_animation()


    # Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))

    if score_time:
        ball_start()
    text1 = font.render(f'{player_score}', True, light_grey)
    text2 = font.render(f'{oppo_score}', True, light_grey)
    screen.blit(text1,(screen_width/2+10,screen_height/2))
    screen.blit(text2, (screen_width/2-20, screen_height / 2))

    pygame.display.flip()
    clock.tick(60)