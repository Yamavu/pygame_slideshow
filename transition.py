from typing import Callable, Dict
from enum import Enum, auto

from pygame import Surface, Rect


def transistion_flip(
        screen: Surface,
        cur_img: Surface,
        next_img: Surface,
        progress: float,
        target: Rect):
    """simply change from one image to another preloaded image"""
    if progress > 0.5:
        screen.blit(next_img, dest=target.topleft)
    else:
        screen.blit(cur_img, dest=target.topleft)


def linear(p) -> int:
    """internal function for linear transition"""
    return int(p * 255)


def polynomial(p, x) -> int:
    """internal function for polynomial transition"""
    return int(pow(p, x) * 255)


def transition_fade(
        screen: Surface,
        cur_img: Surface,
        next_img: Surface,
        progress: float,
        target: Rect):
    """fade from one image to another preloaded image"""
    _cur_img = cur_img.copy()
    _cur_img.set_alpha(polynomial(1.0-progress, 4))
    _next_img = next_img.copy()
    _next_img.set_alpha(linear(progress))
    screen.blit(_cur_img, dest=target.topleft)
    screen.blit(_next_img, dest=target.topleft)


class TransitionType(Enum):
    """all available types for transitioning from one image to another"""
    flip = auto()
    fade = auto()


TRANSITION_FUNCTIONS: Dict[
        Enum,
        Callable[[Surface, Surface, Surface, float, Rect], None]] = {
    TransitionType.fade: transition_fade,
    TransitionType.flip: transistion_flip
}
