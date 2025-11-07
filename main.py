import pygame
import random

pygame.init()

width, height = 400, 400

screen = pygame.display.set_mode((width,height))

black = (0,0,0)
green = (11,218,81)
white = (255,255,255)
gray = (135, 135, 135)
GRID_SIZE = 20

pygame.display.set_caption("snake")
clock = pygame.time.Clock()

class snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.dir = (GRID_SIZE, 0)
        self.grow = False
        self.next_dir = None
        self.last_move_position = self.body[0]

    def move(self):
        current_head = self.body[0]

        if (self.next_dir
        and current_head[0] % GRID_SIZE == 0
        and current_head[1] % GRID_SIZE == 0
        and (self.next_dir[0] * -1, self.next_dir[1] * -1) != self.dir):
            self.dir = self.next_dir
            self.next_dir = None
        
        head_x, head_y = self.body[0]
        new_head = (head_x + self.dir[0], head_y + self.dir[1])
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_dir(self, new_dir):
        self.next_dir = new_dir

    def check_collision(self,width,height):
        head = self.body[0]
        if (head[0] < 0 
        or head[0] >= width
        or head[1] < 0
        or head[1] >= height):
            return True

        if head in self.body[1:]:
            return True

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, white,(segment[0],segment[1],GRID_SIZE, GRID_SIZE))

class apple:
    def __init__(self,width,height):
        self.position = (0,0)
        self.width = width
        self.height = height
        self.randomize_position()

    def randomize_position(self):
        max_x = (self.width // GRID_SIZE) - 1
        max_y = (self.height // GRID_SIZE) - 1
        x = random.randint(0, max_x) * GRID_SIZE
        y = random.randint(0, max_y) * GRID_SIZE
        self.position = (x,y)

    def draw(self,screen):
        pygame.draw.rect(screen, green, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

class game:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.snake = snake()
        self.apple = apple(width,height)
        self.score = 0
        self.game_over = False

    def update(self):
        if not self.game_over:
            snake_head = self.snake.body[0]
            apple_pos = self.apple.position
            self.snake.move()
            if self.snake.body[0] == self.apple.position:
                self.snake.grow = True
                self.score +=1
                self.apple.randomize_position()
                while self.apple.position in self.snake.body:
                    self.apple.randomize_position()
        if self.snake.check_collision(self.width,self.height):
            self.game_over = True

    def draw_grid(self,screen):
        for x in range(0, self.width, GRID_SIZE):
            pygame.draw.line(screen, gray, (x, 0),(x, self.height))
        for y in range(0, self.height, GRID_SIZE):
            pygame.draw.line(screen, gray, (0, y), (self.width, y))      


    def draw(self,screen):
        screen.fill(black)
        self.draw_grid(screen)
        self.snake.draw(screen)
        self.apple.draw(screen)
        font = pygame.font.Font(None,36)
        score_text = font.render(f"{self.score}",True,white)
        screen.blit(score_text,(10,10))

def main():
    game_instance = game(width, height)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_instance.snake.change_dir((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    game_instance.snake.change_dir((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    game_instance.snake.change_dir((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    game_instance.snake.change_dir((GRID_SIZE, 0))
        game_instance.update()
        game_instance.draw(screen)
        pygame.display.flip()
        clock.tick(10)



if __name__ == "__main__":
    main()