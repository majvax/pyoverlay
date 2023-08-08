from overlay import Overlay, Point, Rect, RGBA, Color
import time

import win32con

fov_radius = 150

# callable class
class OnTick:
    def __init__(self) -> None:
        self.fov_radius = 150
    
    def __call__(self, overlay: Overlay) -> None:
        if overlay.get_input(win32con.VK_ESCAPE):
            overlay.stop()
        if overlay.get_input(win32con.VK_PRIOR):
            self.fov_radius += 1
        if overlay.get_input(win32con.VK_NEXT):
            self.fov_radius -= 1

        
        overlay.draw_test(overlay.target.rect)

        return



        if overlay.target.is_valid:
            overlay.draw_line(
                start=Point(overlay.target.rect.left, overlay.target.rect.top),
                end=Point(overlay.target.rect.right, overlay.target.rect.bottom),
                color=RGBA(255, 255, 255, 1.0)
            )
            overlay.draw_line(
                start=Point(overlay.target.rect.right, overlay.target.rect.top),
                end=Point(overlay.target.rect.left, overlay.target.rect.bottom),
                color=RGBA(255, 255, 255, 1.0)
            )        
            overlay.draw_empty_circle(overlay.target.rect.center, self.fov_radius, Color.GREEN)
            overlay.draw_empty_rect(overlay.target.rect, RGBA(255, 255, 255, 1.0))
            overlay.draw_textbox(Point(0, 0), text=f"{str(overlay.fps)} fps", anchor="ul")
            overlay.draw_textbox(Point(0, 50), text=f"{str(overlay.ms)} ms", anchor="ul")


class Crosshair:
    def __init__(self) -> None:
        pass

    def __call__(self, overlay: Overlay) -> None:
        overlay.draw_line(
            start=Point(overlay.target.rect.center.x - 10, overlay.target.rect.center.y),
            end=Point(overlay.target.rect.center.x + 10, overlay.target.rect.center.y),
            color=Color.WHITE
        )
        overlay.draw_line(
            start=Point(overlay.target.rect.center.x, overlay.target.rect.center.y - 10),
            end=Point(overlay.target.rect.center.x, overlay.target.rect.center.y + 10),
            color=Color.WHITE
        )



def on_tick_(overlay: Overlay) -> None:
    global fov_radius


    if overlay.get_input(win32con.VK_PRIOR):
        fov_radius += 1
    if overlay.get_input(win32con.VK_NEXT):
        fov_radius -= 1


    if overlay.target.is_valid:
        overlay.draw_line(
            Point(overlay.target.rect.left, overlay.target.rect.top),
            Point(overlay.target.rect.right, overlay.target.rect.bottom),
            RGBA(255, 255, 255, 1.0)
        )
        overlay.draw_line(
            Point(overlay.target.rect.right, overlay.target.rect.top),
            Point(overlay.target.rect.left, overlay.target.rect.bottom),
            RGBA(255, 255, 255, 1.0)
        )        
        overlay.draw_empty_circle(overlay.target.rect.center, fov_radius, RGBA(0, 255, 0, 1.0))
        overlay.draw_empty_rect(overlay.target.rect, RGBA(255, 255, 255, 1.0))
        overlay.draw_textbox(Point(0, 0), text=f"{str(overlay.fps)} fps", anchor="ul")
        overlay.draw_textbox(Point(0, 50), text=f"{str(overlay.ms)} ms", anchor="ul")

def on_error(overlay: Overlay, error: str) -> None:
    print(error)
    



def main() -> None:
    
    overlay = Overlay("Terminal")
    # overlay.on_tick = Crosshair()
    overlay.on_tick = OnTick()
    # overlay.on_error = on_error

    overlay.create()
    overlay.run()


if __name__ == "__main__":
    main()
