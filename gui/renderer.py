import pygame
from config import WHITE, LIGHT_GRAY, HOVER_COLOR

def draw_board(screen, board_origin, cell_size, HEIGHT, WIDTH, revealed, flags, game, lost, mine_img, flag_img):
    cells_rects = []
    mouse_pos = pygame.mouse.get_pos()
    for i in range(HEIGHT):
        row=[]
        for j in range(WIDTH):
            rect = pygame.Rect(board_origin[0]+j*cell_size, board_origin[1]+i*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, HOVER_COLOR if rect.collidepoint(mouse_pos) else LIGHT_GRAY, rect, border_radius=4)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=4)

            if (i,j) in revealed:
                neighbors = pygame.font.SysFont("OpenSans",20).render(str(game.nearby_mines((i,j))),True,(0,0,0))
                screen.blit(neighbors, neighbors.get_rect(center=rect.center))
            elif (i,j) in flags:
                screen.blit(flag_img, rect)
            elif game.is_mine((i,j)) and lost:
                screen.blit(mine_img, rect)
            row.append(rect)
        cells_rects.append(row)
    return cells_rects
