import sys
from typing import Iterator, Tuple
from argparse import ArgumentParser
from itertools import cycle
from pathlib import Path

from pygame import Surface, init as pygame_init, quit as pygame_quit, Rect
from pygame import QUIT, KEYDOWN, K_ESCAPE, SRCALPHA
from pygame.transform import smoothscale
from pygame.image import load
from pygame.time import Clock, get_ticks
from pygame.display import set_mode, flip
from pygame.event import get as get_events

IMAGE_SUFFIXES = [".jpg", ".png", ".jpeg", ".bmp"]

TARGET = Rect(100,40,400,400)
TARGET_RATIO = TARGET.width / TARGET.height

def images_iter(folder:Path) -> Iterator[Path]:
    if not folder.is_dir():
        raise ValueError(f"folder {str(folder)} is no directory")
    return cycle(sorted(folder.iterdir()))

def load_image_to_surface(image_path:Path) -> Surface:
    if not image_path.is_file():
        raise ValueError(f"image {str(image_path)} is no file")
    surface = load(image_path).convert_alpha()
    return surface

def scale_image(image_path:Path, rect:Rect) -> Surface:
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

def iter_slideshow_images(folder:Path):
    for image_path in images_iter(folder):
        if image_path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        target_surface = Surface(TARGET.size, flags=SRCALPHA)
        _scaled_image = scale_image(image_path, TARGET)
        _target_rect = _scaled_image.get_rect(center=target_surface.get_rect().center)
        target_surface.blit(_scaled_image, _target_rect)
        # draw _s in the center of _target_surface
        yield target_surface

def draw_background(screen:Surface) -> Surface:
    screen.fill((128, 32, 192))

def transition_fade(screen:Surface, cur_img:Surface, next_img:Surface, progress:float):
    def linear(p) -> int:
        return int(p *  255)
    def quadratic(p) -> int:
        return int(p * p * 255)
    _cur_img = cur_img.copy()
    _cur_img.set_alpha(linear(1.0-progress))
    _next_img = next_img.copy()
    _next_img.set_alpha(linear(progress))
    screen.blit(_cur_img, dest=TARGET.topleft)
    screen.blit(_next_img, dest=TARGET.topleft)

def main(folder:Path):
    pygame_init()
    transition_duration: int = 1000
    image_display_time: int = 3000
    screen_size: Tuple[int,int] = (640, 480)
    clock = Clock()
    screen = set_mode(screen_size)
    _iter = iter_slideshow_images(folder)
    cur_img = next(_iter, None)
    #current_image = next(image_iter, None)
    nxt_img = next(_iter, None)
    last_switch = get_ticks()
    running = True
    in_transition = False
    transistion_start = None
    progress = 0.0

    while running and cur_img:
        for event in get_events():
            if event.type == QUIT or \
              (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
        now = get_ticks()
        if not in_transition and nxt_img and \
              now - last_switch > image_display_time:
            in_transition = True
            transistion_start = now
            progress = 0.0
        draw_background(screen)
        if in_transition:
            progress = (now - transistion_start) / transition_duration
            if progress >= 1.0:
                # End of fade
                cur_img = nxt_img
                nxt_img = next(_iter, None) # preload next image
                last_switch = now
                in_transition = False
                progress = 0.0
            transition_fade(screen, cur_img, nxt_img, progress)
        else:
            screen.blit(cur_img, TARGET.topleft)
        flip()
        clock.tick(60)
    pygame_quit()
    sys.exit()

if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("folder", type=Path, default=Path("img"), nargs="?")
    args = p.parse_args()
    main(folder=args.folder)
