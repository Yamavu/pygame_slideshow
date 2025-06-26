import pygame
from pytest import fixture

from main import draw_background


@fixture
def screen_size():
    return (200, 100)


@fixture
def screen(screen_size):
    """Creates a Pygame Surface for testing."""
    screen = pygame.Surface(screen_size)
    return screen


def test_draw_background(screen):
    """Tests the draw_background function."""
    pygame.init()
    screen.fill((0, 0, 0))
    draw_background(screen)
    assert screen.get_width() == 200
    assert screen.get_height() == 100
    assert screen.get_at(screen.get_rect().center) != (0, 0, 0)
    pygame.quit()
