import pygame
import pygame.gfxdraw
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Get the current display resolution
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h

# Set up the drawing window to be fullscreen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Set up the clock for a decent framerate
clock = pygame.time.Clock()


# Function to draw an animated rainbow background
def draw_rainbow_background(screen, angle):
    for x in range(0, screen_width):
        # Calculate color components based on the sine of the angle + x position
        red = math.sin(angle + x * 0.01) * 127 + 128
        green = math.sin(angle + x * 0.01 + 2 * math.pi / 3) * 127 + 128
        blue = math.sin(angle + x * 0.01 + 4 * math.pi / 3) * 127 + 128

        # Set the color for each vertical line
        color = (int(red), int(green), int(blue))

        # Draw a vertical line
        pygame.draw.line(screen, color, (x, 0), (x, screen_height))


# Function to draw psychedelic rectangles of static size
def draw_psychedelic_rectangles(screen, angle):
    for i in range(0, screen_width, 20):
        for j in range(0, screen_height, 20):
            # Calculate color components based on the sine of the angle
            red = (math.sin(angle + i) + 1) / 2
            green = (math.sin(angle + 2 + j) + 1) / 2
            blue = (math.sin(angle + 4 + (i+j)) + 1) / 2

            # Convert color components to 0-255 scale
            red = int(red * 255)
            green = int(green * 255)
            blue = int(blue * 255)

            # Create rectangles with varying colors
            rect_color = (red, green, blue)
            rect_x = i + (math.sin(angle + i) * 10)
            rect_y = j + (math.cos(angle + j) * 10)
            pygame.draw.rect(screen, rect_color, [rect_x, rect_y, 20, 20])


# Function to draw psychedelic rectangles of varying sizes
def draw_psychedelic_rectangles_varied(screen, angle, rect_size):
    # Calculate base rectangle size with a small variation
    base_rect_size = 20
    rect_size = base_rect_size + rect_size_variation

    for i in range(0, screen_width, base_rect_size):
        for j in range(0, screen_height, base_rect_size):
            # Calculate color components based on the sine of the angle
            red = (math.sin(angle + i) + 1) / 2
            green = (math.sin(angle + 2 + j) + 1) / 2
            blue = (math.sin(angle + 4 + (i+j)) + 1) / 2

            # Convert color components to 0-255 scale
            red = int(red * 255)
            green = int(green * 255)
            blue = int(blue * 255)

            # Create rectangles with varying colors and varying positions
            rect_color = (red, green, blue)
            rect_x = i + (math.sin(angle + i) * 10)
            rect_y = j + (math.cos(angle + j) * 10)
            pygame.draw.rect(screen, rect_color, [rect_x, rect_y, rect_size, rect_size])


def psychedelic_effect_rect(screen, angle):
    # Fill the background with black
    screen.fill((0, 0, 0))

    # Calculate color components based on the sine of the angle
    red = (math.sin(angle) + 1) / 2
    green = (math.sin(angle + 2) + 1) / 2
    blue = (math.sin(angle + 4) + 1) / 2

    # Convert color components to 0-255 scale
    red = int(red * 255)
    green = int(green * 255)
    blue = int(blue * 255)

    for i in range(0, screen_width, 20):
        for j in range(0, screen_height, 20):
            # Create rectangles with varying colors
            rect_color = (red, green, blue)
            rect_x = i + (math.sin(angle + i) * 10)
            rect_y = j + (math.cos(angle + j) * 10)
            pygame.draw.rect(screen, rect_color, [rect_x, rect_y, 20, 20])


# Function to smoothly change speed of the animation
def smooth_speed_change(current_speed, min_speed, max_speed):
    # Adjust the speed by a small random factor
    speed_change = random.uniform(-0.001, 0.001)
    new_speed = current_speed + speed_change

    # Clamp the new speed to be within min_speed and max_speed
    new_speed = max(min(new_speed, max_speed), min_speed)

    return new_speed


# Function to smoothly change rectangle size with a guaranteed minimum size
def smooth_rect_size_change(angle, min_variation, max_variation):
    # Sine function oscillates between -1 and 1
    oscillation = math.sin(angle)

    # Normalize the oscillation to be between 0 and 1
    normalized_oscillation = (oscillation + 1) / 2

    # Now map this to our min_variation and max_variation range
    size_variation = normalized_oscillation * (max_variation - min_variation) + min_variation

    return size_variation


class Ripple:
    def __init__(self, x, y, max_radius):
        self.x = x
        self.y = y
        self.radius = 1  # Start with a radius that is clearly visible
        self.max_radius = max_radius
        self.num_circles = random.randint(2, 5)
        self.color = (255, 255, 255)  # Default white for now, will be set by the gradient function
        self.alpha = 255  # Start with full opacity
        self.active = True
        self.growth_rate = random.uniform(0.01, 0.05)
        self.alpha_decay_rate = 255 / (self.max_radius / self.growth_rate)

    def update(self):
        # Increment the radius slower to ensure visibility
        growth_rate = 0.5  # Adjust this as needed to slow down the ripple's growth
        self.radius += growth_rate

        # Calculate fade rate based on the max radius and the desired lifespan of the ripple
        fade_rate = 255 / (self.max_radius / growth_rate)
        self.alpha -= fade_rate
        self.alpha = max(self.alpha, 0)

        # Deactivate the ripple if it's fully faded or has reached its maximum size
        if self.radius >= self.max_radius or self.alpha <= 0:
            self.active = False


