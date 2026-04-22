import pygame
import math

pygame.init()

# Window size
WIDTH = 800
HEIGHT = 600

# Create main screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Base layer keeps all finished drawings
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))

# Colors
colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)

clock = pygame.time.Clock()

# Left mouse button pressed flag
LMBpressed = False

# Default thickness of shapes
THICKNESS = 5

# Current and previous mouse positions
currX = 0
currY = 0
prevX = 0
prevY = 0

# Default drawing mode
mode = "rect"

# Default drawing color
current_color = colorRED


# Calculate normal rectangle from two mouse points
def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))


# Calculate square from two mouse points
def calculate_square(x1, y1, x2, y2):
    side = min(abs(x2 - x1), abs(y2 - y1))

    # Determine direction of drawing
    if x2 >= x1:
        left = x1
    else:
        left = x1 - side

    if y2 >= y1:
        top = y1
    else:
        top = y1 - side

    return pygame.Rect(left, top, side, side)


# Calculate circle center and radius
def calculate_circle(x1, y1, x2, y2):
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) // 2)
    return center_x, center_y, radius


# Calculate points of a right triangle
def calculate_right_triangle(x1, y1, x2, y2):
    # Triangle with one 90-degree angle
    return [(x1, y1), (x1, y2), (x2, y2)]


# Calculate points of an equilateral triangle
def calculate_equilateral_triangle(x1, y1, x2, y2):
    # Use horizontal distance as side length
    side = abs(x2 - x1)

    # If side is too small, return simple points
    if side == 0:
        return [(x1, y1), (x1, y1), (x1, y1)]

    # Height formula for equilateral triangle
    height = int((math.sqrt(3) / 2) * side)

    # Determine direction
    if x2 >= x1:
        left_x = x1
        right_x = x1 + side
    else:
        left_x = x1 - side
        right_x = x1

    # Draw upward if mouse moved up, otherwise downward
    if y2 < y1:
        top_y = y1 - height
        base_y = y1
        top_point = ((left_x + right_x) // 2, top_y)
        left_point = (left_x, base_y)
        right_point = (right_x, base_y)
    else:
        top_y = y1
        base_y = y1 + height
        top_point = ((left_x + right_x) // 2, top_y)
        left_point = (left_x, base_y)
        right_point = (right_x, base_y)

    return [top_point, left_point, right_point]


# Calculate points of a rhombus
def calculate_rhombus(x1, y1, x2, y2):
    # Bounding rectangle
    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    # 4 points of rhombus
    return [
        (center_x, top),      # top
        (right, center_y),    # right
        (center_x, bottom),   # bottom
        (left, center_y)      # left
    ]


# Draw saved base layer first
screen.blit(base_layer, (0, 0))

running = True
while running:
    for event in pygame.event.get():
        # Quit window
        if event.type == pygame.QUIT:
            running = False

        # Start drawing on left mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX = event.pos[0]
            prevY = event.pos[1]

        # While mouse is moving with pressed button, show preview
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1]

                # Redraw old saved picture
                screen.blit(base_layer, (0, 0))

                if mode == "rect":
                    pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)

                elif mode == "square":
                    pygame.draw.rect(screen, current_color, calculate_square(prevX, prevY, currX, currY), THICKNESS)

                elif mode == "circle":
                    center_x, center_y, radius = calculate_circle(prevX, prevY, currX, currY)
                    if radius > 0:
                        pygame.draw.circle(screen, current_color, (center_x, center_y), radius, THICKNESS)

                elif mode == "line":
                    pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)

                elif mode == "right_triangle":
                    points = calculate_right_triangle(prevX, prevY, currX, currY)
                    pygame.draw.polygon(screen, current_color, points, THICKNESS)

                elif mode == "equilateral_triangle":
                    points = calculate_equilateral_triangle(prevX, prevY, currX, currY)
                    pygame.draw.polygon(screen, current_color, points, THICKNESS)

                elif mode == "rhombus":
                    points = calculate_rhombus(prevX, prevY, currX, currY)
                    pygame.draw.polygon(screen, current_color, points, THICKNESS)

        # Finish drawing when mouse button released
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX = event.pos[0]
            currY = event.pos[1]

            if mode == "rect":
                pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)

            elif mode == "square":
                pygame.draw.rect(screen, current_color, calculate_square(prevX, prevY, currX, currY), THICKNESS)

            elif mode == "circle":
                center_x, center_y, radius = calculate_circle(prevX, prevY, currX, currY)
                if radius > 0:
                    pygame.draw.circle(screen, current_color, (center_x, center_y), radius, THICKNESS)

            elif mode == "line":
                pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)

            elif mode == "right_triangle":
                points = calculate_right_triangle(prevX, prevY, currX, currY)
                pygame.draw.polygon(screen, current_color, points, THICKNESS)

            elif mode == "equilateral_triangle":
                points = calculate_equilateral_triangle(prevX, prevY, currX, currY)
                pygame.draw.polygon(screen, current_color, points, THICKNESS)

            elif mode == "rhombus":
                points = calculate_rhombus(prevX, prevY, currX, currY)
                pygame.draw.polygon(screen, current_color, points, THICKNESS)

            # Save final drawing to base layer
            base_layer.blit(screen, (0, 0))

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            # Increase thickness
            if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                THICKNESS += 1

            # Decrease thickness
            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                if THICKNESS > 1:
                    THICKNESS -= 1

            # Modes
            if event.key == pygame.K_r:
                mode = "rect"

            if event.key == pygame.K_s:
                mode = "square"

            if event.key == pygame.K_e:
                mode = "circle"

            if event.key == pygame.K_l:
                mode = "line"

            if event.key == pygame.K_t:
                mode = "right_triangle"

            if event.key == pygame.K_q:
                mode = "equilateral_triangle"

            if event.key == pygame.K_h:
                mode = "rhombus"

            # Colors
            if event.key == pygame.K_1:
                current_color = colorRED

            if event.key == pygame.K_2:
                current_color = colorBLUE

            if event.key == pygame.K_3:
                current_color = colorBLACK

            # Clear screen
            if event.key == pygame.K_c:
                base_layer.fill(colorWHITE)
                screen.blit(base_layer, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()