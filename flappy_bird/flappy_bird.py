import threading
import time
import pygame
import random
import requests

# Initialize global variables
user_input = 0
running = True

ESP_IP = "192.168.4.1"

ST_MAX = 0.1
ST_MIN = 1.6
ST_AVERAGE = (ST_MAX + ST_MIN) / 2

ST_OLD_MIN = 0
ST_OLD_MAX = 0

def fetch_data():
    global user_input  # Use global variable to communicate with the main thread
    esp_ip = ESP_IP  # Replace with the actual IP address of ESP32
    url = f"http://{esp_ip}/"
    
    while running:
        try:
            response = requests.get(url, timeout=1)
            voltage = float(response.text)
            
            # Scale the voltage to a suitable range for game control
            scaled_input = (voltage - ST_MIN) / (ST_MAX - ST_MIN) * 100
            user_input = min(max(int(scaled_input), 0), 100)
            print(voltage)
        except requests.exceptions.RequestException:
            user_input = 0


# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen dimensions
WIDTH = 1440
HEIGHT = 900

# Bird attributes
bird_y = HEIGHT // 2
bird_velocity = 0

# Pipe attributes
pipe_gap = 300
pipe_width = 75
pipe_velocity = 2
upper_pipe_height = random.randint(50, HEIGHT - pipe_gap - 50)
lower_pipe_height = HEIGHT - upper_pipe_height - pipe_gap
pipe_x = WIDTH

# Set up screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Start auxiliary thread
data_thread = threading.Thread(target=fetch_data)
data_thread.start()

pipes = []

def add_pipe():
    upper_pipe_height = random.randint(50, HEIGHT - pipe_gap - 50)
    lower_pipe_height = HEIGHT - upper_pipe_height - pipe_gap
    # Set initial x position of the new pipe based on the last pipe in the list
    new_x = WIDTH if not pipes else pipes[-1]["x"] + 300  # 300 is the spacing, adjust as needed
    pipes.append({"x": new_x, "upper_height": upper_pipe_height, "lower_height": lower_pipe_height})


# Start with four pipes
for _ in range(4):
    add_pipe()

while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Decide bird's velocity based on the voltage
    voltage_diff = user_input - 50  # Assuming user_input is scaled from 0 to 100
    bird_velocity = -voltage_diff / 10  # Adjust the divisor to control sensitivity

    # Update bird's position
    bird_y += bird_velocity

    # Prevent the bird from going off-screen
    if bird_y < 0:
        bird_y = 0
    elif bird_y + 20 > HEIGHT:
        bird_y = HEIGHT - 20

    # Draw the bird
    pygame.draw.circle(screen, RED, (WIDTH // 4, bird_y), 20)

    # Update and draw pipes
    for pipe in pipes:
        pipe["x"] -= pipe_velocity
        # Draw upper pipe
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, pipe_width, pipe["upper_height"]))
        # Draw lower pipe
        pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["upper_height"] + pipe_gap, pipe_width, pipe["lower_height"]))

    # Remove pipes that have moved off the left side of the screen and add new ones as needed
    pipes = [pipe for pipe in pipes if pipe["x"] + pipe_width > 0]
    while len(pipes) < 4:
        add_pipe()

    # Update the screen
    pygame.display.flip()
    clock.tick(60)

# Terminate the auxiliary thread
running = False
data_thread.join()  

pygame.quit()