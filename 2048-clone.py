import pygame, random, time, sys
from pygame.locals import *

NUM_ROWS = 4  # y
NUM_COLS = 4  # x
CELL_SIZE = 60  # Cell size in pixels
TOP_SCREEN_MARGIN = 50
WINDOW_WIDTH = NUM_COLS * CELL_SIZE
WINDOW_HEIGHT = NUM_ROWS * CELL_SIZE + TOP_SCREEN_MARGIN

SCORE_FONT_SIZE = 30
CELL_FONT_SIZE = 20

FPS = 10  # Game FPS
CELL_MOVE_SPEED = 10  # in frames per second

# set up the colors R G B
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
NAVY_BLUE = ( 60,  60, 100)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)
PURPLE = (255,   0, 255)
CYAN = (0, 255, 255)

# setup directions
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'


class Board(object):
    def __init__(self):
        self.board = {}
        self.shift_direction = None
        self.move_count = 0
        self.score = 0
        self.game_over = False
        self.game_win = False
        self.dt = 0.0
        self.busy = False

    def create(self):
        for x in range(NUM_ROWS):
            for y in range(NUM_COLS):
                cell_loc = (x, y)
                # print(cell_loc)
                self.board[cell_loc] = Cell(cell_loc, 0, False)

    def pop_random(self):
        available_cell_list = []
        for (x, y), cell in self.board.items():
            if cell.value == 0: # If value < 2 then this is an empty cell
                available_cell_list.append((x, y))
        if len(available_cell_list) == 0:
            return False
        else:
            rand_xy = random.choice(available_cell_list)
            self.board[rand_xy] = Cell(rand_xy, 2, False)

    def update(self, dt):

        if self.busy:
            self.busy = False
            self.shift_board()
        elif not self.busy and self.move_count > 0:
            self.pop_random()
            self.move_count = 0

        #print(self.busy)

    def draw(self, display):
        display.fill(BLACK)
        for i, c in self.board.items():
            c.draw()

    def shift_order(self):
        order = []
        if self.shift_direction == LEFT:
            for y in range(NUM_ROWS):
                for x in range(NUM_COLS):
                    order.append((x,y))
            #return [(0,0),(1,0),(2,0),(3,0),(0,1),(1,1),(2,1),(3,1),(0,2),(1,2),(2,2),(3,2),(0,3),(1,3),(2,3),(3,3)]
        if self.shift_direction == RIGHT:
            for y in range(NUM_ROWS):
                for x in range(NUM_COLS-1, -1, -1):
                    order.append((x,y))
            #return [(3,0),(2,0),(1,0),(0,0),(3,1),(2,1),(1,1),(0,1),(3,2),(2,2),(1,2),(0,2),(3,3),(2,3),(1,3),(0,3)]
        if self.shift_direction == UP:
            for x in range(NUM_COLS):
                for y in range(NUM_ROWS):
                        order.append((x, y))
            #return [(0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
        if self.shift_direction == DOWN:
            for x in range(NUM_COLS):
                for y in range(NUM_ROWS-1, -1, -1):
                    order.append((x,y))
            #return [(0,3),(0,2),(0,1),(0,0),(1,3),(1,2),(1,1),(1,0),(2,3),(2,2),(2,1),(2,0),(3,3),(3,2),(3,1),(3,0)]
        return order

    def shift_board(self):
        #print(self.shift_order())

        for (x, y) in self.shift_order():
            current_cell = self.board[(x, y)]
            current_cell.lock = False
            next_cell = self.get_next_cell((x, y))

            if current_cell.value >= 2 and next_cell:  # action only on nonempty cells
                if next_cell.value == 0:
                    next_cell.value, next_cell.lock = current_cell.value, False
                    current_cell.value, current_cell.lock = 0, False
                    if self.get_next_cell(next_cell.location):
                        self.busy = True

                elif next_cell.value == current_cell.value and next_cell.lock is False:
                    next_cell.value += current_cell.value
                    next_cell.lock = True
                    current_cell.value, current_cell.lock = 0, False
                    self.score += next_cell.value + current_cell.value

                self.move_count += 1

    def get_next_cell(self, location):

        x, y = location
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

        if (x, y) == location: # no move
            return False
        else:
            return self.board[(x, y)]


    def tick(self, dt):
        self.dt = dt
        #print("dt " + str(dt))


class Cell(object):
    def __init__(self, location, value, lock):
        self.location = location
        self.value = value
        self.lock = lock
        self.x, self.y = location
        self.offset = 0

    def draw(self):

        cell_colors = {2: RED, 4: GREEN, 8: BLUE, 16: YELLOW, 32: ORANGE, 64: PURPLE, 128: CYAN, 256: NAVY_BLUE,
                       512: GRAY}
        x, y = self.location
        (loc_x, loc_y) = x * CELL_SIZE, (y * CELL_SIZE) + TOP_SCREEN_MARGIN
        if self.value >= 2:
            cell_rect = pygame.rect.Rect((loc_x, loc_y), (CELL_SIZE - 2, CELL_SIZE - 2))
            pygame.draw.rect(screen, cell_colors[self.value], cell_rect)
            font = pygame.font.Font('freesansbold.ttf', CELL_FONT_SIZE)
            text = font.render(str(self.value), True, WHITE)
            text_pos = text.get_rect(center=(cell_rect.centerx,cell_rect.centery))
            screen.blit(text, text_pos)


class Game(object):

    def __init__(self):
        self.board = None
        pygame.init()
        pygame.display.set_caption("Py2048 - by ED")
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF)
        self.board = Board()

        #self.font = pygame.font.Font(None, FONT_SIZE)

    def start(self):
        self.board.create()
        self.board.pop_random()
        self.board.pop_random()
        pass

    def quit(self):
        pygame.quit()
        sys.exit()

    def play(self):
        self.start()

        while True:
            self.draw()
            dt = min(self.clock.tick(FPS) / 1000.0, 1.0 / FPS)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    self.input(event.key)
                elif event.type == QUIT:
                    self.quit()
            self.board.update(dt)
            self.clock.tick(FPS)

    def draw(self):
        self.board.draw(self.display)
        self.draw_score()
        #pygame.display.flip()
        pygame.display.update()


    def draw_score(self):
        score_rect = pygame.rect.Rect((0, 0), (NUM_COLS * CELL_SIZE, TOP_SCREEN_MARGIN))
        font = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)
        text = font.render(str(self.board.score), True, WHITE)
        text_pos = text.get_rect(center=(score_rect.centerx,score_rect.centery))
        screen.blit(text, text_pos)

    def input(self, key):
        if key == K_ESCAPE:
            self.quit()
        if key == pygame.K_LEFT and not self.board.busy:
            self.board.shift_direction = LEFT
            self.board.busy = True
        if key == pygame.K_RIGHT and not self.board.busy:
            self.board.shift_direction = RIGHT
            self.board.busy = True
        if key == pygame.K_UP and not self.board.busy:
            self.board.shift_direction = UP
            self.board.busy = True
        if key == pygame.K_DOWN and not self.board.busy:
            self.board.shift_direction = DOWN
            self.board.busy = True

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    Game().play()