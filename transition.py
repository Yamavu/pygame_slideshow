from pygame import Surface, Rect

def linear(p) -> int:
    return int(p *  255)

def polynomial(p, x) -> int:
    return int(pow(p,x) * 255)

def transition_fade(screen:Surface, cur_img:Surface, next_img:Surface, progress:float, target:Rect):
    _cur_img = cur_img.copy()
    _cur_img.set_alpha(polynomial(1.0-progress, 4))
    _next_img = next_img.copy()
    _next_img.set_alpha(linear(progress))
    screen.blit(_cur_img, dest=target.topleft)
    screen.blit(_next_img, dest=target.topleft)
