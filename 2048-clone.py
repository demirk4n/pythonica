import pygame
import random
from pygame.locals import *

NUM_ROWS = 4 #y
NUM_COLS = 4 #x

CELL_SIZE = 60 # Cell size in pixels
TOP_SCREEN_MARGIN = 50
# set up the colors R G B

BLACK = (0, 0, 0)
GRAY     = (100, 100, 100)
NAVY_BLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

# setup directions
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


class Board():
    def __init__(self, screen):
        self.board = {}
        self.create_board()
        self.pop_random()
        self.pop_random()
        self.shift_direction = None
        self.move_count = 0
        self.score = 0

    def create_board(self):
        for x in range(NUM_ROWS):
            for y in range(NUM_COLS):
                cell_loc = (x, y)
                # print(cell_loc)
                self.board[cell_loc] = Cell(cell_loc, 0, screen, False)

    def pop_random(self):
        available_cell_list = []
        for (x, y), cell in self.board.items():
            if cell.value == 0: # If value < 2 then this is an empty cell
                available_cell_list.append((x, y))

        if len(available_cell_list) == 0:
            return False
        else:
            rand_xy = random.choice(available_cell_list)
            self.board[rand_xy] = Cell(rand_xy, 2, screen, False)

    def update(self, event, dt):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.shift_direction = LEFT
            print("left pressed")
            self.shift_board()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.shift_direction = RIGHT
            print("right pressed")
            self.shift_board()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.shift_direction = UP
            print("up pressed")
            self.shift_board()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.shift_direction = DOWN
            print("down pressed")
            self.shift_board()

    def draw_board(self, dt):
        screen.fill(BLACK)
        for xy, cell in self.board.items():
            cell.draw_cell(xy, cell.value)
            cell.lock = False

        if self.move_count > 0:
            self.pop_random()

        self.move_count = 0

    def shift_order(self):
        order = []
        if self.shift_direction == LEFT:
            for y in range(NUM_ROWS):
                for x in range(NUM_COLS):
                    order.append((x,y))
            return order
            #return [(0,0),(1,0),(2,0),(3,0),(0,1),(1,1),(2,1),(3,1),(0,2),(1,2),(2,2),(3,2),(0,3),(1,3),(2,3),(3,3)]
        if self.shift_direction == RIGHT:
            for y in range(NUM_ROWS):
                for x in range(NUM_COLS-1, -1 , -1):
                    order.append((x,y))
            return order
            #return [(3,0),(2,0),(1,0),(0,0),(3,1),(2,1),(1,1),(0,1),(3,2),(2,2),(1,2),(0,2),(3,3),(2,3),(1,3),(0,3)]
        if self.shift_direction == UP:
            for x in range(NUM_COLS):
                for y in range(NUM_ROWS):
                        order.append((x,y))
            return order
            #return [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
        if self.shift_direction == DOWN:
            for x in range(NUM_COLS):
                for y in range(NUM_ROWS-1, -1, -1):
                    order.append((x,y))
            return order
            #return [(0,3),(0,2),(0,1),(0,0),(1,3),(1,2),(1,1),(1,0),(2,3),(2,2),(2,1),(2,0),(3,3),(3,2),(3,1),(3,0)]

    def shift_board(self):
        # print(self.shift_order())
        for (x, y) in self.shift_order():
                cell = self.board[(x, y)]
                if cell.value >= 2:# action only on nonempty cells
                    self.cell_action((x, y))

    def cell_action(self, xy):
        x, y = xy
        if self.shift_direction == LEFT:
            x -= 1
            if x < 0:
                x = 0
        if self.shift_direction == RIGHT:
            x += 1
            if x == NUM_COLS:
                x = NUM_COLS - 1
        if self.shift_direction == UP:
            y -= 1
            if y < 0:
                y = 0
        if self.shift_direction == DOWN:
            y += 1
            if y == NUM_ROWS:
                y = NUM_ROWS - 1

        current_cell = self.board[xy]
        target_cell = self.board[(x, y)]

        if not (x, y) == xy:
            if target_cell.value == 0:
                self.board[(x, y)] = Cell((x, y), current_cell.value, screen, False)
                self.board[xy] = Cell(xy, 0, screen, False)
                self.cell_action((x, y))
                self.move_count += 1
            if target_cell.value == current_cell.value and target_cell.lock is False:
                self.board[(x, y)] = Cell((x, y), target_cell.value + current_cell.value, screen, True)
                self.board[xy] = Cell(xy, 0, screen, False)
                self.move_count += 1
            else:
                pass


class Cell():
    def __init__(self, cell_loc, value, screen, lock):
        self.cell_loc = cell_loc
        self.value = value
        self.lock = lock
        self.x, self.y = cell_loc
        self.draw_cell(cell_loc, value)

    def draw_cell(self, cell_loc, value):
        cell_colors = {2: RED, 4: GREEN, 8: BLUE, 16: YELLOW, 32: ORANGE, 64: PURPLE, 128: CYAN, 256: NAVY_BLUE}
        x, y = cell_loc
        (loc_x, loc_y) = x * CELL_SIZE, (y * CELL_SIZE) + TOP_SCREEN_MARGIN
        if value >= 2:
            cell_rect = pygame.rect.Rect((loc_x, loc_y), (CELL_SIZE - 2, CELL_SIZE - 2))
            pygame.draw.rect(screen, cell_colors[value], cell_rect)
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(str(value), True, WHITE)
            text_pos = text.get_rect(center=(cell_rect.centerx,cell_rect.centery))
            screen.blit(text, text_pos)

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()
        board = Board(screen)

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    board.update(event, dt)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    board.update(event, dt)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    board.update(event, dt)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    board.update(event, dt)

            board.draw_board(dt / 1000.)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((NUM_COLS * CELL_SIZE, (NUM_ROWS * CELL_SIZE) + TOP_SCREEN_MARGIN))
    Game().main(screen)

