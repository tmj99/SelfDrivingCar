import pygame
from picamera2 import Picamera2
import io

# Initialize Pygame
pygame.init()

# Set the screen dimensions (adjust as needed)
screen_width = 640
screen_height = 480

# Create a Pygame display window
screen = pygame.display.set_mode((screen_width, screen_height))

# Create a Pygame clock to control frame rate
clock = pygame.time.Clock()

# Initialize the Raspberry Pi Camera
camera = Picamera2()
camera.resolution = (screen_width, screen_height)

try:
    while True:
        # Capture an image from the camera
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        image = pygame.image.load(io.BytesIO(stream.read()))

        # Display the captured image on the Pygame screen
        screen.blit(image, (0, 0))
        pygame.display.flip()

        # Check for quit events (e.g., closing the Pygame window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Control the frame rate (adjust as needed)
        clock.tick(30)

except KeyboardInterrupt:
    # Clean up and exit the program on KeyboardInterrupt (Ctrl+C)
    pygame.quit()