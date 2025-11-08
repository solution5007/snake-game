import pygame
import random

pygame.init()

width, height = 400, 400
screen = pygame.display.set_mode((width, height))

black = (0, 0, 0)
green = (11, 218, 81)
white = (255, 255, 255)
gray = (135, 135, 135)
GRID_SIZE = 20
GAME_SPEED = 10

pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

class Menu:
    def __init__(self, width, height, title="SNAKE GAME"):
        self.width = width
        self.height = height
        self.title = title
        self.options = []
        self.selected_index = 0
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.active = True
        self.score = 0
    
    def set_options(self, options):
        self.options = options
        self.selected_index = 0

    def set_score(self, score):
        self.score = score

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
                return "navigate"
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
                return "navigate"
            elif event.key == pygame.K_RETURN:
                return self.selected_index
            elif event.key == pygame.K_LEFT:
                return "decrease"
            elif event.key == pygame.K_RIGHT:
                return "increase"
        return None
    
    def draw(self, screen):
        screen.fill(black)
        title_text = self.title_font.render(self.title, True, white)
        screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 80))
        
        if self.score > 0:
            score_text = self.font.render(f"Score: {self.score}", True, white)
            screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 150))

        for i, option in enumerate(self.options):
            color = green if i == self.selected_index else white
            text = self.font.render(option, True, color)
            x = self.width // 2 - text.get_width() // 2
            y = 200 + i * 50
            screen.blit(text, (x, y))

            if i == self.selected_index:
                arrow = self.font.render(">", True, green)
                screen.blit(arrow, (x - 40, y))

class Setting:
    def __init__(self, name, values, current_index=0):
        self.name = name
        self.values = values
        self.current_index = current_index
    
    def get_display_name(self):
        return f"{self.name}: {self.values[self.current_index]}"
    
    def next_value(self):
        self.current_index = (self.current_index + 1) % len(self.values)
        return self.values[self.current_index]
    
    def get_current_value(self):
        return self.values[self.current_index]

class SettingsManager:
    def __init__(self):
        self.settings = {
            "apples": Setting("Apples", [1, 2, 3, 5], 0)
        }
        self.setting_names = list(self.settings.keys())
    
    def get_menu_options(self):
        options = []
        for name in self.setting_names:
            options.append(self.settings[name].get_display_name())
        options.append("Back to Menu")
        return options
    
    def handle_setting_action(self, option_index):
        if option_index < len(self.setting_names):
            setting_name = self.setting_names[option_index]
            self.settings[setting_name].next_value()
            return "settings"
        else:
            return "menu"
    
    def get_setting_value(self, name):
        return self.settings[name].get_current_value()

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.dir = (GRID_SIZE, 0)
        self.grow = False
        self.next_dir = None
        self.last_move_position = self.body[0]

    def move(self):
        current_head = self.body[0]

        if (self.next_dir and 
            current_head[0] % GRID_SIZE == 0 and 
            current_head[1] % GRID_SIZE == 0 and 
            (self.next_dir[0] * -1, self.next_dir[1] * -1) != self.dir):
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

    def check_collision(self, width, height):
        head = self.body[0]
        if (head[0] < 0 or head[0] >= width or 
            head[1] < 0 or head[1] >= height):
            return True

        if head in self.body[1:]:
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, white, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