def draw_ripples(surface, ripples, angle):
    ripples_to_remove = []
    for ripple in ripples:
        num_circles = ripple.num_circles
        step = ripple.radius / num_circles
        for i in range(num_circles):
            current_radius = ripple.radius - i * step
            if current_radius > 0:
                # Decrease alpha based on the size of the ripple
                current_alpha = int(max(ripple.alpha - (ripple.alpha_decay_rate * i), 0))

                # Calculate the color, ensuring it is a tuple of integers
                color = calculate_color_with_gradient(angle, current_alpha)

                # Draw the circle with the desired thickness
                thickness = 2  # For example, a thickness of 3
                for t in range(thickness):
                    if current_radius - t > 0:
                        # Ensure that we're drawing within the bounds of the surface
                        x, y = int(ripple.x), int(ripple.y)
                        if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                            pygame.gfxdraw.aacircle(surface, x, y, int(current_radius - t), color)
                            pygame.gfxdraw.circle(surface, x, y, int(current_radius - t), color)

        # Update the ripple's state for the next frame
        ripple.radius += ripple.growth_rate  # assuming there's a growth_rate attribute
        ripple.alpha -= ripple.alpha_decay_rate  # assuming there's an alpha_decay_rate attribute
        surface_width, surface_height = surface.get_size()
        upper_bound = max(surface_width, surface_height) * 1.5  # for example, 150% of the longest dimension

        # Update the ripple's state for the next frame
        ripple.update()  # This line updates both radius and alpha

        # Determine if ripple should be removed
        if not ripple.active:
            ripples_to_remove.append(ripple)

    # Remove the ripples that have faded away
    for ripple in ripples_to_remove:
        ripples.remove(ripple)


# Calculate color with gradient based on angle and given alpha
def calculate_color_with_gradient(angle, alpha):
    # Original color calculation
    red = math.sin(angle) * 127 + 128
    green = math.sin(angle + 2 * math.pi / 3) * 127 + 128
    blue = math.sin(angle + 4 * math.pi / 3) * 127 + 128

    # Tint strength (0 to 1, where 1 is full white color)
    tint_strength = 0.25

    # Apply the white tint to the original color
    red = red + (255 - red) * tint_strength
    green = green + (255 - green) * tint_strength
    blue = blue + (255 - blue) * tint_strength

    # Ensure the components are within the 0-255 range and convert alpha to integer
    return (int(red), int(green), int(blue), int(alpha))


ripples = []  # List to store current bubbles
min_size = 0.001  # The smallest size for rectangles to ensure the background is visible
max_size = 20  # The largest size for rectangles
running = True  # Run until the user asks to quit
angle = 0
current_speed = 0.02  # Starting speed
min_speed = 0.01  # Minimum speed
max_speed = 0.03  # Maximum speed
rect_size_variation = 0  # Starting rectangle size variation
min_variation = 0  # Min size variation
max_variation = 7  # Max size variation (this should be small for smoother transitions)
time = 0
time_increment = 0.1

while running:
    # Did the user click the window close button or press ESC?
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Update angle for the effects with a smoothly changing speed
    current_speed = smooth_speed_change(current_speed, min_speed, max_speed)
    angle += current_speed

    # Smoothly change rectangle size with a guarantee to shrink
    rect_size_variation = smooth_rect_size_change(angle, min_size, max_variation)

    # Draw the rainbow background
    draw_rainbow_background(screen, angle)

    # Draw the psychedelic effect
    # psychedelic_effect_rect(screen, angle)  # no rainbow background or size variation
    # draw_psychedelic_rectangles(screen, angle)  # rainbow background with no size variation
    draw_psychedelic_rectangles_varied(screen, angle, rect_size_variation)  # rainbow background with size variation

    # Update and draw bubbles
    draw_ripples(screen, ripples, angle)
    for ripple in ripples:
        ripple.update()

    time += time_increment
    ripple_probability = (math.sin(time) + 1) / 40  # oscillates between 0.025 and 0.075

    if random.random() < ripple_probability:
        max_radius = random.randint(30, 300)  # random max radius between 50 and 150
        new_ripple = Ripple(random.uniform(0, screen_width), random.uniform(0, screen_height), max_radius)
        ripples.append(new_ripple)

    # # Remove ripples that have grown too large
    ripple = [ripple for ripple in ripples if ripple.active]

    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of 60 frames per second
    clock.tick(60)

# Done! Time to quit.
pygame.quit()
sys.exit()
