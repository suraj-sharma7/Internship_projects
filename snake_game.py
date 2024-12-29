import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)  # Grass green for the background
SNAKE_BODY_COLOR = (0, 128, 255)  # Blue color for the snake body

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enhanced Snake Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Snake initialization
snake = [(100, 100)]
snake_direction = 'RIGHT'
change_to = snake_direction

# Food positions
food = (
    random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
    random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
)
special_food = None
special_food_timer = 0

# Score and speed
score = 0
speed = 10

# Timer initialization
last_special_food_time = time.time()

# Load textures and images
grass_texture = pygame.image.load("grssPn.png")
grass_texture = pygame.transform.scale(grass_texture, (CELL_SIZE, CELL_SIZE))
food_image = pygame.image.load("apple.jpg")
food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))
special_food_image = pygame.image.load("honey.jpg")
special_food_image = pygame.transform.scale(special_food_image, (CELL_SIZE, CELL_SIZE))
snake_head_image = pygame.image.load("head.jpg")
snake_head_image = pygame.transform.scale(snake_head_image, (CELL_SIZE, CELL_SIZE))

def draw_background():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            screen.blit(grass_texture, (x, y))

def show_score():
    font = pygame.font.SysFont('Arial', 24)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_surface, (10, 10))

def show_speedometer():
    font = pygame.font.SysFont('Arial', 24)
    speed_surface = font.render(f'Speed: {speed}', True, WHITE)
    screen.blit(speed_surface, (10, 40))

def spawn_special_food():
    return (
        random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
        random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
    )

def game_loop():
    global snake_direction, change_to, food, special_food, score, speed, last_special_food_time, special_food_timer
    
    while True:
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'

        # Spawn special food every 15 seconds
        if special_food is None and current_time - last_special_food_time >= 15:
            special_food = spawn_special_food()
            special_food_timer = 5  # Special food lasts for 5 seconds

        # Reduce special food timer
        if special_food is not None:
            special_food_timer -= 1 / speed
            if special_food_timer <= 0:
                special_food = None
                last_special_food_time = time.time()

        # Change direction
        snake_direction = change_to

        # Move the snake
        head_x, head_y = snake[0]
        if snake_direction == 'UP':
            head_y -= CELL_SIZE
        elif snake_direction == 'DOWN':
            head_y += CELL_SIZE
        elif snake_direction == 'LEFT':
            head_x -= CELL_SIZE
        elif snake_direction == 'RIGHT':
            head_x += CELL_SIZE

        # Wrap around the screen
        head_x %= SCREEN_WIDTH
        head_y %= SCREEN_HEIGHT

        # Insert new head position
        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # Check if snake eats the food
        if new_head == food:
            score += 1
            if score % 10 == 0:
                speed += 5
            food = (
                random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
            )
        elif special_food is not None and new_head == special_food:
            score += 5
            special_food = None
            last_special_food_time = time.time()
        else:
            # Remove the tail if no food is eaten
            snake.pop()

        # Check if the snake collides with itself
        if new_head in snake[1:]:
            game_over()

        # Draw everything
        draw_background()

        # Draw the snake
        for i, segment in enumerate(snake):
            if i == 0:
                screen.blit(snake_head_image, segment)
            else:
                pygame.draw.rect(screen, SNAKE_BODY_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Draw the food
        screen.blit(food_image, food)

        # Draw special food if it exists
        if special_food is not None:
            screen.blit(special_food_image, special_food)

        # Display score and speedometer
        show_score()
        show_speedometer()

        # Refresh the game screen
        pygame.display.update()

        # Control the game speed
        clock.tick(speed)

def game_over():
    font = pygame.font.SysFont('Arial', 36)
    game_over_surface = font.render('Game Over! Press any key to exit.', True, WHITE)
    screen.blit(game_over_surface, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3))
    pygame.display.flip()

    # Wait for a key press
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()

# Start the game
if __name__ == "__main__":
    game_loop()