class Apple:
    def __init__(self, width, height):
        self.position = (0, 0)
        self.width = width
        self.height = height
        self.randomize_position()

    def randomize_position(self):
        max_x = (self.width // GRID_SIZE) - 1
        max_y = (self.height // GRID_SIZE) - 1
        x = random.randint(0, max_x) * GRID_SIZE
        y = random.randint(0, max_y) * GRID_SIZE
        self.position = (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, green, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))

class AppleManager:
    def __init__(self, width, height, max_apples=3):
        self.width = width
        self.height = height
        self.max_apples = max_apples
        self.apples = []
        self.spawn_apples()

    def set_max_apples(self, count):
        self.max_apples = max(1, count)
        self.adjust_apples_count()

    def adjust_apples_count(self):
        while len(self.apples) > self.max_apples:
            self.apples.pop()
        while len(self.apples) < self.max_apples:
            self.spawn_apple()

    def spawn_apples(self):
        self.apples = []
        for _ in range(self.max_apples):
            self.spawn_apple()

    def spawn_apple(self):
        one_apple = Apple(self.width, self.height)
        self.apples.append(one_apple)

    def check_collision(self, position):
        for i, apple in enumerate(self.apples):
            if apple.position == position:
                self.apples.pop(i)
                self.spawn_apple()
                return True
        return False

    def draw(self, screen):
        for apple in self.apples:
            apple.draw(screen)

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.settings = SettingsManager()
        self.reset_game()
        
        self.menu = Menu(width, height)
        self.menu.set_options(["Start Game", "Settings", "Quit"])
        self.game_state = "menu"

    def reset_game(self):
        self.snake = Snake()
        apples_count = self.settings.get_setting_value("apples")
        self.apple_manager = AppleManager(self.width, self.height, apples_count)
        self.score = 0
        self.game_over = False

    def update(self):
        if self.game_state == "playing" and not self.game_over:
            self.snake.move()
            
            if self.apple_manager.check_collision(self.snake.body[0]):
                self.snake.grow = True
                self.score += 1
            
            if self.snake.check_collision(self.width, self.height):
                self.game_over = True
                self.game_state = "menu"
                self.menu.set_options(["Restart Game", "Settings", "Quit"])
                self.menu.set_score(self.score)
                self.menu.title = "GAME OVER"

    def show_settings_menu(self):
        settings_menu = Menu(self.width, self.height, "SETTINGS")
        settings_menu.set_options(self.settings.get_menu_options())
        return settings_menu

    def handle_menu_action(self, action):
        if self.game_state == "settings":
            if action == "increase" or action == "decrease":
                self.menu = self.show_settings_menu()
                return True
            elif isinstance(action, int):
                new_state = self.settings.handle_setting_action(action)
                if new_state == "menu":
                    self.game_state = "menu"
                    self.menu.set_options(["Start Game", "Settings", "Quit"])
                    self.menu.title = "SNAKE GAME"
                elif new_state == "settings":
                    self.menu = self.show_settings_menu()
                return True
        
        if action == 0:
            self.reset_game()
            self.game_state = "playing"
            return True
        elif action == 1:
            self.game_state = "settings"
            self.menu = self.show_settings_menu()
            return True
        elif action == 2:
            pygame.quit()
            exit()
        
        return False

    def handle_menu_event(self, event):
        if self.game_state in ["menu", "settings"]:
            result = self.menu.handle_event(event)
            if result is not None:
                return self.handle_menu_action(result)
        return False

    def draw(self, screen):
        if self.game_state == "playing":
            screen.fill(black)
            self.draw_grid(screen)
            self.snake.draw(screen)
            self.apple_manager.draw(screen)
            
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, white)
            screen.blit(score_text, (10, 10))
            
        elif self.game_state in ["menu", "settings"]:
            self.menu.draw(screen)

    def draw_grid(self, screen):
        for x in range(0, self.width, GRID_SIZE):
            pygame.draw.line(screen, gray, (x, 0), (x, self.height))
        for y in range(0, self.height, GRID_SIZE):
            pygame.draw.line(screen, gray, (0, y), (self.width, y))

def main():
    game_instance = Game(width, height)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_instance.handle_menu_event(event):
                continue

            elif game_instance.game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game_instance.snake.change_dir((0, -GRID_SIZE))
                    elif event.key == pygame.K_DOWN:
                        game_instance.snake.change_dir((0, GRID_SIZE))
                    elif event.key == pygame.K_LEFT:
                        game_instance.snake.change_dir((-GRID_SIZE, 0))
                    elif event.key == pygame.K_RIGHT:
                        game_instance.snake.change_dir((GRID_SIZE, 0))
                    elif event.key == pygame.K_ESCAPE:
                        game_instance.game_state = "menu"
                        game_instance.menu.set_options(["Restart Game", "Settings", "Quit"])
                        game_instance.menu.set_score(game_instance.score)
        
        if game_instance.game_state == "playing":
            game_instance.update()
        
        game_instance.draw(screen)
        pygame.display.flip()
        clock.tick(GAME_SPEED)

if __name__ == "__main__":
    main()