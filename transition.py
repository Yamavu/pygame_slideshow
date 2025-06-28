from typing import Callable, Dict
from enum import Enum, auto
from functools import partial

from pygame import Surface, Rect
from pygame.transform import smoothscale_by


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


def transistion_scale(
        screen: Surface,
        cur_img: Surface,
        next_img: Surface,
        progress: float,
        target: Rect,
        dim: int = 0):
    """center scale current image down and scale up next image """
    _cur_fac = (
        (2*(-0.5+progress), 1),
        (2*(0.5-progress), 1)
    )
    if dim == 1:
        _cur_fac = [(y, x) for x, y in _cur_fac]
    if progress > 0.5:
        _next_img = smoothscale_by(next_img, _cur_fac[0])
        target = _next_img.get_rect(center=target.center)
        screen.blit(_next_img, dest=target.topleft)
    else:
        _cur_img = smoothscale_by(cur_img, _cur_fac[1])
        target = _cur_img.get_rect(center=target.center)
        screen.blit(_cur_img, dest=target.topleft)


transistion_scale_x = partial(transistion_scale, dim=0)


transistion_scale_y = partial(transistion_scale, dim=1)


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
    scale_x = auto()
    scale_y = auto()


TRANSITION_FUNCTIONS: Dict[
        Enum,
        Callable[
            [Surface, Surface, Surface, float, Rect],
            None]] = {
    TransitionType.fade: transition_fade,
    TransitionType.flip: transistion_flip,
    TransitionType.scale_x: transistion_scale_x,
    TransitionType.scale_y: transistion_scale_y
}
