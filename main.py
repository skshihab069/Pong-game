import pygame
import sys
import random
from pygame import mixer


def draw_shapes():
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, yellow, ball)
    pygame.draw.aaline(screen, white, (screen_width / 2, 0), (screen_width / 2, screen_hight))


def ball_movement():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.top <= 0 or ball.bottom >= screen_hight:
        ball_speed_y *= -1
        pygame.mixer.Sound.play(pong_sound)
        # player score
    if ball.left <= 0:
        player_score += 1
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()  # tells how much time it has been since game started
        # opponent score
    if ball.right >= screen_width:
        opponent_score += 1
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()  # tells how much time it has been since game started

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y < 0:
            ball_speed_x *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_hight:
        player.bottom = screen_hight


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_hight:
        opponent.bottom = screen_hight


def ball_restart_timer():
    global ball_speed_x, ball_speed_y, score_time
    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_hight / 2)
    # timer countdown
    if current_time - score_time < 700:
        num_three = game_font.render("3", False, white)
        screen.blit(num_three, (screen_width / 2 - 19, screen_hight / 2 + 20))
    if 700 < current_time - score_time < 1400:
        num_two = game_font.render("2", False, white)
        screen.blit(num_two, (screen_width / 2 - 19, screen_hight / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        num_one = game_font.render("1", False, white)
        screen.blit(num_one, (screen_width / 2 - 19, screen_hight / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x = 0
        ball_speed_y = 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


def display_score():
    player_text = game_font.render(f'Player {player_score}', False, white)
    screen.blit(player_text, (900, 20))
    opponent_text = game_font.render(f'Bot {opponent_score}', False, white)
    screen.blit(opponent_text, (80, 20))


def show_winner():
    global player, opponent, ball_speed_x, ball_speed_y

    if player_score == 3 and opponent_score != 3:
        player_text = winner_font.render('Player wins', False, white)
        screen.blit(player_text, (screen_width / 2, screen_hight / 2))
        player = pygame.Rect(screen_width + 20, screen_hight + 20, 10, 140)
        ball_speed_x, ball_speed_y = 0, 0

    if opponent_score == 3 and player_score != 3:
        opponent_text = winner_font.render('Bot wins', False, white)
        screen.blit(opponent_text, (screen_width / 2, screen_hight / 2))
        opponent = pygame.Rect(screen_width + 20, screen_hight + 20, 10, 140)
        ball_speed_x, ball_speed_y = 0, 0

pygame.mixer.pre_init(44100, -16, 2 ,512)
pygame.init()
clock = pygame.time.Clock()

# setting up screen
screen_width = 1080
screen_hight = 750
screen = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption('Pong')

# Game rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_hight / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_hight / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_hight / 2 - 70, 10, 140)
# Game variables
ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7
# Scores
player_score = 0
opponent_score = 0
game_font = pygame.font.Font('freesansbold.ttf', 24)
winner_font = pygame.font.Font('freesansbold.ttf', 64)
score_time = True

# Sound
pong_sound = pygame.mixer.Sound('pong.ogg')
score_sound = pygame.mixer.Sound('score.ogg')

# colors
light_grey = (200, 200, 200)
yellow = (255, 255, 21)
white = (255, 255, 255)
# Game loop
Running = True
while Running:
    screen.fill((42, 129, 45))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7

    # Scores
    if score_time:
        ball_restart_timer()  # every time a player  or opponents scores the score_time is set to true and resets the ball

    display_score()
    opponent_ai()
    player_animation()
    draw_shapes()
    ball_movement()
    show_winner()

    pygame.display.flip()
    clock.tick(60)  # Determines the speed of while loop meaning the clock will tick 120 times per tick
