import pygame
import button
import pygame, sys, random


pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

largura = 1280
altura = 960
screen = pygame.display.set_mode((largura, altura))  # define o tamanho da tela
pygame.display.set_caption('PING PONG')  # define o titulo do jogo

ball = pygame.Rect(largura / 2 - 15, altura / 2 - 15, 30, 30)  # define a posicao, em x,y e depois o tamanho
player = pygame.Rect(largura - 20, altura / 2 - 70, 10, 140)  # define a posicao, em x,y e depois o tamanho
opponent = pygame.Rect(10, altura / 2 - 70, 10, 140)  # define a posicao, em x,y e depois o tamanho



light_grey = (200, 200, 200)
red = (255,0,0)
ball_speed_x = 7
ball_speed_y = 7 * random.choice((1, -1))
# controla a velocidade da bola
player_speed = 0 * random.choice((1, -1))
opponent_speed = 7

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.Font('freesansbold.ttf', 42)
fontemenu = "Arial"

# sound
# plob_sound = pygame.mixer.Sound("Plob.ogg")
# score_sound = pygame.mixer.Sound("score.ogg")


# create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# game variables
game_paused = False
menu_state = "menu"
jogo = False

# define fonts
font = pygame.font.SysFont("arialblack", 50)

# define colours
TEXT_COL = (255, 255, 255)

# load button images
imagemdefundo = pygame.image.load("imagens/fundo.jpg").convert_alpha()
resume_img = pygame.image.load("imagens/play1.png").convert_alpha()
mesadefundo = pygame.image.load("imagens/mesa.jpeg").convert_alpha()
quit_img = pygame.image.load("imagens/quit1.png").convert_alpha()
resume_button = button.Button(485, 315, resume_img, 0.8)
# options_button = button.Button(297, 250, options_img, 1)
quit_button = button.Button(450,460, quit_img, 1)


# create button instances


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x  # faz a bola se mover
    ball.y += ball_speed_y  # faz a bola se mover
    if ball.top <= 0 or ball.bottom >= altura:
        ball_speed_y *= -1  # diz o que a acontece se ela bate na borda e impede ela de sair da tela
        # pygame.mixer.Sound.play(plob_sound)  faz toca musica
    # Player Score
    if ball.left <= 0:
        ball_start()
        player_score += 1
        # pygame.mixer.Sound.play(score_sound)

    # Opponent Score
    if ball.right >= largura:
        ball_start()
        opponent_score += 1
        # pygame.mixer.Sound.play(score_sound)

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
        # pygame.mixer.Sound.play(plob_sound)

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
        # pygame.mixer.Sound.play(plob_sound)


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= altura:
        player.bottom = altura


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= altura:
        opponent.bottom = altura


def ball_start():
    global ball_speed_x, ball_speed_y
    ball.center = (largura / 2, altura / 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def pingpong():
    global player_speed
    jogando = True
    while jogando:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7

        ball_animation()
        player_animation()
        opponent_ai()



        screen.blit(mesadefundo,(0,0))  # define a cor do fundo
        pygame.draw.rect(screen, light_grey, player)  # cria a raquete do lado direito
        pygame.draw.rect(screen, light_grey, opponent)  # cria a raquete do lado esquerdo
        pygame.draw.ellipse(screen, light_grey, ball)  # cria bola do jogo
        pygame.draw.aaline(screen, light_grey, (largura / 2, 0),
                           (largura / 2, altura))  # cria uma linha no meio da tela ( a rede do ping pong)



        player_text = basic_font.render(f'{player_score}', False, red)
        screen.blit(player_text, (660, 470))

        opponent_text = basic_font.render(f'{opponent_score}', False, red)
        screen.blit(opponent_text, (600, 470))

        pygame.display.flip()
        clock.tick(60)


def menu():
    global game_paused, menu_state
    run = True
    while run:

        screen.blit(imagemdefundo,(0,0))

        # check if game is paused
        if game_paused == True:
            # check menu state
            if menu_state == "menu":
                # draw pause screen buttons
                if resume_button.draw(screen):
                    game_paused = False
                    pingpong()
                if quit_button.draw(screen):
                    run = False

        else:
            draw_text("Desenvolvido por Vitor Gabriel e Gabriel belo", font, TEXT_COL, 50,70)
            draw_text("aperte ESPAÇO para continuar", font, TEXT_COL, 380, 470)
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


menu()