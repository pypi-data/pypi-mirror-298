import pygame

class PhysicsAnimation:
    def __init__(self, asset, gravity=0.5, bounce_factor=0.7):
        self.asset = asset
        self.x = 100
        self.y = 100
        self.vy = 0
        self.gravity = gravity
        self.bounce_factor = bounce_factor

    def update(self, dt):
        """
        Update the position of the asset using basic physics (gravity, bounce).
        """
        self.vy += self.gravity
        self.y += self.vy * dt

        # Bounce off the bottom of the screen
        if self.y > 500:
            self.y = 500
            self.vy = -self.vy * self.bounce_factor

        return self.asset, (self.x, self.y)


def ease_in_out(t):
    """
    Simple easing function for smooth animations.
    
    Parameters:
    - t: A float between 0 and 1, representing the animation progress.
    """
    return t * t * (3 - 2 * t)


class EasingAnimation:
    def __init__(self, asset, start_pos, end_pos, duration):
        self.asset = asset
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.duration = duration
        self.elapsed_time = 0

    def update(self, dt):
        """
        Update the position of the asset using an easing function.
        """
        self.elapsed_time += dt
        t = min(self.elapsed_time / self.duration, 1)  # Cap at 1
        eased_t = ease_in_out(t)

        new_x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * eased_t
        new_y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * eased_t

        return self.asset, (new_x, new_y)
