import sys
from typing import Iterator, Tuple, Callable
from argparse import ArgumentParser
from itertools import cycle
from pathlib import Path

from pygame import Surface, Rect
from pygame import init as pygame_init, quit as pygame_quit
from pygame import QUIT, KEYDOWN, K_ESCAPE, SRCALPHA
from pygame.transform import smoothscale
from pygame.image import load
from pygame.time import Clock, get_ticks
from pygame.display import set_mode, flip
from pygame.event import get as get_events

from transition import TRANSITION_FUNCTIONS


def images_iter(folder: Path) -> Iterator[Path]:
    """iterate over a directory repeatingly"""
    if not folder.is_dir():
        raise ValueError(f"folder {str(folder)} is no directory")
    return cycle(sorted(folder.iterdir()))


def load_image_to_surface(image_path: Path) -> Surface:
    """load an image to a pygame.Surface"""
    if not image_path.is_file():
        raise ValueError(f"image {str(image_path)} is no file")
    surface = load(image_path).convert_alpha()
    return surface


def _scale_image(image_path: Path, rect: Rect) -> Surface:
    """scale image to a given size"""
    s = load_image_to_surface(image_path)
    rect_ratio = rect.width / rect.height
    _width, _height = s.get_width(), s.get_height()
    _ratio = _width / _height
    if _ratio > rect_ratio:
        _target = (rect.width, int(rect.width / _ratio))
    elif _ratio < rect_ratio:
        _target = (int(rect.height * _ratio), rect.height)
    else:
        _target = (rect.width, rect.height)
    print(f"scaling {image_path.stem} from {(_width, _height)} to {_target}")
    return smoothscale(s, _target)


def iter_slideshow_images(
        folder: Path,
        target: Rect,
        image_suffixes: Tuple[str]):
    """
    scales an image from directory and center it
    returns a transparent pygame.Surface
    """
    for image_path in images_iter(folder):
        if image_path.suffix.lower() not in image_suffixes:
            continue
        surface = Surface(target.size, flags=SRCALPHA)
        _scaled_image = _scale_image(image_path, target)
        _target_rect = _scaled_image.get_rect(center=surface.get_rect().center)
        surface.blit(_scaled_image, _target_rect)
        yield surface


def draw_background(screen: Surface) -> None:
    """draws the background"""
    screen.fill((128, 32, 192))


def draw_foreground(screen: Surface) -> None:
    """draws the foreground"""
    pass


def get_transition_function(
    name: str,
) -> Callable[[Surface, Surface, Surface, float, Rect], None]:
    for k, fun in TRANSITION_FUNCTIONS.items():
        if k.name == name:
            return fun
    raise ValueError(f"transistion_type {name.name} not found")


def main(
        folder: Path,
        display_ms: int,
        transition_ms: int,
        transition_type: str):
    """show a slideshow to a window of a given size"""
    pygame_init()
    transition_function = get_transition_function(transition_type)
    screen_size: Tuple[int, int] = (640, 480)
    target = Rect(100, 40, 400, 400)
    image_suffixes = (".jpg", ".png", ".jpeg", ".bmp")
    # target_ratio = target.width / target.height
    clock = Clock()
    screen = set_mode(screen_size)
    _iter = iter_slideshow_images(folder, target, image_suffixes)
    cur_img = next(_iter, None)
    # current_image = next(image_iter, None)
    nxt_img = next(_iter, None)
    last_switch = get_ticks()
    running = True
    in_transition = False
    transistion_start = None
    progress = 0.0

    while running and cur_img:
        for event in get_events():
            if event.type == QUIT \
                    or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
        now = get_ticks()
        if not in_transition and nxt_img \
                and now - last_switch > display_ms:
            in_transition = True
            transistion_start = now
            progress = 0.0
        draw_background(screen)
        if in_transition:
            progress = (now - transistion_start) / transition_ms
            if progress >= 1.0:
                # End of fade
                cur_img = nxt_img
                nxt_img = next(_iter, None)  # preload next image
                last_switch = now
                in_transition = False
                progress = 0.0
            transition_function(screen, cur_img, nxt_img, progress, target)
        else:
            screen.blit(cur_img, target.topleft)
        draw_foreground(screen)
        flip()
        clock.tick(60)
    pygame_quit()
    sys.exit()


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("folder", type=Path, default=Path("img"), nargs="?")
    p.add_argument("image_display_time", type=float, default=4.0, nargs="?")
    p.add_argument("transition_time", type=float, default=1.0, nargs="?")
    p.add_argument("transition_type", type=str, default="scale_x", nargs="?")
    args = p.parse_args()
    main(
        folder=args.folder,
        display_ms=int(args.image_display_time * 1000),
        transition_ms=int(args.transition_time * 1000),
        transition_type=args.transition_type,
    )
