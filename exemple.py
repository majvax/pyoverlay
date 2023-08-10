from pyoverlay import Overlay, Point, Rect, RGBA, Color
import win32con


class OnTick:
    """This class is called every frame."""
    def __init__(self) -> None:
        self.fov_radius = 150

    def __call__(self, overlay: Overlay) -> None:
        if overlay.get_input(win32con.VK_ESCAPE):
            overlay.stop()
        if overlay.get_input(win32con.VK_PRIOR):
            self.fov_radius += 1
        if overlay.get_input(win32con.VK_NEXT):
            self.fov_radius -= 1

        if overlay.target.is_valid:
            # draw an empty circle
            overlay.draw_empty_circle(overlay.target.rect.center, self.fov_radius, Color.WHITE)
            # draw an empty rect
            overlay.draw_empty_rect(overlay.target.rect, Color.WHITE)
            # draw fps
            overlay.draw_text(f"FPS: {overlay.fps}", Point(overlay.target.rect.center.x, overlay.target.rect.top + 20), Color.GREEN)


if __name__ == "__main__":
    overlay = Overlay("Terminal")
    overlay.on_tick = OnTick()

    overlay.create()
    overlay.run()
