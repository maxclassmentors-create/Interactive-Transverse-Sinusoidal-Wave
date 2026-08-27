import pygame
import math

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Transverse Sinusoidal Wave")

clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
BACKGROUND = (20, 25, 35)
GRID = (60, 65, 75)
WHITE = (240, 240, 240)
WAVE_COLOR = (50, 180, 255)
EQUILIBRIUM_COLOR = (150, 150, 150)
TEXT_COLOR = (240, 240, 240)
SLIDER_COLOR = (100, 100, 110)
HANDLE_COLOR = (255, 180, 50)

# -----------------------------
# Fonts
# -----------------------------
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 32, bold=True)

# -----------------------------
# Wave Variables
# -----------------------------

# Amplitude in pixels
amplitude = 100

# Frequency in Hz
frequency = 1.0

# Wavelength in pixels
wavelength = 400

# Wave speed in pixels/second
wave_speed = 400

# Time variable
time = 0

# Pause state
paused = False


# -----------------------------
# Slider Class
# -----------------------------
class Slider:
    def __init__(self, x, y, width, min_value, max_value, value, label):
        self.x = x
        self.y = y
        self.width = width

        self.min_value = min_value
        self.max_value = max_value
        self.value = value

        self.label = label

        self.dragging = False

    def value_to_x(self):
        percentage = (
            (self.value - self.min_value)
            / (self.max_value - self.min_value)
        )

        return self.x + percentage * self.width

    def x_to_value(self, mouse_x):
        percentage = (mouse_x - self.x) / self.width

        percentage = max(0, min(1, percentage))

        return self.min_value + percentage * (
            self.max_value - self.min_value
        )

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos

            handle_x = self.value_to_x()

            if abs(mouse_x - handle_x) < 15 and abs(mouse_y - self.y) < 20:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:

            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:

            if self.dragging:
                mouse_x = event.pos[0]

                self.value = self.x_to_value(mouse_x)

    def draw(self, surface):

        # Label
        label_surface = font.render(
            f"{self.label}: {self.value:.2f}",
            True,
            TEXT_COLOR
        )

        surface.blit(
            label_surface,
            (self.x, self.y - 45)
        )

        # Slider line
        pygame.draw.line(
            surface,
            SLIDER_COLOR,
            (self.x, self.y),
            (self.x + self.width, self.y),
            8
        )

        # Handle
        handle_x = self.value_to_x()

        pygame.draw.circle(
            surface,
            HANDLE_COLOR,
            (int(handle_x), self.y),
            12
        )


# -----------------------------
# Create Sliders
# -----------------------------

amplitude_slider = Slider(
    100, 580,
    400,
    20, 200,
    amplitude,
    "Amplitude (pixels)"
)

frequency_slider = Slider(
    650, 580,
    400,
    0.1, 5.0,
    frequency,
    "Frequency (Hz)"
)


# -----------------------------
# Draw Grid
# -----------------------------
def draw_grid():

    # Vertical grid lines
    for x in range(0, WIDTH, 50):

        pygame.draw.line(
            screen,
            GRID,
            (x, 150),
            (x, 500),
            1
        )

    # Horizontal grid lines
    for y in range(150, 501, 50):

        pygame.draw.line(
            screen,
            GRID,
            (0, y),
            (WIDTH, y),
            1
        )


# -----------------------------
# Draw Wave
# -----------------------------
def draw_wave():

    center_y = 325

    points = []

    # Convert wave speed into phase movement.
    phase = time * frequency * 2 * math.pi

    for x in range(WIDTH):

        # Sinusoidal transverse wave
        y = center_y + amplitude * math.sin(
            2 * math.pi * x / wavelength - phase
        )

        points.append((x, int(y)))

    if len(points) > 1:

        pygame.draw.lines(
            screen,
            WAVE_COLOR,
            False,
            points,
            4
        )


# -----------------------------
# Draw Equilibrium Line
# -----------------------------
def draw_equilibrium():

    center_y = 325

    pygame.draw.line(
        screen,
        EQUILIBRIUM_COLOR,
        (0, center_y),
        (WIDTH, center_y),
        2
    )

    label = small_font.render(
        "Equilibrium position",
        True,
        EQUILIBRIUM_COLOR
    )

    screen.blit(
        label,
        (20, center_y + 10)
    )


# -----------------------------
# Draw Information
# -----------------------------
def draw_information():

    wave_speed_actual = frequency * wavelength

    info = [
        f"Amplitude = {amplitude:.1f} px",
        f"Frequency = {frequency:.2f} Hz",
        f"Wavelength = {wavelength:.0f} px",
        f"Wave speed = f × λ = {wave_speed_actual:.1f} px/s"
    ]

    y = 90

    for text in info:

        surface = small_font.render(
            text,
            True,
            TEXT_COLOR
        )

        screen.blit(surface, (30, y))

        y += 25


# -----------------------------
# Main Program
# -----------------------------
running = True

while running:

    # Delta time in seconds
    dt = clock.tick(60) / 1000

    # -------------------------
    # Events
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Sliders
        amplitude_slider.handle_event(event)
        frequency_slider.handle_event(event)

        # Keyboard controls
        if event.type == pygame.KEYDOWN:

            # Space = pause/play
            if event.key == pygame.K_SPACE:
                paused = not paused

            # R = reset
            if event.key == pygame.K_r:

                amplitude_slider.value = 100
                frequency_slider.value = 1.0

                time = 0

    # -------------------------
    # Update Variables
    # -------------------------

    amplitude = amplitude_slider.value
    frequency = frequency_slider.value

    # Update wave
    if not paused:

        time += dt

    # -------------------------
    # Drawing
    # -------------------------

    screen.fill(BACKGROUND)

    # Title
    title = title_font.render(
        "Interactive Transverse Sinusoidal Wave",
        True,
        WHITE
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 20)
    )

    draw_grid()
    draw_equilibrium()
    draw_wave()
    draw_information()

    # Sliders
    amplitude_slider.draw(screen)
    frequency_slider.draw(screen)

    # Controls
    controls = small_font.render(
        "SPACE = Pause/Play       R = Reset",
        True,
        TEXT_COLOR
    )

    screen.blit(
        controls,
        (WIDTH // 2 - controls.get_width() // 2, 650)
    )

    # Pause indicator
    if paused:

        pause_text = font.render(
            "PAUSED",
            True,
            HANDLE_COLOR
        )

        screen.blit(
            pause_text,
            (WIDTH // 2 - pause_text.get_width() // 2, 110)
        )

    pygame.display.flip()


pygame.quit()