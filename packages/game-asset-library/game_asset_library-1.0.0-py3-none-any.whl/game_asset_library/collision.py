import pygame

def check_collision(rect1, rect2):
    """
    Check if two rectangular assets are colliding.
    
    Parameters:
    - rect1: First Pygame Rect object
    - rect2: Second Pygame Rect object
    """
    return rect1.colliderect(rect2)


def check_point_in_rect(point, rect):
    """
    Check if a point (x, y) is inside a rectangular asset.
    
    Parameters:
    - point: Tuple (x, y) representing the point
    - rect: Pygame Rect object
    """
    return rect.collidepoint(point)
