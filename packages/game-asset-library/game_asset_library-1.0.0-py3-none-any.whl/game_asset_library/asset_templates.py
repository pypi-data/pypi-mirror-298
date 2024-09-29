import pygame
import random
import math

def create_dynamic_character(parts=None, color=(0, 128, 255), size=(100, 150)):
    """
    Create a character with dynamic, customizable parts (head, body, arms, legs).
    Parts can be customized using a dictionary: {'head': 'circle', 'arms': 'lines', etc.}
    
    Parameters:
    - parts: Dictionary to customize parts (e.g., {'head': 'circle', 'body': 'square', ...})
    - color: Base RGB color of the character
    - size: Tuple for size (width, height)
    """
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)

    # Default parts if not provided
    default_parts = {
        'head': 'circle',
        'body': 'rectangle',
        'arms': 'lines',
        'legs': 'lines'
    }
    if not parts:
        parts = default_parts

    # Draw body
    body_color = (color[0], color[1] - 30, color[2])
    pygame.draw.rect(surface, body_color, (width // 4, height // 2, width // 2, height // 2))

    # Draw head
    if parts['head'] == 'circle':
        pygame.draw.circle(surface, (255, 255, 255), (width // 2, height // 4), width // 4)
    elif parts['head'] == 'square':
        pygame.draw.rect(surface, (255, 255, 255), (width // 3, height // 6, width // 3, width // 3))

    # Draw arms
    if parts['arms'] == 'lines':
        pygame.draw.line(surface, (0, 0, 0), (width // 4, height // 2), (0, height // 3), 3)
        pygame.draw.line(surface, (0, 0, 0), (3 * width // 4, height // 2), (width, height // 3), 3)

    # Draw legs
    if parts['legs'] == 'lines':
        pygame.draw.line(surface, (0, 0, 0), (width // 3, height), (width // 3, height + 20), 3)
        pygame.draw.line(surface, (0, 0, 0), (2 * width // 3, height), (2 * width // 3, height + 20), 3)

    return surface


def create_polygon_object(vertices=5, color=(0, 255, 0), size=(40, 40)):
    """
    Create a procedurally generated polygon with a specified number of vertices.
    
    Parameters:
    - vertices: Number of vertices in the polygon
    - color: RGB tuple for color
    - size: Tuple for size (width, height)
    """
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)
    center = (width // 2, height // 2)
    radius = min(width, height) // 2
    points = []

    for i in range(vertices):
        angle = 2 * math.pi * i / vertices
        x = center[0] + int(radius * math.cos(angle))
        y = center[1] + int(radius * math.sin(angle))
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)
    return surface


def create_textured_background(pattern_type="gradient", colors=((255, 0, 0), (0, 0, 255)), size=(800, 600)):
    """
    Create a textured background with different patterns (gradient, noise, stripes, etc.).
    
    Parameters:
    - pattern_type: 'gradient', 'stripes', 'noise', 'circles', etc.
    - colors: Color tuple for patterns (start_color, end_color)
    - size: Size of the background surface
    """
    surface = pygame.Surface(size)
    width, height = size

    if pattern_type == "gradient":
        start_color, end_color = colors
        for y in range(height):
            ratio = y / height
            new_color = [
                int(start_color[i] * (1 - ratio) + end_color[i] * ratio)
                for i in range(3)
            ]
            pygame.draw.line(surface, new_color, (0, y), (width, y))

    elif pattern_type == "noise":
        for x in range(width):
            for y in range(height):
                if random.random() > 0.95:
                    surface.set_at((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    elif pattern_type == "stripes":
        for y in range(0, height, 20):
            pygame.draw.rect(surface, colors[0], (0, y, width, 10))

    elif pattern_type == "circles":
        for _ in range(100):
            radius = random.randint(5, 30)
            pygame.draw.circle(surface, colors[random.randint(0, 1)], (random.randint(0, width), random.randint(0, height)), radius)

    return surface
