import pygame
import random

def apply_texture_overlay(asset, texture_type="stripes", color=(255, 255, 255)):
    """
    Apply a texture overlay to an asset (e.g., stripes, noise).
    
    Parameters:
    - texture_type: 'stripes', 'noise', 'dots'
    - color: RGB color of the texture overlay
    """
    width, height = asset.get_size()
    overlay = pygame.Surface(asset.get_size(), pygame.SRCALPHA)

    if texture_type == "stripes":
        for y in range(0, height, 10):
            pygame.draw.rect(overlay, color, (0, y, width, 5))

    elif texture_type == "noise":
        for x in range(width):
            for y in range(height):
                if random.random() > 0.9:
                    overlay.set_at((x, y), color)

    elif texture_type == "dots":
        for _ in range(100):
            pygame.draw.circle(overlay, color, (random.randint(0, width), random.randint(0, height)), 2)

    asset.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return asset


def apply_lighting(asset, intensity=0.3):
    """
    Apply a simple lighting effect to an asset by darkening parts of it.
    
    Parameters:
    - intensity: Float value for the darkness intensity (0 = no change, 1 = completely dark)
    """
    lighting_surface = pygame.Surface(asset.get_size(), pygame.SRCALPHA)
    lighting_surface.fill((0, 0, 0, int(255 * intensity)))
    asset.blit(lighting_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    return asset


def customize_with_gradient(asset, direction="vertical", start_color=(255, 0, 0), end_color=(0, 0, 255)):
    """
    Apply a gradient effect to an asset.
    
    Parameters:
    - direction: 'vertical' or 'horizontal'
    - start_color: RGB start color
    - end_color: RGB end color
    """
    width, height = asset.get_size()

    if direction == "vertical":
        for y in range(height):
            ratio = y / height
            new_color = [
                int(start_color[i] * (1 - ratio) + end_color[i] * ratio)
                for i in range(3)
            ]
            pygame.draw.line(asset, new_color, (0, y), (width, y))

    elif direction == "horizontal":
        for x in range(width):
            ratio = x / width
            new_color = [
                int(start_color[i] * (1 - ratio) + end_color[i] * ratio)
                for i in range(3)
            ]
            pygame.draw.line(asset, new_color, (x, 0), (x, height))

    return asset
