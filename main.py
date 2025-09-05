import pygame, sys, time
from config import *
from core.board import Minesweeper
from core.ai import MinesweeperAI
from gui.renderer import draw_board
from gui.ui import draw_button
from gui.log_panel import LogPanel

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper AI")
font_small = pygame.font.SysFont("OpenSans",20)
font_medium = pygame.font.SysFont("OpenSans",28)
font_large = pygame.font.SysFont("OpenSans",40)

cell_size = 50
board_origin = (BOARD_PADDING, BOARD_PADDING)

flag_img = pygame.image.load("assets/images/flag.png")
mine_img = pygame.image.load("assets/images/mine.png")
flag_img = pygame.transform.scale(flag_img,(cell_size,cell_size))
mine_img = pygame.transform.scale(mine_img,(cell_size,cell_size))

game = Minesweeper(HEIGHT, WIDTH, MINES)
ai = MinesweeperAI(HEIGHT, WIDTH, log_callback=None)
revealed=set()
flags=set()
lost=False
instructions=True

log_panel_rect = pygame.Rect(SCREEN_WIDTH*2/3+BOARD_PADDING,300,SCREEN_WIDTH/3-2*BOARD_PADDING,SCREEN_HEIGHT-300-BOARD_PADDING)
log_panel = LogPanel(screen, log_panel_rect, font_small)
ai.log_callback = log_panel.add_message

clock=pygame.time.Clock()

def ai_move():
    global lost
    move = ai.make_safe_move() or ai.make_random_move()
    if move:
        if game.is_mine(move):
            lost=True
            log_panel.add_message(f"AI hit mine at {move}")
        else:
            revealed.add(move)
            ai.add_knowledge(move, game.nearby_mines(move))
            log_panel.add_message(f"AI revealed {move}, {game.nearby_mines(move)} mines nearby")
        time.sleep(0.5)

while True:
    clock.tick(FPS)
    screen.fill(BLACK)
    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    log_panel.draw()

    for event in pygame.event.get():
        if event.type==pygame.QUIT: pygame.quit(); sys.exit()
        elif event.type==pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w,event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    if lost:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay,(0,0))
        game_over_text = font_large.render("GAME OVER", True, RED)
        screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2-50)))
        reset_btn = pygame.Rect(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2, 200,50)
        draw_button(screen, reset_btn,"RESET",WHITE,BUTTON_HOVER,font_medium)
        if mouse_pressed[0] and reset_btn.collidepoint(mouse_pos):
            game = Minesweeper(HEIGHT, WIDTH, MINES)
            ai = MinesweeperAI(HEIGHT, WIDTH, log_callback=log_panel.add_message)
            revealed=set(); flags=set(); lost=False; log_panel.messages.clear()
        pygame.display.flip()
        continue

    board_cells = draw_board(screen, board_origin, cell_size, HEIGHT, WIDTH, revealed, flags, game, lost, mine_img, flag_img)

    ai_btn = pygame.Rect(SCREEN_WIDTH*2/3+BOARD_PADDING,150,200,50)
    reset_btn = pygame.Rect(SCREEN_WIDTH*2/3+BOARD_PADDING,220,200,50)
    draw_button(screen, ai_btn,"AI Move",WHITE,BUTTON_HOVER,font_medium)
    draw_button(screen, reset_btn,"Reset",WHITE,BUTTON_HOVER,font_medium)

    left,_,right = mouse_pressed
    if left:
        if ai_btn.collidepoint(mouse_pos): ai_move()
        elif reset_btn.collidepoint(mouse_pos):
            game = Minesweeper(HEIGHT, WIDTH, MINES)
            ai = MinesweeperAI(HEIGHT, WIDTH, log_callback=log_panel.add_message)
            revealed=set(); flags=set(); lost=False; log_panel.messages.clear()
        else:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if board_cells[i][j].collidepoint(mouse_pos):
                        if (i,j) not in flags and (i,j) not in revealed:
                            if game.is_mine((i,j)): lost=True
                            else:
                                revealed.add((i,j))
                                ai.add_knowledge((i,j), game.nearby_mines((i,j)))
                        time.sleep(0.1)
    elif right:
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if board_cells[i][j].collidepoint(mouse_pos):
                    if (i,j) in flags: flags.remove((i,j))
                    else: flags.add((i,j))
                    time.sleep(0.1)

    pygame.display.flip()
