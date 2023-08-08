from pyoverlay import Overlay, Point, Rect, RGBA, Color
import win32con
import time



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




def main() -> None:
    
    overlay = Overlay("Terminal")
    overlay.on_tick = OnTick()

    overlay.create()
    overlay.run()


if __name__ == "__main__":
    main()
