from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Base class for objects drawn on the game board."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draw the object on the game board."""
        pass


class Apple(GameObject):
    """An apple that the snake can eat."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        super().__init__(position, body_color)

    def randomize_position(self):
        """Place the apple at a random grid position."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Draw the apple on the game board."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """The player-controlled snake."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Return the snake's current head position."""
        return self.positions[0]

    def update_direction(self):
        """Apply the queued direction change."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move the snake forward by one grid cell."""
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head[1] + y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)
        self.last = self.positions[-1] if len(self.positions) > 1 else None
        self.positions.insert(0, new_position)
        if len(self.positions) > 1:
            self.positions.pop()

    def draw(self):
        """Draw the snake on the game board."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Reset the snake to its initial state."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def main():
    """Initialize and run the Snake game."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    apple.randomize_position()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            # Добавляем новый сегмент змейки
            snake.positions.append(
                snake.last if snake.last else snake.positions[-1]
            )
            apple.randomize_position()
            # Проверяем, чтобы яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


def handle_keys(game_object):
    """Update the game object's direction in response to keyboard input."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()
